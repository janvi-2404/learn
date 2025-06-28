from odoo import api, fields, models
import xlsxwriter
import base64
from io import BytesIO

class SendSalesReport(models.TransientModel):
    _name = 'send.sales.report'
    _description = 'This is sale report'

    def action_xlsx_report_download(self, salesperson_id, start_date, end_date):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Sales Report')

        # Define styles
        bold_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter', 
            'bg_color': '#ADD8E6', 'border': True, 'text_wrap': True
        })
        header_format = workbook.add_format({
            'bold': True, 'align': 'center', 'font_size': 12, 'valign': 'vcenter', 
            'bg_color': '#ADD8E6', 'font_color': 'black', 'border': True, 'text_wrap': True
        })
        normal_format = workbook.add_format({
            'text_wrap': True, 'align': 'left', 'bg_color': '#E0FFFF', 'valign': 'top', 'border': True
        })
        number_format = workbook.add_format({
            'num_format': '0.00', 'text_wrap': True, 'bg_color': '#E0FFFF', 'align': 'left', 'border': True
        })
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yy', 'align': 'left', 'bg_color': '#E0FFFF', 'valign': 'top', 'border': True
        })
        total_format = workbook.add_format({
            'bold': True, 'bg_color': '#ADD8E6', 'border': True 
        })

        # Set column sizes
        sheet.set_column('A:A', 7)
        sheet.set_column('B:C', 13)
        sheet.set_column('D:E', 15)
        sheet.set_column('F:F', 10)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:K', 12)
        sheet.set_column('N:N', 10)
        sheet.set_column('O:O', 10)
        sheet.set_default_row(20) 
        sheet.set_row(0, 30)

        # Write report header
        report_header = f"Sales Report from {start_date} to {end_date}"
        sheet.merge_range('A1:O1', report_header, header_format)
        sheet.set_row(0, 25)  # Set row height for the header
        sheet.set_row(1, 30)

        # Write headers with bold format
        headers = [
            'Number', 'Order Date', 'Expected date', 'Customer', 'Salesperson', 'Sales Team', 'Company',
            'Untaxed amount', 'Taxes', 'Amount Total', 'Tags', 'Status', 'Delivery status', 'Invoice status',
            'Amount to invoice'
        ]
        for i, header in enumerate(headers):
            sheet.write(1, i, header, bold_format)
        
        sales_orders = self.env['sale.order'].search([
            ('user_id', '=', salesperson_id.id),
            ('date_order', '>=', start_date),
            ('date_order', '<', end_date)
        ])

        row = 2
        for order in sales_orders:
            sheet.write(row, 0, order.name, normal_format)
            sheet.write(row, 1, order.date_order.strftime('%d/%m/%Y'), date_format)
            sheet.write(row, 2, order.expected_date.strftime('%d/%m/%Y') if order.expected_date else '', date_format)
            sheet.write(row, 3, order.partner_id.name, normal_format)
            sheet.write(row, 4, order.user_id.name, normal_format)
            sheet.write(row, 5, order.team_id.name, normal_format)
            sheet.write(row, 6, order.company_id.name, normal_format)
            sheet.write(row, 7, order.amount_untaxed, number_format)
            sheet.write(row, 8, order.amount_tax, number_format)
            sheet.write(row, 9, order.amount_total, number_format)
            sheet.write(row, 10, ', '.join(order.tag_ids.mapped('name')), normal_format)
            sheet.write(row, 11, order.state, normal_format)
            sheet.write(row, 12, order.delivery_status, normal_format)
            sheet.write(row, 13, order.invoice_status, normal_format)
            sheet.write(row, 14, order.amount_to_invoice, number_format)
            row += 1

        workbook.close()
        output.seek(0)
        return output.read()