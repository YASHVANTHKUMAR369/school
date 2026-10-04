import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

AADHAR_RE = re.compile(r'^\d{12}$')


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _inherit = ['school.sequence.mixin', 'mail.thread', 'mail.activity.mixin']
    _sequence_code = 'school.student.admission.no'
    _sequence_field = 'admission_no'
    _order = 'first_name'

    admission_no = fields.Char(readonly=True, copy=False)
    roll_no = fields.Char()
    first_name = fields.Char(required=True, tracking=True)
    last_name = fields.Char()
    name = fields.Char(compute='_compute_name', store=True, string='Full Name')
    dob = fields.Date(string='Date of Birth', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], required=True)
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'),
         ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'), ('o-', 'O-')])
    aadhar_no = fields.Char(string='Aadhar Number')
    category = fields.Selection(
        [
            ('general', 'General'),
            ('obc', 'OBC'),
            ('sc', 'SC'),
            ('st', 'ST'),
            ('ews', 'EWS'),
            ('other', 'Other'),
        ],
        default='general',
    )
    religion = fields.Char()
    mother_tongue = fields.Char()
    nationality_id = fields.Many2one('res.country', string='Nationality')
    photo = fields.Image(max_width=512, max_height=512)
    standard_id = fields.Many2one('school.standard', string='Standard', required=True, tracking=True)
    section_id = fields.Many2one(
        'school.section', string='Section', tracking=True,
        domain="[('standard_id', '=', standard_id)]")
    academic_year_id = fields.Many2one('school.academic.year', string='Academic Year', required=True)
    admission_date = fields.Date(default=fields.Date.context_today)
    previous_school = fields.Char()
    medical_notes = fields.Text()
    application_id = fields.Many2one('school.admission.application', string='Admission Application', readonly=True)
    guardian_ids = fields.Many2many(
        'school.guardian', 'school_student_guardian_rel', 'student_id', 'guardian_id',
        string='Guardians')
    primary_guardian_id = fields.Many2one(
        'school.guardian', string='Primary Guardian',
        domain="[('id', 'in', guardian_ids)]")
    state = fields.Selection(
        [
            ('admitted', 'Admitted'),
            ('active', 'Active'),
            ('alumni', 'Alumni'),
            ('tc_issued', 'TC Issued'),
            ('struck_off', 'Struck Off'),
        ],
        default='admitted', required=True, tracking=True,
    )
    active = fields.Boolean(default=True)

    _admission_no_uniq = models.Constraint('UNIQUE (admission_no)', 'Admission number must be unique.')

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = ' '.join(filter(None, [rec.first_name, rec.last_name]))

    @api.constrains('aadhar_no')
    def _check_aadhar_no(self):
        for rec in self:
            if rec.aadhar_no and not AADHAR_RE.match(rec.aadhar_no):
                raise ValidationError('Aadhar Number must be exactly 12 digits.')

    @api.onchange('guardian_ids')
    def _onchange_guardian_ids(self):
        if self.primary_guardian_id and self.primary_guardian_id not in self.guardian_ids:
            self.primary_guardian_id = False
        if not self.primary_guardian_id and self.guardian_ids:
            self.primary_guardian_id = self.guardian_ids[0]

    def action_activate(self):
        self.write({'state': 'active'})

    def action_mark_alumni(self):
        self.write({'state': 'alumni'})
