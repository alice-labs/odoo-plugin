from odoo import models, fields, api, _
import requests
from odoo.exceptions import UserError, ValidationError
from odoo import api, exceptions

class Configuration(models.Model):
    _name = 'set.whatsapp.config'
    _description = 'Set Whatsapp Configuration'
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True,tracking=True,size=100)
    secret_key = fields.Char(string='Secret Key', required=True,tracking=True,size=200)
    is_active = fields.Boolean(string='Active', default=False,tracking=True)

    @api.constrains('is_active')
    def _check_unique_secret_key(self):
        msg = 'One Active Configurations is Available named "%s"' % self.name
        envobj = self.env['set.whatsapp.config'].search([('is_active', '=', True)])
        if len(envobj) > 1:
            raise exceptions.ValidationError(msg + " already exists!")

    def get_platform_list(self):
        if not self.is_active == True:
            raise UserError('Please activate whatsapp api config')
        else:
            headers = {
                'X-Myalice-Api-Key': self.secret_key
            }
            platform_url = 'https://api.myalice.ai/stable/open/whatsapp/get-platform-list'
            response = requests.get(platform_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                platform_obj = self.env['get.platform.list']
                platform_obj.search([]).unlink()
                for d in data:
                    platform_id = d['id']
                    platform_obj.create({
                        'platform_id': platform_id,
                        'title': d['title'],
                        'number': d['number'],
                    })
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'sticky': True,
                    'params': {
                        'type': 'success',
                        'message': _("API Connected Successfully"),
                        'next': {'type': 'ir.actions.act_window_close'},
                    }
                }

            else:
                raise UserError('Error in getting platform list')