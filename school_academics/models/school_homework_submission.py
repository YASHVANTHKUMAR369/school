from odoo import api, fields, models


class SchoolHomeworkSubmission(models.Model):
    _name = 'school.homework.submission'
    _description = 'Homework Submission'
    _order = 'submission_date desc'

    homework_id = fields.Many2one('school.homework', string='Homework', required=True, ondelete='cascade')
    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    due_date = fields.Date(related='homework_id.due_date', store=True)
    submission_date = fields.Datetime()
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    text_answer = fields.Text()
    marks_obtained = fields.Float()
    teacher_remark = fields.Char()
    state = fields.Selection(
        [
            ('pending', 'Pending'),
            ('submitted', 'Submitted'),
            ('late_submitted', 'Late Submitted'),
            ('graded', 'Graded'),
        ],
        default='pending', required=True,
    )

    _homework_student_uniq = models.Constraint(
        'UNIQUE (homework_id, student_id)', 'This student already has a submission row for this homework.')

    def action_submit(self):
        for rec in self:
            today = fields.Date.context_today(rec)
            state = 'late_submitted' if rec.due_date and today > rec.due_date else 'submitted'
            rec.write({'submission_date': fields.Datetime.now(), 'state': state})

    def action_grade(self):
        self.write({'state': 'graded'})
