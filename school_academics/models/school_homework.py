from odoo import api, fields, models


class SchoolHomework(models.Model):
    _name = 'school.homework'
    _description = 'Homework'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'due_date desc'

    name = fields.Char(required=True, tracking=True)
    subject_id = fields.Many2one('school.subject', string='Subject', required=True)
    section_id = fields.Many2one('school.section', string='Section', required=True)
    staff_id = fields.Many2one('school.staff', string='Teacher', required=True)
    assign_date = fields.Date(default=fields.Date.context_today, required=True)
    due_date = fields.Date(required=True)
    description = fields.Html()
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('closed', 'Closed'),
        ],
        default='draft', required=True, tracking=True,
    )
    submission_ids = fields.One2many('school.homework.submission', 'homework_id', string='Submissions')
    submission_count = fields.Integer(compute='_compute_submission_count')

    @api.depends('submission_ids')
    def _compute_submission_count(self):
        for rec in self:
            rec.submission_count = len(rec.submission_ids)

    def action_publish(self):
        self.ensure_one()
        self.write({'state': 'published'})
        students = self.env['school.student'].search([
            ('section_id', '=', self.section_id.id), ('state', '=', 'active')])
        existing = self.submission_ids.student_id
        to_create = students - existing
        self.env['school.homework.submission'].create([
            {'homework_id': self.id, 'student_id': student.id} for student in to_create
        ])

    def action_close(self):
        self.write({'state': 'closed'})
