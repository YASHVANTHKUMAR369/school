{
    'name': 'School Attendance',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Daily student and staff attendance',
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': ['school_core', 'school_admission', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_student_attendance_views.xml',
        'views/school_staff_attendance_views.xml',
        'wizards/school_attendance_register_wizard_views.xml',
        'views/school_attendance_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
