from odoo import http
from odoo.http import request

class Main(http.Controller):

    @http.route('/shopping/hello', type='http', auth='public', website=True)
    def hello(self, **kwargs):
        customers = request.env['sale.order'].search([])
        return request.render("Online_shopping.sale_order",{
            'sale_data': customers
        })