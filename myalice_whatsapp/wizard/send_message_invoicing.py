from odoo import api,fields,models,_
import requests
from odoo.exceptions import UserError, ValidationError
import json


class SendMessageContact(models.TransientModel):
    _name = 'send.message.invoicing.wizard'
    _description = 'Send Message Invoice'

    res_model = fields.Char('Document Model Name')
    wa_template_id = fields.Many2one(comodel_name="get.template.list", string="Template", required=True)
    phone = fields.Char(string='Phone',readonly=False,compute='_default_phone')
    variables_available = fields.Boolean(compute="_compute_variables_available")
    variable_keys = fields.Char(string='Template Variables', readonly=True)
    variable_values = fields.Char(string='Values', readonly=False,required=True)

    preview_whatsapp = fields.Html(compute="_compute_preview_whatsapp", string="Message Preview")

    @api.depends('wa_template_id')
    def _compute_variables_available(self):
        try:
            if self.wa_template_id.variables_ids:
                self.variables_available = True
                self.variable_keys = self.wa_template_id.variables_ids.attribute
            else:
                self.variables_available = False
        except:
            self.variables_available = False

    @api.depends('wa_template_id')
    def _default_phone(self):
        context = self.env.context
        active_id = context.get('active_id')
        active_model = context.get('active_model')
        active_record = self.env[active_model].browse(active_id)
        if active_record:
            self.phone = active_record.partner_id.phone
        else:
            self.phone = ''

    @api.onchange('wa_template_id')
    def _onchange_wa_template_id(self):
        self.ensure_one()
        if self.wa_template_id:
            template_obj = self.env['get.template.list'].search([('id', '=', self.wa_template_id.id)])
            if template_obj.variables_ids:
                for v in template_obj.variables_ids:
                    if v.attribute == 'phone':
                        v.attribute = self.phone

    def action_send_whatsapp_invoicing(self):
        self.ensure_one()
        if not self.phone:
            raise UserError(_("Please Enter Phone Number"))
        else:
            if self.phone[0] != '+':
                raise UserError(_("Please Enter Phone Number with country code"))

        if not self.wa_template_id:
            raise UserError(_("Please Select Template"))

        customer_phone = self.phone
        wa_template_id = self.wa_template_id

        secret_key = self.env['set.whatsapp.config'].search([('is_active', '=', True)])

        url = 'https://api.myalice.ai/stable/open/whatsapp/send-template-message'
        template_id = wa_template_id.template_id
        channel_id = wa_template_id.platform_id

        headers = {
            'X-Myalice-Api-Key': secret_key.secret_key
        }
        try:
            attribute_obj = self.wa_template_id.variables_ids.attribute
            attributes = {
                attribute_obj: self.variable_values
            }
        except:
            attributes = ''
        data = {'template_id': template_id,
                'channel_id': channel_id,
                'customer_phone': customer_phone,
                'attributes':attributes,}

        response = requests.post(url, data=json.dumps(data),headers=headers)
        if response.status_code == 200:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'sticky': True,
                'params': {
                    'type': 'success',
                    'message': _("Message Sent Successfully"),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        else:
            raise UserError(_("Message Not Sent"))