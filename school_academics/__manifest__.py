{
    'name': 'School Academics',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Timetable, syllabus tracking and homework',
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': ['school_core', 'school_admission', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_timetable_slot_views.xml',
        'views/school_syllabus_topic_views.xml',
        'views/school_homework_views.xml',
        'views/school_academics_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
