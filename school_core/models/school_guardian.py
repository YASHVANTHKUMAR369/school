import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError

AADHAR_RE = re.compile(r'^\d{12}$')


class SchoolGuardian(models.Model):
    _name = 'school.guardian'
    _description = 'Guardian / Parent'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(required=True, tracking=True)
    relation = fields.Selection(
        [
            ('father', 'Father'),
            ('mother', 'Mother'),
            ('guardian', 'Guardian'),
        ],
        required=True, default='guardian',
    )
    mobile = fields.Char()
    email = fields.Char()
    aadhar_no = fields.Char(string='Aadhar Number')
    occupation = fields.Char()
    street = fields.Char()
    city = fields.Char()
    state = fields.Char()
    zip = fields.Char()
    country_id = fields.Many2one('res.country', string='Country')
    is_primary_contact = fields.Boolean(string='Primary Contact')
    # student_ids is added by school_admission once school.student exists.

    @api.constrains('aadhar_no')
    def _check_aadhar_no(self):
        for rec in self:
            if rec.aadhar_no and not AADHAR_RE.match(rec.aadhar_no):
                raise ValidationError('Aadhar Number must be exactly 12 digits.')
