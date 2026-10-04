from odoo import fields, models


class SchoolStudentAttendance(models.Model):
    _name = 'school.student.attendance'
    _description = 'Student Attendance'
    _order = 'date desc'

    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    section_id = fields.Many2one(related='student_id.section_id', store=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    state = fields.Selection(
        [
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('late', 'Late'),
            ('half_day', 'Half Day'),
            ('leave', 'On Leave'),
        ],
        default='present', required=True,
    )
    remark = fields.Char()
    marked_by = fields.Many2one('school.staff', string='Marked By')

    _student_date_uniq = models.Constraint(
        'UNIQUE (student_id, date)', 'Attendance for this student on this date is already recorded.')
