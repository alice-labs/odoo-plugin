from odoo import models, fields, api,_

class StoreTempMessage(models.Model):
    _name = 'store.temp.message'
    _description = 'Store Temp Message'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
    wa_template_id = fields.Many2one(comodel_name="get.template.list", string="Template", required=True)
    phone = fields.Char(string='Phone',readonly=False,)
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