from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessError
from datetime import datetime, timedelta
import base64

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    extra_tags = fields.Char(string="extra_tags")
    image = fields.Image(string="Image", related="product_id.image_1920")

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            'extra_tags': self.extra_tags
        })
        return values


class writeAnotherDetail(models.Model):
    _inherit="stock.move"

    extra_tags = fields.Char(string = "Extra field")
    image = fields.Image(string="Image", related="product_id.image_1920")


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['extra_tags']
        return fields


class SaleOrder(models.Model):
    _inherit = "sale.order"
            
    # def generate_report(self): 
    #     print("Generating report for Sale Order:", self.name)
    #     return True

    # commission = fields.Float(string="Commission", compute="compute_commision_amount")
    
    # @api.depends("amount_total")
    # def compute_commision_amount(self):
    #     for i in self:
    #         i.commission = (i.amount_total*5)/100

    commission = fields.Float(string="Commission", compute="compute_commision_amount")
    
    @api.depends("amount_total", "partner_id.commission_amount_on", "partner_id.percentage")
    def compute_commision_amount(self):
        for order in self:
            if order.amount_total > order.user_id.partner_id.commission_amount_on:
                order.commission = (order.amount_total * order.user_id.partner_id.percentage) / 100
            else:
                order.commission = 0.0

    commission_order_id = fields.Many2one('commission.on.line', string='Commission Order', readonly=True)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.commission_order_id:
            self.commission_order_id.write({
                'order_id': self.name,
                'customer_name': self.user_id.name,
                'order_date': self.date_order,
                'commission': self.commission,
                'total': self.amount_total,
            })
        else:
            commission_order = self.env['commission.on.line'].create({
                'order_id': self.name,
                'customer_name': self.user_id.name,
                'order_date': self.date_order,
                'commission': self.commission,
                'total': self.amount_total,
            })
            self.commission_order_id = commission_order.id
        return res

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        if self.commission_order_id:
            self.commission_order_id.unlink()
        return res

    checking_date = fields.Date(string = "Ordering Date", help="enter the date when order was placed")

    nick_name = fields.Char(string="Nick Name")

    def action_generate_sale_report(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generate Sale Report',
            'res_model': 'sale.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id}
        }

    @api.model
    def _get_order_lines_to_report(self):
        order_lines_context = self.env.context.get('order_lines')
        if order_lines_context:
            return self.order_line.filtered(lambda l: l.id in order_lines_context)
        return super(SaleOrder, self)._get_order_lines_to_report()

    def generate_and_send_monthly_report(self):
        today = fields.Date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        start_date = first_day_of_previous_month.strftime('%Y-%m-%d')
        end_date = last_day_of_previous_month.strftime('%Y-%m-%d')

        salespersons = self.env['res.users'].search([('share', '=', False)])
        for salesperson in salespersons:
            # print('salesperson',salesperson.name)
            report = self.env['send.sales.report'].action_xlsx_report_download(salesperson , start_date, end_date)
            attachment = self.env['ir.attachment'].create({
                'name': f'sales_report_from_{start_date}_to_{end_date}.xlsx',
                'type': 'binary',
                'datas': base64.b64encode(report),
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            })

            email_values = {
                'subject': f"Monthly Sales Report ({start_date} to {end_date})",
                'email_to':f'{salesperson.login}',
                'email_from':f'{self.env.user.email}',
                'attachment_ids': [(4, attachment.id)],
            }

            mail_template = self.env.ref('Online_shopping.email_template_sale_report')
            mail_template.send_mail(salesperson.id , email_values=email_values, force_send=True)

        return True

    state = fields.Selection(selection_add=[('to_approve', "To Approve")])

    def action_confirm(self):
        # print(self)
        for order in self:
            sale_limit = float(self.env['ir.config_parameter'].sudo().get_param('sale_limit'))
            if order.amount_total > sale_limit:
                order.state = 'to_approve'
            else:
                super(SaleOrder, order).action_confirm()

    def action_approve(self):
        self.env['sale.order'].browse(self.id).state = 'sale'

    

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    nick_name = fields.Char(string="Nick Name", readonly=True,related='sale_id.nick_name')


