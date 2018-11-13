# -*- coding: utf-8 -*-

{
    'name' : 'Delivery And Invoice Report',
    'version' : '11.0.0.1',
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'category': 'Report',
    'website': 'http://www.caretit.com',
    'description' : 'Generate Delivery Note Report & Invoice Report',
    'depends' : ['product','purchase','sale_stock', 'account'],
    'data' : [
		'views/stock_picking_view.xml',
        'report/delivery_note_report_view.xml',
        'report/invoice_report_view.xml',
        'report/custom_layouts_hf.xml',
 		'report_menu.xml',
 	],
    'demo' : [
    ],
    'installable': True,
}

