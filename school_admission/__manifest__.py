{
    'name': 'School Admission',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Enquiry to admission workflow and the student register',
    'description': """
School Admission
=================
Enquiry -> Application -> Interview -> Admission workflow.
Defines the central school.student register used by the whole suite.
""",
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': ['school_core', 'mail'],
    'data': [
        'security/school_admission_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/school_admission_enquiry_views.xml',
        'views/school_admission_application_views.xml',
        'views/school_student_views.xml',
        'views/school_guardian_views.xml',
        'views/school_admission_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
