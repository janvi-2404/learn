from odoo import fields, models, api, _
from odoo.exceptions import UserError

class CancelOrderWizard(models.TransientModel):
    _name = 'cancel.order.wizard'
    _description = "This is a notification before removing orders."

    password = fields.Char(string='Password')

    def cancel_order(self):
        expected_password = "janvi"  
        if self.password == expected_password:
            active_ids = self.env.context.get('active_ids')
            orders = self.env['product.order'].browse(active_ids)
            orders.action_cancel()  
            orders.write({'state': 'cancel'})
            return {'type': 'ir.actions.act_window_close'}
        else:
            raise UserError('Incorrect password! Please try again.')
            # return {
            #     'type': 'ir.actions.act_window',
            #     'res_model': 'cancel.order.wizard',
            #     'view_mode': 'form',
            #     'target': 'new',
            #     'context': {'default_password': _('Incorrect password! Please try again.')},
            # }