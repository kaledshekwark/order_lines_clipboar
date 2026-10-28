{
    'name': 'Line Clipboard',
    'version': '19.0.1.2.0',
    'summary': 'Copy product lines between sale orders, purchase orders, transfers and invoices',
    'category': 'Sales',
    'author': 'Khaled Alsheekh warak ',
    'company': 'Ice Code Solutions',
    'website': 'https://www.icecodesolutions.com',
    'depends': ['sale', 'purchase', 'stock', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'security/line_clipboard_security.xml',
        'wizard/sale_line_copy_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,


}
