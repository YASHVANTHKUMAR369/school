{
    'name': 'School Core',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Core masters for the Indian School Management System',
    'description': """
School Core
===========
Foundational master data for the School Management suite:
academic years, boards, standards, sections, subjects, staff & guardian
masters, school letterhead configuration and shared security groups.
""",
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/school_board_data.xml',
        'views/school_academic_year_views.xml',
        'views/school_board_views.xml',
        'views/school_standard_views.xml',
        'views/school_section_views.xml',
        'views/school_subject_views.xml',
        'views/school_staff_views.xml',
        'views/school_guardian_views.xml',
        'views/school_config_views.xml',
        'views/school_core_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
