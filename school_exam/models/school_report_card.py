from odoo import api, fields, models


class SchoolReportCard(models.Model):
    _name = 'school.report.card'
    _description = 'Report Card'
    _order = 'exam_id, student_id'

    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    exam_id = fields.Many2one('school.exam', string='Exam', required=True, ondelete='cascade')
    total_max_marks = fields.Float()
    total_marks_obtained = fields.Float()
    percentage = fields.Float(compute='_compute_percentage', store=True)
    overall_grade = fields.Char()
    rank_in_section = fields.Integer()
    attendance_percentage = fields.Float()
    state = fields.Selection(
        [('draft', 'Draft'), ('published', 'Published')], default='draft', required=True)

    _student_exam_uniq = models.Constraint(
        'UNIQUE (student_id, exam_id)', 'A report card for this student and exam already exists.')

    @api.depends('total_marks_obtained', 'total_max_marks')
    def _compute_percentage(self):
        for rec in self:
            rec.percentage = (rec.total_marks_obtained / rec.total_max_marks * 100.0) if rec.total_max_marks else 0.0

    @api.model
    def generate_for_exam(self, exam):
        students = self.env['school.student'].search([
            ('standard_id', '=', exam.standard_id.id),
            ('section_id', 'in', exam.section_ids.ids),
            ('state', '=', 'active'),
        ])
        # Try to enrich the report card with an attendance percentage, but
        # school_exam must stay installable without school_attendance.
        Attendance = self.env.get('school.student.attendance')

        cards = self.env['school.report.card']
        for student in students:
            results = exam.result_ids.filtered(lambda r: r.student_id == student)
            total_max = sum(results.mapped('max_marks'))
            total_obtained = sum(results.mapped('marks_obtained'))
            percentage = (total_obtained / total_max * 100.0) if total_max else 0.0
            grade_line = exam.grade_scale_id.get_grade(percentage) if exam.grade_scale_id else False

            attendance_pct = 0.0
            if Attendance is not None:
                total_days = Attendance.search_count([
                    ('student_id', '=', student.id),
                    ('date', '>=', exam.academic_year_id.date_start),
                    ('date', '<=', exam.date_to),
                ])
                present_days = Attendance.search_count([
                    ('student_id', '=', student.id),
                    ('date', '>=', exam.academic_year_id.date_start),
                    ('date', '<=', exam.date_to),
                    ('state', 'in', ('present', 'late', 'half_day')),
                ])
                attendance_pct = (present_days / total_days * 100.0) if total_days else 0.0

            card = self.search([('student_id', '=', student.id), ('exam_id', '=', exam.id)], limit=1)
            vals = {
                'student_id': student.id,
                'exam_id': exam.id,
                'total_max_marks': total_max,
                'total_marks_obtained': total_obtained,
                'overall_grade': grade_line.grade if grade_line else False,
                'attendance_percentage': attendance_pct,
                'state': 'published',
            }
            if card:
                card.write(vals)
            else:
                card = self.create(vals)
            cards |= card

        # Rank within each section by percentage, descending.
        for section in exam.section_ids:
            section_cards = cards.filtered(lambda c: c.student_id.section_id == section).sorted(
                'percentage', reverse=True)
            for index, card in enumerate(section_cards, start=1):
                card.rank_in_section = index
        return cards
