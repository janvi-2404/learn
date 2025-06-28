from odoo import http
from odoo.http import request
import json

class SaleOrderController(http.Controller):

    @http.route('/create_sale_order', type='json', auth='public', method=['POST'], csrf=False)
    def create_sale_order(self, **kwargs):
        order_data = json.loads(request.httprequest.data)
        # print("order_data>>>>>>>>>>>", order_data)

        partner_id = order_data.get('partner_id')
        user_id = order_data.get('user_id')
        order_lines = order_data.get('order_lines', [])

        if not partner_id or not user_id or not order_lines:
            return {'status': 'error', 'message': 'Missing required fields'}

        sale_order = request.env['sale.order'].sudo().create({
            'partner_id': partner_id,
            'user_id': user_id,
            'order_line': [(0, 0, {
                'product_id': line['product_id'],
                'product_uom_qty': line['product_uom_qty'],
                'price_unit': line['price_unit'],
            }) for line in order_lines]
        })

        return {'status': 'success', 'sale_order_id': sale_order.id}

    @http.route('/website/form/mail.mail', type='json', auth='public', method=['POST'], website=True)
    def create_email(self, **kwargs):
        values = json.loads(request.httprequest.data)
        val = values.get('data_value')
        if values:
            mail_mail = request.env['mail.mail'].sudo().create(val)
            if mail_mail:
                mail_mail.send()
            return {'status': 'success', 'message': 'Email created successfully'}
        return {'status': 'error', 'message': 'Missing values'}