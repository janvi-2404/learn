from odoo import models, fields, api

class Commission(models.Model):
    _name = 'commission'
    _description = 'Commission'

    sales_person_id = fields.Many2one('res.users', string='Sales Person')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    sale_order_ids = fields.Many2many('commission.on.line', string='Sale Orders')

    total_commission = fields.Float(string='Total Commission', compute='_compute_total_amount')
    total_amount = fields.Float(string='Total Amount' , compute='_compute_total_amount')

    @api.depends('sale_order_ids.commission', 'sale_order_ids.total')
    def _compute_total_amount(self):
        for record in self:
            record.total_commission = sum(order.commission for order in record.sale_order_ids)
            record.total_amount = sum(order.total for order in record.sale_order_ids)

    # @api.onchange('sales_person_id', 'start_date', 'end_date')
    # def _onchange_sales_person_id(self):
    #     self.sale_order_ids = False  # Reset sale order ids
    #     if self.sales_person_id and self.start_date and self.end_date:
    #         orders = self.env['sale.order'].search([
    #             ('user_id', '=', self.sales_person_id.id),
    #             ('date_order', '>=', self.start_date),
    #             ('date_order', '<=', self.end_date)
    #         ])
    #         self.sale_order_ids = [(6, 0, orders.ids)]

    # @api.depends('sale_order_ids')
    # def _compute_total_commission(self):
    #     for commission in self:
    #         total = sum(commission.sale_order_ids.mapped('amount_total'))
    #         commission.total_commission = total * 0.05
            # commission.total_commission = total

    # @api.depends('sales_person_id', 'start_date', 'end_date')
    def _compute_sale_orders(self):
        for commission in self:
            if commission.sales_person_id and commission.start_date and commission.end_date:
                orders = self.env['commission.on.line'].search([
                    ('customer_name', '=', commission.sales_person_id.name),
                    ('order_date', '>=', commission.start_date),
                    ('order_date', '<=', commission.end_date)
                ])
                commission.sale_order_ids = [(6, 0, orders.ids)]
            else:
                commission.sale_order_ids = False

    def compute_commission_totals(self):
        self._compute_sale_orders()

