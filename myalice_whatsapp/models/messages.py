from odoo import models, fields, api


class WhatsappMessages(models.Model):
    _name = 'whatsapp.sent.messages'
    _description = 'Whatsapp Messages'
    _rec_name = "customer_phone"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    status = fields.Selection([('draft', 'Draft'), ('sent', 'Sent'), ('failed', 'Failed')], string='Status', default='draft')
    customer_phone = fields.Char(string='Customer Phone', required=True, tracking=True, size=20)
    template_id = fields.Many2one(comodel_name='get.template.list',
                                  string='Template',
                                  required=True,
                                  tracking=True,ondelete='cascade')
    platform_id = fields.Many2one(comodel_name='get.platform.list',
                                  string='Platform',
                                  required=True,
                                  tracking=True,)


    # def send_whatsapp_message(self):
    #     pass
        # for rec in self:
        #     headers = {
        #         rec.whatsapp_api_config_id.headers_key: rec.whatsapp_api_config_id.headers_token
        #     }
        #     url = rec.whatsapp_api_config_id.api_url
        #     print(rec.customer_phone)
        #     print(rec.template_id.template_id)
        #     print(rec.platform_id.platform_id)
        #     data = {
        #         "customer_phone": rec.customer_phone,
        #         "template_id": rec.template_id.template_id,
        #         "channel_id": rec.platform_id.platform_id,
        #         # "attributes": {"form_id":"Hello"},
        #         # "attachment": {}
        #     }
        #     json_object = json.dumps(data)
        #     print(json_object)
        #     response = requests.post(url, headers=headers, data=json_object)
        #     print(response)
        #     if response.status_code == 200:
        #         data = response.json()
        #         if data['status'] == 'finished':
        #             rec.status = 'sent'
        #         else:
        #             rec.status = 'failed'
        #     else:
        #         raise UserError('Error in sending message')

