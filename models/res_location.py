from odoo import fields, models

class ResLocation(models.Model):
    _name = 'res.location'
    _description = 'This model is show a Different Location in Ahemdabad'
    _rec_name = 'location'
    
    location = fields.Char(string='Location')

    