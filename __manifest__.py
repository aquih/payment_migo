# -*- coding: utf-8 -*-

{
    'name': 'Migo Payment Provider',
    'category': 'Accounting/Payment Providers',
    'summary': 'Payment Provider: Migo Implementation',
    'version': '2.1',
    'description': """Migo Payment Provider""",
    'author': 'aquíH',
    'website': 'http://aquih.com/',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_migo_templates.xml',
        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',
    ],
    'images': ['static/description/icon.png'],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'Other OSI approved licence',
}
