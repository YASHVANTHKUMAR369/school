from odoo import api, fields, models


class SchoolExamResult(models.Model):
    _name = 'school.exam.result'
    _description = 'Exam Result'
    _order = 'student_id'

    exam_id = fields.Many2one('school.exam', string='Exam', required=True, ondelete='cascade')
    schedule_id = fields.Many2one('school.exam.schedule', string='Subject Schedule', required=True, ondelete='cascade')
    subject_id = fields.Many2one(related='schedule_id.subject_id', store=True)
    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    max_marks = fields.Float(related='schedule_id.max_marks', store=True)
    marks_obtained = fields.Float()
    is_absent = fields.Boolean()
    percentage = fields.Float(compute='_compute_percentage', store=True)
    grade = fields.Char(compute='_compute_percentage', store=True)
    remark = fields.Char()

    _exam_student_subject_uniq = models.Constraint(
        'UNIQUE (exam_id, student_id, schedule_id)',
        'A result for this student/subject in this exam already exists.')

    @api.depends('marks_obtained', 'max_marks', 'is_absent')
    def _compute_percentage(self):
        for rec in self:
            if rec.is_absent or not rec.max_marks:
                rec.percentage = 0.0
                rec.grade = 'AB' if rec.is_absent else False
                continue
            rec.percentage = (rec.marks_obtained / rec.max_marks) * 100.0
            scale = rec.exam_id.grade_scale_id
            line = scale.get_grade(rec.percentage) if scale else False
            rec.grade = line.grade if line else False
