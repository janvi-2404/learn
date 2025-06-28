from odoo import models, fields, api

class SaleReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'
    _description = 'This is report Wizard'

    order_id = fields.Many2one('sale.order', string='Sale Order')
    sale_order_line_ids = fields.Many2many('sale.order.line', string='Sale Order Lines')

    # @api.onchange('order_id')
    # def _onchange_order_id(self):
    #     if self.order_id:
    #         self.sale_order_line_ids = self.order_id.order_line.ids

    def confirm_generate_report(self):
        # selected_product_ids = self.sale_order_line_ids.ids
        # sale_order_lines = self.env['sale.order.line'].browse(selected_product_ids)
        report_data = {
            'order_id': self.order_id.id,
            'sale_order_line_ids': [(6, 0, self.sale_order_line_ids.ids)]
        }
        return self.env.ref('Online_shopping.sale_order_report_my').report_action(self, data=report_data)


    def report(self):
        # print(" selected order line <", self.sale_order_line_ids)
        order_line = self.sale_order_line_ids.mapped('id')
        # print(" selected order line", order_line)
        action = self.env.ref('Online_shopping.report_sale_order_document_my').with_context(my_report = True, order_lines = order_line).report_action(self.order_id)
        # print(action)
        return action

        # def generate_report(self, report_data):
        # report_obj = self.env['your.report.model']
        # report = report_obj.create(report_data)
        # report_action = self.env.ref('.action_report_name').report_action(report)
        # return report_action