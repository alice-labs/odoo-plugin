from odoo import models, fields, api,_
import requests
from odoo.exceptions import UserError, ValidationError

class GetPlatformList(models.Model):
    _name = 'get.platform.list'
    _description = 'Get Platform List'
    _rec_name = "title"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    platform_id = fields.Integer(string='Platform ID', readonly=True,tracking=True)
    title = fields.Char(string='Title',readonly=True,size=100)
    number = fields.Char(string='Number',readonly=True,size=20)

    def get_template_list(self):
        whatsapp_config_obj = self.env['set.whatsapp.config'].sudo().search([('is_active', '=', True)])
        if whatsapp_config_obj:
            api_secret_key = whatsapp_config_obj.secret_key
            headers = {
                'X-Myalice-Api-Key': api_secret_key
            }
            template_url = 'https://api.myalice.ai/stable/open/whatsapp/get-template-list'
            url= template_url+"?"+"platform_id="+str(self.platform_id)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                template_obj = self.env['get.template.list']

                for d in data:
                    if d['status'] == 'approved':
                        buttons_obj = d['buttons']
                        variables_obj = d['attributes']
                        headers_obj = d['header']
                        template_obj.search([('template_id', '=', d['id'])]).unlink()
                        template = template_obj.sudo().create({
                            'template_id': d['id'],
                            'name': d['name'],
                            'status': d['status'],
                            'body': d['body'],
                            'footer': d['footer'],
                            'platform_id': int(self.platform_id),

                        })
                        try:
                            header_type = headers_obj['type']
                        except:
                            header_type = ''
                        try:
                            header_value = headers_obj['value']
                        except:
                            header_value = ''
                        template.write({
                            'header_type': header_type or None,
                            'header_value': header_value or None,
                        })

                        for b in buttons_obj:
                            try:
                                verbose = b['verbose']
                            except:
                                verbose = ''
                            template.write({
                                'button_ids': [(0, 0, {
                                    'buttons_id': b['id'] or None,
                                    'buttons_type': b['type'] or None,
                                    'buttons_title': b['title'] or None,
                                    'buttons_value': b['value'] or None,
                                    'buttons_verbose': verbose or None,
                                })],
                            })

                        for v in variables_obj:
                            template.write({
                                'variables_ids': [(0, 0, {
                                    'attribute': v['attribute'] or None,
                                })],
                            })
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'sticky': True,
                    'params': {
                        'type': 'success',
                        'message': _("Templated Created Successfully"),
                        'next': {'type': 'ir.actions.act_window_close'},
                    }
                }

            else:
                raise UserError('Error in getting template list')
