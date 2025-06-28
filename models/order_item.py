from odoo import models, fields , api , _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class OrderItem(models.Model):
    _name = 'order.item'
    _description = 'Order Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'order_id'

    order_id = fields.Many2one('product.order', string='Order', readonly=True, tracking=True)
    product_id = fields.Many2one('my.product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', tracking=True, default=1.0,
        store=True, readonly=False, required=True)
    price_unit = fields.Monetary(string='Unit Price', related='product_id.price', readonly=True)
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]).id)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for item in self:
            # print(item)
            # print(self)
            item.price_subtotal = item.quantity * item.price_unit

    @api.constrains('quantity')
    def _check_quantity(self):
        for item in self:
            if item.quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Quantity must be positive.'),
    ]