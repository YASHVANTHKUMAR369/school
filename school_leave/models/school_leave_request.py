from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolLeaveRequest(models.Model):
    _name = 'school.leave.request'
    _description = 'Leave Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_from desc'

    applicant_type = fields.Selection(
        [('staff', 'Staff'), ('student', 'Student')], required=True, default='staff', tracking=True)
    staff_id = fields.Many2one('school.staff', string='Staff')
    student_id = fields.Many2one('school.student', string='Student')
    leave_type_id = fields.Many2one('school.leave.type', string='Leave Type', required=True)
    date_from = fields.Date(required=True, tracking=True)
    date_to = fields.Date(required=True, tracking=True)
    no_of_days = fields.Integer(compute='_compute_no_of_days', store=True)
    reason = fields.Text()
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('refused', 'Refused'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft', required=True, tracking=True,
    )

    @api.depends('date_from', 'date_to')
    def _compute_no_of_days(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_to >= rec.date_from:
                rec.no_of_days = (rec.date_to - rec.date_from).days + 1
            else:
                rec.no_of_days = 0

    @api.constrains('applicant_type', 'staff_id', 'student_id')
    def _check_applicant(self):
        for rec in self:
            if rec.applicant_type == 'staff' and not rec.staff_id:
                raise ValidationError('Please select the staff member applying for leave.')
            if rec.applicant_type == 'student' and not rec.student_id:
                raise ValidationError('Please select the student applying for leave.')

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise ValidationError('The end date must be on or after the start date.')

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_refuse(self):
        self.write({'state': 'refused'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
