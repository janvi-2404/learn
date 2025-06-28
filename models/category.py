from odoo import models, fields

class Category(models.Model):
    _name = 'product.category.me'
    _description = 'Category'

    name = fields.Char(string='Name', required=True)





