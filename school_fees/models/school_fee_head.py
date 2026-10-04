from odoo import fields, models


class SchoolFeeHead(models.Model):
    _name = 'school.fee.head'
    _description = 'Fee Head'

    name = fields.Char(required=True, help='E.g. Tuition, Admission, Transport, Hostel, Exam, Library, Lab, Activity')
    code = fields.Char()
    is_recurring = fields.Selection(
        [
            ('one_time', 'One Time'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('annual', 'Annual'),
        ],
        default='annual', required=True,
    )
