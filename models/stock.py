from odoo import models, fields, api

class Stock(models.Model):
    _name = 'my.product.stock'
    _description = 'Product stock quantity'

    product_id = fields.Many2one('my.product.product', string='Product', required=True)
    quantity = fields.Integer(string='quantity', required=True)
    stock_value = fields.Float(string='Stock Value', compute="_compute_stock_value", store=True)
    stock_status = fields.Selection([('in_stock', 'In Stock'),('low_stock', 'Low Stock'),('out_of_stock','Out of Stock')],string='Stock Status', compute="_compute_stock_status")

    @api.depends('quantity', 'product_id.price')
    def _compute_stock_value(self):
        for stock in self:
            # print("stock" ,stock)
            # print(self)
            stock.stock_value = stock.quantity * stock.product_id.price

    @api.depends('quantity')
    def _compute_stock_status(self):
        for stock in self:
            if stock.quantity > 10:
                stock.stock_status = 'in_stock'
            elif 1 <= stock.quantity <= 10:
                stock.stock_status = 'low_stock'
            else:
                stock.stock_status = 'out_of_stock'