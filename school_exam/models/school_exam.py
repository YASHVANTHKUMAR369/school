from odoo import fields, models


class SchoolExam(models.Model):
    _name = 'school.exam'
    _description = 'Exam'
    _inherit = ['mail.thread']
    _order = 'date_from desc'

    name = fields.Char(required=True, tracking=True)
    exam_type_id = fields.Many2one('school.exam.type', string='Exam Type', required=True)
    academic_year_id = fields.Many2one('school.academic.year', string='Academic Year', required=True)
    standard_id = fields.Many2one('school.standard', string='Standard', required=True)
    section_ids = fields.Many2many('school.section', string='Sections')
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    grade_scale_id = fields.Many2one('school.grade.scale', string='Grade Scale')
    schedule_ids = fields.One2many('school.exam.schedule', 'exam_id', string='Subject Schedule')
    result_ids = fields.One2many('school.exam.result', 'exam_id', string='Results')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('scheduled', 'Scheduled'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('results_published', 'Results Published'),
        ],
        default='draft', required=True, tracking=True,
    )

    def action_schedule(self):
        self.write({'state': 'scheduled'})

    def action_start(self):
        self.write({'state': 'ongoing'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_publish_results(self):
        self.ensure_one()
        self.write({'state': 'results_published'})
        self.env['school.report.card'].generate_for_exam(self)
