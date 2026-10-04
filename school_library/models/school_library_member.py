from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolLibraryMember(models.Model):
    _name = 'school.library.member'
    _description = 'Library Member'

    member_code = fields.Char(readonly=True, copy=False)
    partner_type = fields.Selection(
        [('student', 'Student'), ('staff', 'Staff')], required=True, default='student')
    student_id = fields.Many2one('school.student', string='Student')
    staff_id = fields.Many2one('school.staff', string='Staff')
    name = fields.Char(compute='_compute_name', store=True)
    max_books_allowed = fields.Integer(default=3)
    circulation_ids = fields.One2many('school.library.circulation', 'member_id', string='Circulation History')

    @api.depends('partner_type', 'student_id', 'staff_id')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.student_id.name if rec.partner_type == 'student' else rec.staff_id.name

    @api.constrains('partner_type', 'student_id', 'staff_id')
    def _check_partner(self):
        for rec in self:
            if rec.partner_type == 'student' and not rec.student_id:
                raise ValidationError('Please select the student for this library member.')
            if rec.partner_type == 'staff' and not rec.staff_id:
                raise ValidationError('Please select the staff member for this library member.')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('member_code'):
                vals['member_code'] = self.env['ir.sequence'].next_by_code('school.library.member') or '/'
        return super().create(vals_list)
