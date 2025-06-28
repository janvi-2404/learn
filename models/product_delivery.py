from odoo import models, fields, api
class ProductDelivery(models.Model):
    _name = 'product.delivery.me'
    _description = "This is a product delivery information."

    deliveryId = fields.Char(string="Delivery Id" , copy=False , readonly=True )
    order_id = fields.Many2one("product.order",string="Order_id" )
    customer_id = fields.Many2one("my.customer.customer",string="Customer")
    delivery_date = fields.Date(string="Expected delivery date")
    payment = fields.Selection([
        ("unpaid", "Unpaid"),
        ("paid", "Paid")
    ], string="Payment Status")

    state = fields.Selection([('ordered', 'Ordered'), ('delivered', 'Delivered'), ('Cancel', 'Cancel')], string="Status")

    def create(self, vals):
        vals['deliveryId'] = self.env['ir.sequence'].sudo().next_by_code('product.delivery.me') or 'New'
        res = super(ProductDelivery,self).create(vals)
        return res
    
    def write(self, vals):
        res = super(ProductDelivery, self).write(vals)
        for delivery in self:
            if 'state' in vals and vals['state'] == 'delivered':
                order = delivery.order_id
                if order and order.state == 'confirmed':
                    order.action_done_success()
                    if delivery.payment == 'unpaid':
                        delivery.write({'payment' : 'paid'})
        return res
