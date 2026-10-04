{
    'name': 'School Communication',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Notices/circulars and SMS/email dispatch log',
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': ['school_core', 'school_admission', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_notice_views.xml',
        'views/school_sms_provider_config_views.xml',
        'views/school_communication_log_views.xml',
        'views/school_communication_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
