from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    discount = fields.Integer(string="Dicount", config_parameter = 'discount')
    location_id = fields.Many2many(
        string='Locations',
        related='pos_config_id.location_id',
        readonly=False
    )
    enable_shopping = fields.Boolean(string="Enable Orders",
                            help="Enable if you want to order from pos")

    sale_limit = fields.Float(string='Sales Limit', config_parameter = 'sale_limit')