from odoo import api, fields, models


class SchoolStaffAttendance(models.Model):
    _name = 'school.staff.attendance'
    _description = 'Staff Attendance'
    _order = 'date desc'

    staff_id = fields.Many2one('school.staff', string='Staff', required=True, ondelete='cascade')
    date = fields.Date(required=True, default=fields.Date.context_today)
    check_in = fields.Datetime()
    check_out = fields.Datetime()
    state = fields.Selection(
        [
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('half_day', 'Half Day'),
            ('on_leave', 'On Leave'),
        ],
        default='present', required=True,
    )
    worked_hours = fields.Float(compute='_compute_worked_hours', store=True)

    _staff_date_uniq = models.Constraint(
        'UNIQUE (staff_id, date)', 'Attendance for this staff member on this date is already recorded.')

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                rec.worked_hours = (rec.check_out - rec.check_in).total_seconds() / 3600.0
            else:
                rec.worked_hours = 0.0
