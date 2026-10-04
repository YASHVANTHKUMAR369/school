from odoo import fields, models


class SchoolNotice(models.Model):
    _name = 'school.notice'
    _description = 'Notice / Circular'
    _inherit = ['mail.thread']
    _order = 'notice_date desc'

    title = fields.Char(required=True, tracking=True)
    body = fields.Html()
    notice_date = fields.Date(default=fields.Date.context_today, required=True)
    expiry_date = fields.Date()
    audience_type = fields.Selection(
        [
            ('all', 'All'),
            ('standard', 'Standard'),
            ('section', 'Section'),
            ('individual_student', 'Individual Students'),
            ('individual_staff', 'Individual Staff'),
        ],
        default='all', required=True,
    )
    standard_ids = fields.Many2many('school.standard', string='Standards')
    section_ids = fields.Many2many('school.section', string='Sections')
    student_ids = fields.Many2many('school.student', string='Students')
    staff_ids = fields.Many2many('school.staff', string='Staff')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    send_email = fields.Boolean()
    send_sms = fields.Boolean()
    log_ids = fields.One2many('school.communication.log', 'notice_id', string='Dispatch Log')
    state = fields.Selection(
        [('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')],
        default='draft', required=True, tracking=True,
    )

    def _get_target_students(self):
        self.ensure_one()
        Student = self.env['school.student']
        if self.audience_type == 'all':
            return Student.search([('state', '=', 'active')])
        if self.audience_type == 'standard':
            return Student.search([('standard_id', 'in', self.standard_ids.ids), ('state', '=', 'active')])
        if self.audience_type == 'section':
            return Student.search([('section_id', 'in', self.section_ids.ids), ('state', '=', 'active')])
        if self.audience_type == 'individual_student':
            return self.student_ids
        return Student

    def action_publish(self):
        for rec in self:
            rec.write({'state': 'published'})
            students = rec._get_target_students()
            guardians = students.mapped('guardian_ids')
            Log = self.env['school.communication.log']
            for guardian in guardians:
                if rec.send_email and guardian.email:
                    Log.create({
                        'notice_id': rec.id, 'channel': 'email',
                        'recipient_partner_id': guardian.id, 'status': 'pending',
                    })
                if rec.send_sms and guardian.mobile:
                    Log.create({
                        'notice_id': rec.id, 'channel': 'sms',
                        'recipient_partner_id': guardian.id, 'recipient_mobile': guardian.mobile,
                        'status': 'pending',
                    })

    def action_archive_notice(self):
        self.write({'state': 'archived'})
