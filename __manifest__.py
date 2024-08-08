# -*- coding: utf-8 -*-

{
    'name': 'Migo Payment Acquirer',
    'category': 'Accounting/Payment Acquirers',
    'summary': 'Payment Acquirer: Migo Implementation',
    'version': '2.0',
    'description': """Migo Payment Acquirer""",
    'author': 'aquíH',
    'website': 'http://aquih.com/',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_migo_templates.xml',
        'data/payment_provider_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'uninstall_hook': 'uninstall_hook',
    'license': 'Other OSI approved licence',
}
