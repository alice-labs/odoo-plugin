# -*- coding: utf-8 -*-
{
    'name': "WhatsApp with MyAlice",
    'version': '1.0',
    'summary': """
        MyAlice Whatsapp Integration With Odoo
        """,
    'sequence': 1,
    'description': """
        Introducing our latest innovation on the Odoo Marketplace: 
        the WhatsApp Connector for Odoo! Seamlessly integrate your WhatsApp numbers from MyAlice directly into your Odoo environment, revolutionizing the way you communicate with your contacts. 
        This powerful app simplifies and enhances your messaging experience, providing you with a range of features to streamline your communication processes.
    """,
    'category': 'Tools',
    'author': "MyAlice",
    'website': "https://www.myalice.ai/",
    # any module necessary for this one to work correctly
    'depends': ['base','mail','account'],

    # always loaded
    'data': [
        'security/whatsapp_security.xml',
        'security/ir.model.access.csv',
        'views/get_platform_list_views.xml',
        'views/get_template_list_views.xml',
        'views/set_whatsapp_config_views.xml',
        'views/messages_views.xml',

        'wizard/send_message_contact.xml',
        'views/send_message_contacts_view.xml',
        'wizard/send_message_invoicing.xml',
        'views/send_message_invoicing_view.xml',
        'views/menuitem_views.xml',
    ],
    "images": ["static/description/banner.JPG"],

    'application': True,
    'installable': True,
}
