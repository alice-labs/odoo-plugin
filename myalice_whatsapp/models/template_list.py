from odoo import models, fields, api


class GetTemplateList(models.Model):
    _name = 'get.template.list'
    _description = 'Get Template List'
    _rec_name = "name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    template_id = fields.Char(string='Template ID',size=200,tracking=True,readonly=True)
    name = fields.Char(string='Name',size=100,tracking=True,readonly=True)
    status = fields.Char(string='Status',size=100,tracking=True,readonly=True)
    body = fields.Text(string='Body',tracking=True,readonly=True)
    platform_id = fields.Integer(string='Channel',tracking=True,)
    footer = fields.Text(string='Footer',tracking=True,readonly=True)

    header_type = fields.Char(string='Header Type',size=100,tracking=True,readonly=True)
    header_value = fields.Char(string='Header Value',size=1000,tracking=True,readonly=True)

    button_ids = fields.One2many(comodel_name='template.buttons',inverse_name='buttons_ids',string='Buttons',tracking=True,readonly=True)
    variables_ids = fields.One2many(comodel_name='template.variables',inverse_name='template_id',string='Variables',tracking=True,readonly=True)


class TemplateButtons(models.Model):
    _name = 'template.buttons'
    _description = 'Template Buttons'

    buttons_id = fields.Integer(string='Buttons ID', tracking=True, readonly=True)
    buttons_type = fields.Char(string='Buttons Type', size=100, tracking=True, readonly=True)
    buttons_title = fields.Char(string='Buttons Title', size=100, tracking=True, readonly=True)
    buttons_value = fields.Char(string='Buttons Value', size=200, tracking=True, readonly=True)
    buttons_verbose = fields.Char(string='Buttons Verbose', size=200, tracking=True, readonly=True)
    buttons_ids = fields.Many2one(comodel_name='get.template.list',string='Template',required=True,tracking=True,ondelete='cascade')


class TemplateVariables(models.Model):
    _name = 'template.variables'
    _description = 'Template Variables'

    attribute = fields.Char(string='Attribute',size=100,tracking=True,readonly=True)
    template_id = fields.Many2one(comodel_name='get.template.list',string='Template',required=True,tracking=True,ondelete='cascade')