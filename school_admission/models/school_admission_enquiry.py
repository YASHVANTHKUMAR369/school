from odoo import api, fields, models


class SchoolAdmissionEnquiry(models.Model):
    _name = 'school.admission.enquiry'
    _description = 'Admission Enquiry'
    _inherit = ['school.sequence.mixin', 'mail.thread', 'mail.activity.mixin']
    _sequence_code = 'school.admission.enquiry'
    _order = 'enquiry_date desc'

    name = fields.Char(readonly=True, copy=False, default='New')
    enquiry_date = fields.Date(default=fields.Date.context_today, required=True)
    child_name = fields.Char(required=True, tracking=True)
    dob = fields.Date(string='Date of Birth')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    standard_applied_id = fields.Many2one('school.standard', string='Standard Applied For')
    parent_name = fields.Char()
    mobile = fields.Char(required=True)
    email = fields.Char()
    source = fields.Selection(
        [
            ('walk_in', 'Walk-in'),
            ('referral', 'Referral'),
            ('website', 'Website'),
            ('advertisement', 'Advertisement'),
            ('other', 'Other'),
        ],
        default='walk_in',
    )
    next_followup_date = fields.Date()
    remark = fields.Text()
    state = fields.Selection(
        [
            ('new', 'New'),
            ('contacted', 'Contacted'),
            ('converted', 'Converted'),
            ('lost', 'Lost'),
        ],
        default='new', required=True, tracking=True,
    )
    application_id = fields.Many2one('school.admission.application', string='Application', readonly=True, copy=False)

    def action_mark_contacted(self):
        self.write({'state': 'contacted'})

    def action_mark_lost(self):
        self.write({'state': 'lost'})

    def action_convert_to_application(self):
        self.ensure_one()
        application = self.env['school.admission.application'].create({
            'enquiry_id': self.id,
            'child_name': self.child_name,
            'dob': self.dob,
            'gender': self.gender,
            'standard_applied_id': self.standard_applied_id.id,
            'mobile': self.mobile,
            'email': self.email,
        })
        self.write({'state': 'converted', 'application_id': application.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.admission.application',
            'view_mode': 'form',
            'res_id': application.id,
        }
