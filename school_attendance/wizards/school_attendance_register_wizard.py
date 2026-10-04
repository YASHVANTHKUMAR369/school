from odoo import api, fields, models


class SchoolAttendanceRegisterWizard(models.TransientModel):
    _name = 'school.attendance.register.wizard'
    _description = 'Quick Attendance Register'

    section_id = fields.Many2one('school.section', string='Section', required=True)
    date = fields.Date(required=True, default=fields.Date.context_today)
    line_ids = fields.One2many(
        'school.attendance.register.wizard.line', 'wizard_id', string='Students')

    @api.onchange('section_id', 'date')
    def _onchange_section_id(self):
        if not self.section_id:
            self.line_ids = [(5, 0, 0)]
            return
        students = self.env['school.student'].search([
            ('section_id', '=', self.section_id.id), ('state', '=', 'active')])
        existing = self.env['school.student.attendance'].search([
            ('student_id', 'in', students.ids), ('date', '=', self.date)])
        existing_map = {rec.student_id.id: rec.state for rec in existing}
        self.line_ids = [(5, 0, 0)] + [
            (0, 0, {
                'student_id': student.id,
                'state': existing_map.get(student.id, 'present'),
            }) for student in students
        ]

    def action_save(self):
        self.ensure_one()
        Attendance = self.env['school.student.attendance']
        for line in self.line_ids:
            record = Attendance.search([
                ('student_id', '=', line.student_id.id), ('date', '=', self.date)], limit=1)
            vals = {'state': line.state, 'remark': line.remark}
            if record:
                record.write(vals)
            else:
                vals.update({'student_id': line.student_id.id, 'date': self.date})
                Attendance.create(vals)
        return {'type': 'ir.actions.act_window_close'}


class SchoolAttendanceRegisterWizardLine(models.TransientModel):
    _name = 'school.attendance.register.wizard.line'
    _description = 'Quick Attendance Register Line'

    wizard_id = fields.Many2one('school.attendance.register.wizard', required=True, ondelete='cascade')
    student_id = fields.Many2one('school.student', string='Student', required=True)
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
