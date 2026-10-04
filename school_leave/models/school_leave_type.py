from odoo import fields, models


class SchoolLeaveType(models.Model):
    _name = 'school.leave.type'
    _description = 'Leave Type'

    name = fields.Char(required=True)
    applicable_to = fields.Selection(
        [
            ('staff', 'Staff'),
            ('student', 'Student'),
            ('both', 'Both'),
        ],
        default='both', required=True,
    )
    max_days_per_year = fields.Integer()
    carry_forward = fields.Boolean()