class OrderConfirmationButton(models.Model):
    _inherit = 'product.order'

    def confirm_order(self):
        self.action_confirm()
        return True
    
    def cancel_order(self):
        self.action_cancel()
        return True

    def cancel_order_wizard(self):
        return {
            'name': 'Cancel Order',
            'type': 'ir.actions.act_window',
            'res_model': 'cancel.order.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

# class Order(models.Model):
#     _inherit = 'product.order'

#     def action_confirm(self):
#         res = super(Order, self).action_confirm()
        # for order in self:
        #     template_id = self.env.ref('Online_shopping.send_order_confirmation')
        #     template_id.send_mail(order.id, force_send=True)
        # return res

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    def generate_report(self):
        if len(self.ids) < 1:
            data = self.env["hr.expense"].search([])
            action = self.env.ref('Online_shopping.action_report_hr_expense').with_context(report = True, order_lines = data).report_action(data)
            return action
        else:
            action = self.env.ref('Online_shopping.action_report_hr_expense').with_context(report = True, order_lines = self).report_action(self)
            return action

class ResPartner(models.Model):
    _inherit = 'res.partner'

    commission_amount_on = fields.Float(string='Commission Amount On')
    percentage = fields.Integer(string="Percentage")
    dob = fields.Date(string='Date of Birth')
    is_sundry_customer = fields.Boolean(string='Sundry Customer')

    def action_send_email(self):
        self.ensure_one()
        mail_template = self.env.ref('Online_shopping.mail_res_partner_template_blog')
        ctx = {
            'default_model': 'res.partner',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,

        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch,res = super(ResPartner, self)._get_view(view_id, view_type, **options)
        user1= self.env.user.has_group('Online_shopping.shopping_groups_manager_access')
        print(user1)
        form_nodes = arch.xpath("//form")
        form_forms = arch.xpath("//field")
        list_forms = arch.xpath("//tree")
        kanban_forms = arch.xpath("//tree")
        if view_type == 'form' and (not user1):
            # print("asedrf")
            for node in form_nodes:
                node.set('create', 'false')
                node.set('delete', 'false')
            for form in form_forms:
                form.set('readonly', '1')
        if view_type == 'tree' and (not user1):
            for node in list_forms:
                node.set('create','false')
                node.set('delete','false')
        if view_type == 'kanban' and (not user1):
            for node in kanban_forms:
                node.set('create','false')
                node.set('delete','false')
        return arch,res

        
    # def bday_notification(self):
    #     # for rec in self:
    #     # print("ASDE")
    #     try:
    #         records = self.env['res.partner'].search([('dob','=',fields.Date.today())])

    #         for rec in records:
    #                         email_values = {
    #                             'email_to': rec.email,
    #                             'subject': "Happy Birthday",
    #                             # 'body_html': "<div><p>Wishing you a very happy birthday!</p></div>"
    #                             }
    #         mail_template = self.env.ref('Online_shopping.renew_bday_template')
    #         mail_template.with_context({}).send_mail(rec.id, email_values=email_values, force_send=True)
    #         print("Successfully Send a Email For Bday wishes")
            
    #     except Exception as e:
    #         print(e)

#     class CustomStockQuant(models.Model):
#     _inherit = 'stock.quant'

#     @api.model
#     def _get_available_quantity(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False, allow_negative=False):
#         print("<<<<<<<<<<<<<<<<<<<<_get_available_quantity>>>>>>>>>>>>>")
#         available_quantity = super(CustomStockQuant, self)._get_available_quantity(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=strict, allow_negative=allow_negative)
#         print(available_quantity)
#         if available_quantity <= 0:
#             raise UserError(_('Error: Available quantity is zero!'))

#         return available_quantity

class PosOrder(models.Model):
    _inherit = 'pos.order'

    note = fields.Char(string="Added Note")

    discount = fields.Boolean(string="Discount")

    location = fields.Char(string="Location")


    @api.model
    def _order_fields(self, ui_order):
        result = super(PosOrder, self)._order_fields(ui_order)
        result['note'] = ui_order.get('note', "")
        result['discount'] = ui_order.get('discount')
        result['location'] = ui_order.get('location_added',"")
        return result

    def get_discount(self):
        param_conf = self.env['ir.config_parameter'].sudo()
        discount = param_conf.get_param('discount')
        return float(discount)

    def _get_partner_fields(self):
        fields = super(PosOrder, self)._get_partner_fields()
        fields.append('is_sundry_customer')
        return fields

    def get_location(self):
        loc = self.env['pos.config'].search([])
        results = []
        for i in loc:
            for r in i.location_id:
                results.append(r.location)
        # print(results)
        return results
        
class PosConfig(models.Model):
    _inherit = 'pos.config'

    location_id = fields.Many2many('res.location', string='Locations')

class AccountMove(models.Model):
    _inherit = 'account.move.line'

    image = fields.Image(string="Image", related="product_id.image_1920")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_multiplier = fields.Integer(string = 'Price Multiplier')