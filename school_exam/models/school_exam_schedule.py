from odoo import fields, models


class SchoolExamSchedule(models.Model):
    _name = 'school.exam.schedule'
    _description = 'Exam Subject Schedule'
    _order = 'date, time_from'

    exam_id = fields.Many2one('school.exam', string='Exam', required=True, ondelete='cascade')
    subject_id = fields.Many2one('school.subject', string='Subject', required=True)
    date = fields.Date(required=True)
    time_from = fields.Float(string='From')
    time_to = fields.Float(string='To')
    max_marks = fields.Float(default=100.0, required=True)
    passing_marks = fields.Float(default=33.0, required=True)
    room_no = fields.Char()

    _exam_subject_uniq = models.Constraint(
        'UNIQUE (exam_id, subject_id)', 'This subject is already scheduled for this exam.')
