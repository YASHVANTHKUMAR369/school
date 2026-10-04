import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

AADHAR_RE = re.compile(r'^\d{12}$')


class SchoolStaff(models.Model):
    _name = 'school.staff'
    _description = 'Staff'
    _inherit = ['school.sequence.mixin', 'mail.thread', 'mail.activity.mixin']
    _sequence_code = 'school.staff.code'
    _sequence_field = 'staff_code'
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    staff_code = fields.Char(readonly=True, copy=False)
    photo = fields.Image(max_width=512, max_height=512)
    mobile = fields.Char()
    email = fields.Char()
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    dob = fields.Date(string='Date of Birth')
    aadhar_no = fields.Char(string='Aadhar Number')
    qualification = fields.Char()
    active = fields.Boolean(default=True)
    user_id = fields.Many2one(
        'res.users', string='Internal User', domain=[('share', '=', False)],
        help='Backend login for this staff member (Teacher/Accountant/etc.), if any.')
    class_teacher_section_ids = fields.One2many(
        'school.section', 'class_teacher_id', string='Class Teacher Of')

    _staff_code_uniq = models.Constraint(
        'UNIQUE (staff_code)', 'Staff code must be unique.')

    @api.constrains('aadhar_no')
    def _check_aadhar_no(self):
        for rec in self:
            if rec.aadhar_no and not AADHAR_RE.match(rec.aadhar_no):
                raise ValidationError('Aadhar Number must be exactly 12 digits.')
