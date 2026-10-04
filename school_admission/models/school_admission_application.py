from odoo import api, fields, models


class SchoolAdmissionApplication(models.Model):
    _name = 'school.admission.application'
    _description = 'Admission Application'
    _inherit = ['school.sequence.mixin', 'mail.thread', 'mail.activity.mixin']
    _sequence_code = 'school.admission.application'
    _order = 'create_date desc'

    name = fields.Char(readonly=True, copy=False, default='New')
    enquiry_id = fields.Many2one('school.admission.enquiry', string='Origin Enquiry')
    academic_year_id = fields.Many2one(
        'school.academic.year', string='Academic Year', required=True,
        default=lambda self: self.env['school.academic.year'].search([('is_current', '=', True)], limit=1))
    child_name = fields.Char(string='Applicant Name', required=True, tracking=True)
    dob = fields.Date(string='Date of Birth', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True)
    photo = fields.Image(max_width=512, max_height=512)
    standard_applied_id = fields.Many2one('school.standard', string='Standard Applied For', required=True)
    previous_school = fields.Char()
    mobile = fields.Char(required=True)
    email = fields.Char()
    interview_date = fields.Datetime()
    interview_score = fields.Float()
    interview_remark = fields.Text()
    reject_reason = fields.Text()
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('interview_scheduled', 'Interview Scheduled'),
            ('interview_done', 'Interview Done'),
            ('admitted', 'Admitted'),
            ('waitlisted', 'Waitlisted'),
            ('rejected', 'Rejected'),
        ],
        default='draft', required=True, tracking=True,
    )
    student_id = fields.Many2one('school.student', string='Student', readonly=True, copy=False)

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_schedule_interview(self):
        self.write({'state': 'interview_scheduled'})

    def action_mark_interview_done(self):
        self.write({'state': 'interview_done'})

    def action_waitlist(self):
        self.write({'state': 'waitlisted'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def action_admit(self):
        self.ensure_one()
        student = self.env['school.student'].create({
            'first_name': self.child_name,
            'dob': self.dob,
            'gender': self.gender,
            'photo': self.photo,
            'standard_id': self.standard_applied_id.id,
            'academic_year_id': self.academic_year_id.id,
            'admission_date': fields.Date.context_today(self),
            'previous_school': self.previous_school,
            'application_id': self.id,
        })
        self.write({'state': 'admitted', 'student_id': student.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.student',
            'view_mode': 'form',
            'res_id': student.id,
        }
