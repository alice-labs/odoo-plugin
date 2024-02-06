from odoo import api, fields, models, _
import requests
from odoo.exceptions import UserError, ValidationError
import json
import re
from lxml import etree


class SendMessageInvoicing(models.TransientModel):
    _name = 'send.message.invoicing.wizard'
    _description = 'Send Message Invoice'

    res_model = fields.Char('Document Model Name')
    wa_template_id = fields.Many2one(comodel_name="get.template.list", string="Template", required=True)
    phone = fields.Char(string='Phone',readonly=False,compute='_default_phone')
    free_text_1 = fields.Char(string="Free Text 1", )
    free_text_2 = fields.Char(string="Free Text 2", )
    free_text_3 = fields.Char(string="Free Text 3", )
    free_text_4 = fields.Char(string="Free Text 4", )
    free_text_5 = fields.Char(string="Free Text 5", )
    free_text_6 = fields.Char(string="Free Text 6", )
    free_text_7 = fields.Char(string="Free Text 7", )
    free_text_8 = fields.Char(string="Free Text 8", )
    free_text_9 = fields.Char(string="Free Text 9", )
    free_text_10 = fields.Char(string="Free Text 10", )

    preview_whatsapp = fields.Html(compute="_compute_preview_whatsapp", string="Message Preview")



    @api.depends('wa_template_id')
    def _default_phone(self):
        context = self.env.context
        active_id = context.get('active_id')
        active_model = context.get('active_model')
        active_record = self.env[active_model].browse(active_id)
        if active_record:
            self.phone = active_record.partner_id.mobile
        else:
            self.phone = ''

    @api.onchange('wa_template_id')
    def _compute_free_text(self):
        self.free_text_1 = False
        self.free_text_2 = False
        self.free_text_3 = False
        self.free_text_4 = False
        self.free_text_5 = False
        self.free_text_6 = False
        self.free_text_7 = False
        self.free_text_8 = False
        self.free_text_9 = False
        self.free_text_10 = False
        attribute = self.wa_template_id.variables_ids.mapped('attribute')
        free_text_count = 1
        if attribute:
            for param in attribute:
                self[f"free_text_{free_text_count}"] = param
                free_text_count += 1

    def action_send_whatsapp_invoicing(self):
        # Validation
        self.ensure_one()
        if not self.phone:
            raise UserError(_("Please Enter Phone Number"))
        else:
            if self.phone[0] != '+':
                raise UserError(_("Please Enter Phone Number with country code"))
        if not self.wa_template_id:
            raise UserError(_("Please Select Template"))

        # Concatenate Template Variables and Values
        try:
            variable_keys = self.wa_template_id.variables_ids.mapped('attribute')
            variable_list = [self.free_text_1, self.free_text_2, self.free_text_3, self.free_text_4, self.free_text_5,
                             self.free_text_6, self.free_text_7, self.free_text_8, self.free_text_9, self.free_text_10]
            variable_values = [x for x in variable_list if x]
            attributes = {}
            attachment = {}
            if variable_keys !=[] and variable_values !=[]:
                if variable_keys == variable_values:
                    raise UserError(_("Please Enter Template Variables"))
                elif len(variable_keys) != len(variable_values):
                    raise UserError(_("Please Enter all the values for the Template Variables"))
                else:
                    attributes = dict(zip(variable_keys, variable_values))

            # Get Invoice PDF Data
            if self.wa_template_id.header_type == 'document':
                context = self.env.context
                active_id = context.get('active_id')
                active_model = context.get('active_model')
                active_record = self.env[active_model].browse(active_id)
                server_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                invoice_public_url = server_url + active_record.get_portal_url()
                attachment = {
                    'document': invoice_public_url
                }

            secret_key = self.env['set.whatsapp.config'].search([('is_active', '=', True)])

            url = 'https://api.myalice.ai/stable/open/whatsapp/send-template-message'
            template_id = self.wa_template_id.template_id
            channel_id = self.wa_template_id.platform_id

            headers = {
                'X-Myalice-Api-Key': secret_key.secret_key
            }

            data = {'template_id': template_id,
                    'channel_id': channel_id,
                    'customer_phone': self.phone,
                    'attributes': attributes,
                    'attachment': attachment,}

            response = requests.post(url, data=json.dumps(data), headers=headers)
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
        except Exception:
            raise ValidationError(_("Something went wrong. Please contact MyAlice."))