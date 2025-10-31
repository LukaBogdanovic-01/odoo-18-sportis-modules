{
    'name': 'Sportis CRM',
    'version': '18.0.1.0.0',
    'summary': 'Custom CRM enhancements for Sportis project',
    'category': 'Sales/CRM',
    'author': 'Luka',
    'depends': ['crm', 'base', 'sales_team', 'project_todo', 'mail', 'contacts', 'calendar', 'project', 'mass_mailing', 'account', 'spreadsheet_dashboard', 'website'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/crm_stage_view.xml', 
        'views/contact_form_view.xml',
        'views/code_books_view.xml',
        'views/contact_menu_view.xml',
        'views/crm_menu_view.xml',
    ],
        'assets': {
        'web.assets_backend': [
            'sportis_crm/static/src/css/styles.css',
        ],
    },
    'installable': True,
    'application': False,
}
