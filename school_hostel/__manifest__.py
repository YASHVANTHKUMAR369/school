{
    'name': 'School Hostel',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Hostel, room and bed allocation',
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': ['school_core', 'school_admission', 'mail'],
    'data': [
        'security/school_hostel_security.xml',
        'security/ir.model.access.csv',
        'views/school_hostel_views.xml',
        'views/school_hostel_allocation_views.xml',
        'views/school_hostel_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
