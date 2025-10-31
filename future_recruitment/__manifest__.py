{
    'name': 'Future Recruitment',
    'version': '18.0.1.0.0',
    'summary': 'Custom recruitment module for Sportis project',
    'category': 'Human Resources',
    'author': 'Luka',
    'depends': ['base', 'mail', 'sportis_crm'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'data/rec_kanban_stage_data.xml',
        'views/recruitment_form_view.xml',
        'views/code_books_view.xml',
        'views/recruitment_menu.xml',
    ],
    'installable': True,
    'application': False,

}
