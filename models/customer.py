from odoo import models, fields, api, tools, _
from odoo.exceptions import ValidationError
from datetime import datetime
import uuid

class Customer(models.Model):
    _name = 'my.customer.customer'
    _description = 'Customer'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    address = fields.Text(string='Address')
    customerID = fields.Char(string='Customer Id', readonly=True, copy=False)
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count')
    order_ids = fields.One2many('product.order', 'customer_id', string='Orders')
    dob = fields.Date(string='Date of Birth')

    @api.depends('order_ids')
    def _compute_order_count(self):
        for rec in self:
            rec.order_count = len(rec.order_ids)

    def create(self, vals):
        # print(vals)
        if vals.get('customerID', _('New')) == _('New'):
            vals['customerID'] = self._generate_customerID()
            # print(vals['name'])
        return super(Customer, self).create(vals)
    
    def _generate_customerID(self):
        # Generate a random UUID
        return str(uuid.uuid4())

    @api.constrains('customerID')
    def _check_unique_customerID(self):
        # print(self)
        for record in self:
            if record.customerID:
                existing_record = self.search([('customerID', '=', record.customerID)])
                if len(existing_record) > 1:
                    raise ValidationError("User ID must be unique.")

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if record.name:
                existing_record = self.search([('name', '=', record.name)])
                if len(existing_record) > 1:
                    raise ValidationError("User alredy exist.")

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        user_groups = self.env.user.groups_id
        target_group = self.env.ref('Online_shopping.shopping_groups_manager_access')
        if view_type == 'form' and target_group in user_groups:
            for node in arch.xpath("//field[@name='email']"):
                node.set('readonly', '1')
            print("user_groups",user_groups)
            print("target_group",target_group)

        return arch, view

    def action_order_list(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orders',
            'res_model': 'product.order',
            'view_mode': 'form',
            'target':'new',
            'domain': [('customer_id', '=', self.id)]
        }

    @api.model
    def bday_notification(self):
        try:
            today = datetime.now().date()
            records = self.env['my.customer.customer'].search([
                ('dob', '!=', False),  
                ('dob', 'like', f"%-{today.month:02d}-{today.day:02d}"),
            ])

            for rec in records:
                email_values = {
                    'email_to': rec.email,
                    'subject': "Happy Birthday"
                }
                mail_template = self.env.ref('Online_shopping.renew_bday_template')
                mail_template.with_context({}).send_mail(rec.id, email_values=email_values, force_send=True)
                # print("Successfully Sent an Email For Birthday wishes")
                
        except Exception as e:
            print(e)


