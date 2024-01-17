# -*- coding: utf-8 -*-
# from odoo import http


# class Whatsapp(http.Controller):
#     @http.route('/myalice_whatsapp/myalice_whatsapp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/myalice_whatsapp/myalice_whatsapp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('myalice_whatsapp.listing', {
#             'root': '/myalice_whatsapp/myalice_whatsapp',
#             'objects': http.request.env['myalice_whatsapp.myalice_whatsapp'].search([]),
#         })

#     @http.route('/myalice_whatsapp/myalice_whatsapp/objects/<model("myalice_whatsapp.myalice_whatsapp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('myalice_whatsapp.object', {
#             'object': obj
#         })
