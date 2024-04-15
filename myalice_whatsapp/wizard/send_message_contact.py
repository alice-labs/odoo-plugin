from odoo import api,fields,models,_
import requests
from odoo.exceptions import UserError, ValidationError
import json
from markupsafe import Markup
import tempfile
import base64


class SendMessageContact(models.TransientModel):
    _name = 'send.message.contact.wizard'
    _description = 'Send Message Contact'

    res_model = fields.Char('Document Model Name')
    wa_template_id = fields.Many2one(comodel_name="get.template.list", string="Template", required=True)
    phone = fields.Char(string='Phone',readonly=False,)
    file = fields.Binary(string='File',attachment=True)
    file_name = fields.Char(string='File Name')
    is_file_available = fields.Boolean(default=False,compute='_is_file_available')
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

    # @api.constrains('file')
    # def _check_file(self):
    #     if str(self.file_name.split(".")[1]) != 'pdf':
    #         raise ValidationError("Cannot upload file different from .pdf file")

    @api.model
    def default_get(self, fields):
        res = super(SendMessageContact, self).default_get(fields)
        context = self.env.context
        active_id = context.get('active_id')
        active_record = self.env['store.temp.message'].search([('partner_id', '=', active_id)], limit=1)
        if active_record:
            res['wa_template_id'] = active_record.wa_template_id.id
            res['phone'] = active_record.phone
            res['free_text_1'] = active_record.free_text_1
            res['free_text_2'] = active_record.free_text_2
            res['free_text_3'] = active_record.free_text_3
            res['free_text_4'] = active_record.free_text_4
            res['free_text_5'] = active_record.free_text_5
            res['free_text_6'] = active_record.free_text_6
            res['free_text_7'] = active_record.free_text_7
            res['free_text_8'] = active_record.free_text_8
            res['free_text_9'] = active_record.free_text_9
            res['free_text_10'] = active_record.free_text_10
        else:
            active_model = context.get('active_model')
            active_record = self.env[active_model].browse(active_id)
            if active_record:
                res['phone'] = active_record.mobile
        return res

    @api.onchange("wa_template_id")
    def _is_file_available(self):
        file = self.wa_template_id.header_type
        if file:
            self.is_file_available = True
        else:
            self.is_file_available = False

    @api.depends(lambda self: self._get_free_text_fields())
    def _compute_preview_whatsapp(self):
        for record in self:
            if record.wa_template_id:
                variable = record.wa_template_id.variables_ids.mapped('attribute')
                body = record.wa_template_id.body
                if len(variable) >0:
                    for i in range(len(variable)):
                        if record[f"free_text_{i+1}"]:
                            key = variable[i]
                            key_with_brackets = "{{" + key + "}}"
                            value = f"<b>{record[f'free_text_{i+1}']}</b>"
                            body = body.replace(key_with_brackets, value)
                    body = Markup(body)
                record.preview_whatsapp = self.env['ir.qweb']._render('myalice_whatsapp.template_message_preview', {

                    'body': body,
                    'buttons': record.wa_template_id.button_ids,
                    'header_type': record.wa_template_id.header_type,
                    'footer_text': record.wa_template_id.footer,
                })
            else:
                record.preview_whatsapp = None
    def _get_free_text_fields(self):
        return ["wa_template_id"] + [f"free_text_{i}" for i in range(1, 11)]


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

    def action_send_whatsapp_template(self):
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
            if variable_keys != [] and variable_values != []:
                if variable_keys == variable_values:
                    raise UserError(_("Please Enter Template Variables"))
                elif len(variable_keys) != len(variable_values):
                    raise UserError(_("Please Enter all the values for the Template Variables"))
                else:
                    attributes = dict(zip(variable_keys, variable_values))

            secret_key = self.env['set.whatsapp.config'].search([('is_active', '=', True)])

            # if self.is_file_available and self.file:
            #     binary_content = self.file
            #     with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
            #         temp.write(base64.b64decode(binary_content))
            #         temp.seek(0)  # reset file pointer to the beginning
            #
            #         document_url = 'https://api.myalice.ai/stable/bots/upload-document'
            #         document_headers = {
            #             'X-Myalice-Api-Key': secret_key.secret_key
            #         }
            #         document_data = {
            #             'file': temp
            #         }
            #         document_response = requests.post(document_url, data=document_data, headers=document_headers)

            if self.file:
                binary_content = self.file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
                    temp.write(base64.b64decode(binary_content))
                    temp_path = temp.name

                with open(temp_path, 'rb') as file:
                    response = requests.post('https://api.myalice.ai/stable/bots/upload-document',
                                                headers={'X-Myalice-Api-Key': secret_key.secret_key},
                                                files={'file': (self.file_name, file, 'application/pdf')})
                    if response.status_code == 200:
                        document_url = response.json()['url']


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
                    }
            if document_url:
                data['document'] = document_url


            response = requests.post(url, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                self.env['store.temp.message'].create({
                    'partner_id': self.env.context.get('active_id'),
                    'wa_template_id': self.wa_template_id.id,
                    'phone': self.phone,
                    'free_text_1': self.free_text_1,
                    'free_text_2': self.free_text_2,
                    'free_text_3': self.free_text_3,
                    'free_text_4': self.free_text_4,
                    'free_text_5': self.free_text_5,
                    'free_text_6': self.free_text_6,
                    'free_text_7': self.free_text_7,
                    'free_text_8': self.free_text_8,
                    'free_text_9': self.free_text_9,
                    'free_text_10': self.free_text_10,
                })
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
        except Exception as e:
            raise ValidationError(_(str(e)))
