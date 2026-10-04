{
    'name': 'School Leave',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Staff and student leave requests',
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': ['school_core', 'school_admission', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/school_leave_type_data.xml',
        'views/school_leave_type_views.xml',
        'views/school_leave_request_views.xml',
        'views/school_leave_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
