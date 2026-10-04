{
    'name': 'School Portal',
    'version': '19.0.1.0.0',
    'category': 'School Management',
    'summary': 'Guardian/parent portal: attendance, homework, exam results, fees, library, transport, notices',
    'author': 'Yashvanth Kumar',
    'license': 'LGPL-3',
    'depends': [
        'portal', 'mail',
        'school_core', 'school_admission', 'school_academics', 'school_attendance',
        'school_exam', 'school_fees', 'school_transport', 'school_hostel',
        'school_library', 'school_communication',
    ],
    'data': [
        'security/school_portal_security.xml',
        'security/ir.model.access.csv',
        'wizards/school_portal_grant_wizard_views.xml',
        'views/school_guardian_views.xml',
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
