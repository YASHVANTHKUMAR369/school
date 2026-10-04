from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolAcademicYear(models.Model):
    _name = 'school.academic.year'
    _description = 'Academic Year'
    _inherit = ['mail.thread']
    _order = 'date_start desc'

    name = fields.Char(required=True, tracking=True)
    date_start = fields.Date(
        required=True, tracking=True,
        default=lambda self: fields.Date.today().replace(month=6, day=1))
    date_end = fields.Date(
        required=True, tracking=True,
        default=lambda self: (fields.Date.today() + relativedelta(years=1)).replace(month=3, day=31))
    is_current = fields.Boolean(string='Current Year', tracking=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('closed', 'Closed'),
        ],
        default='draft', required=True, tracking=True,
    )
    section_ids = fields.One2many('school.section', 'academic_year_id', string='Sections')

    _name_uniq = models.Constraint(
        'UNIQUE (name)', 'An academic year with this name already exists.')

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start >= rec.date_end:
                raise ValidationError('The end date must be after the start date.')

    @api.constrains('is_current')
    def _check_single_current(self):
        for rec in self:
            if rec.is_current:
                other = self.search([('is_current', '=', True), ('id', '!=', rec.id)])
                if other:
                    other.write({'is_current': False})

    def action_activate(self):
        self.write({'state': 'active'})

    def action_close(self):
        self.write({'state': 'closed'})
