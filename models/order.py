from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta
import base64

class Order(models.Model):
    _name = 'product.order'
    _description = 'Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'orderId'

    order_date = fields.Datetime(string='Order Date')
    customer_id = fields.Many2one('my.customer.customer', string='Customer')
    customer_email = fields.Char(string='Customer Email', related='customer_id.email', store=True)
    customer_address = fields.Text(string='Customer Address', related='customer_id.address', store=True)
    order_item_ids = fields.One2many('order.item', 'order_id', string='Order Items', auto_join=True, store=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]).id)
    orderId = fields.Char(string='Order Id', readonly=True, default='New')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancel','Cancel')], string='Status', default='draft')
    delivery_id = fields.Many2one('product.delivery.me' , string = 'Delivery ID' , readonly=True)
    payment_method = fields.Selection([
        ('debit_card', 'Debit Card'),
        ('credit_card', 'Credit Card'),
        ('upi', 'UPI'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ], string='Payment Method')

    payment_status = fields.Selection([
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ], string='Payment Status', compute='_compute_payment_status', store=True)

    def action_draft(self):
        # print(self)
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        fields_metadata = self.env['product.order'].fields_get(allfields=['customer_id', 'state','payment_status'],attributes=['string', 'type', 'required', 'selection'])
        print(fields_metadata)
        for rec in self:
            rec.state = 'confirmed'
        for order in self:
            template_id = self.env.ref('Online_shopping.send_order_confirmation')
            template_id.send_mail(order.id, force_send=True)

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_done_success(self):
        self.write({'state': 'done',
                    'payment_status':'paid'})

    @api.depends('payment_method')
    def _compute_payment_status(self):
        for record in self:
            if record.payment_method == 'cash_on_delivery':
                record.payment_status = 'unpaid'
            else:
                record.payment_status = 'paid'
    
    @api.depends('order_item_ids')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order_item.price_subtotal for order_item in order.order_item_ids)
    
    @api.depends('order_item_ids')
    def _compute_order_item_count(self):
        for order in self:
            order.order_item_count = len(order.order_item_ids)

    # @api.depends('order_item_ids')
    # def _compute_order_item_details(self):
    #     for order in self:
    #         order.order_item_product_ids = order.order_item_ids.mapped('product_id')
    #         order.order_item_quantities = [(6, 0, order.order_item_ids.mapped('quantity'))]
    #         order.order_item_prices_unit = [(6, 0, order.order_item_ids.mapped('price_unit'))]
    #         order.order_item_subtotals = [(6, 0, order.order_item_ids.mapped('price_subtotal'))]

    @api.depends('order_item_ids')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(order_item.price_subtotal for order_item in order.order_item_ids)

    @api.model
    def create(self, vals):
        vals['orderId'] = self.env['ir.sequence'].next_by_code('product.order') or 'New'
        res = super(Order,self).create(vals)
        return res
    
    def write(self, vals):
        res = super(Order, self).write(vals)
        # if self.state == 'confirmed':
        confirmed_orders = self.filtered(lambda order: order.state == 'confirmed')
        print('confirmed_orders',confirmed_orders)
        for order in confirmed_orders:
            # print(confirmed_orders)
            # Check delivery record already exists or not
            existing_delivery = self.env['product.delivery.me'].search([('order_id', '=', order.id)], limit=1)
            # print('existing_delivery',existing_delivery)
            if existing_delivery:
                delivery_vals = {
                    'delivery_date': fields.Date.today() + timedelta(days=3), 
                    'payment': 'paid' if order.payment_status == 'paid' else 'unpaid' , 
                    'state' : 'ordered'
                }
                existing_delivery.write(delivery_vals)
                # print('existing_delivery',existing_delivery)
            else:
               
                self.env['product.delivery.me'].create({
                    'order_id': order.id,
                    'customer_id': order.customer_id.id,
                    'delivery_date': fields.Date.today() + timedelta(days=3),  
                    'payment': 'paid' if order.payment_status == 'paid' else 'unpaid' , 
                    'state' : 'ordered'
                })
            # query = """ALTER TABLE product_category_me DROP COLUMN create_uid"""
            query = """SELECT id FROM product_order"""
            self.env.cr.execute(query)
            order1 = self.env.cr.fetchall()
            # print("order1------>", order1)
        return res

    def cancel_order(self):
        return {
            'name': 'Cancel Order',
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.order.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
    
    def download_report(self):
        data = self.env["product.order"].search([('state', '=', 'confirmed')])
        # print("data",data)
        action = self.env.ref('Online_shopping.action_report_product_order').with_context(report = True, order_lines = data).report_action(data)
        return action

    def all_orders(self):
        print(self)
        
    # def confirm_order_with_email(self):
    #     self.action_confirm()
        
    #     template = self.env.ref('Online_shopping.email_template_order_confirmation')
    #     template_values = {
    #         'name': self.customer_id, 
    #     }
        
    #     if 'order_id' in template_values:
    #         del template_values['order_id']

    #     body_html = template._render_template(template.body_html, **template_values)
        
    #     mail_values = {
    #         'subject': template.subject,
    #         'body_html': body_html,
    #         'email_to': self.customer_email, 
    #         'email_from': self.env.user.email,
    #     }
        
    #     self.env['mail.mail'].create(mail_values).send()
    #     print("Order confirmation email sent successfully.")
        
    #     return True




    