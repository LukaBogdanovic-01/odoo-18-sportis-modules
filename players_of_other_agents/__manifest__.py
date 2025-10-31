{
    'name': 'Players of Other Agents',
    'version': '18.0.1.0.0',
    'summary': 'Players managed by other agents',
    'category': 'Recruitment',
    'author': 'Luka',
    'depends': ['base', 'crm','sportis_crm'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'data/pota_kanban_stage_data.xml',
        'views/pota_form.xml',
        'views/code_books_view.xml',
        'views/pota_menu.xml',
    ],
    'installable': True,
    'application': False,
}
