from odoo import models, fields, api

class ModuleModelSelector(models.Model):
    _name = 'module.model.selector'
    _description = 'Module and Model Selector'

    selected_module = fields.Many2one('ir.module.module', string='Select Module', domain=[('state', '=', 'installed')])
    selected_model = fields.Many2one('ir.model', string='Select Model')

    @api.onchange('selected_module')
    def _onchange_selected_module(self):
        if self.selected_module:
            models = self.env['ir.model'].search([('model', 'ilike', self.selected_module.name)])
            return {'domain': {'selected_model': [('id', 'in', models.ids)]}}
        else:
            return {'domain': {'selected_model': []}}
