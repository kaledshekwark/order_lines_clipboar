{
    'name': 'Sale Line Clipboard',
    'version': '19.0.1.1.0',


    'summary': 'Copy product lines between sale orders, purchase orders and transfers',
    'category': 'Sales',
    'author': 'Khaled Alsheekh warak ',
    'company': 'Ice Code Solutions',
    'website': 'https://www.icecodesolutions.com',

    'depends': ['sale', 'purchase', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/line_clipboard_security.xml',
        'wizard/sale_line_copy_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,

}
