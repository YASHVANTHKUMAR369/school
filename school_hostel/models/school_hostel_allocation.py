from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolHostelAllocation(models.Model):
    _name = 'school.hostel.allocation'
    _description = 'Hostel Allocation'

    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    hostel_id = fields.Many2one('school.hostel', string='Hostel', required=True)
    room_id = fields.Many2one(
        'school.hostel.room', string='Room', required=True, domain="[('hostel_id', '=', hostel_id)]")
    bed_id = fields.Many2one(
        'school.hostel.bed', string='Bed', required=True, domain="[('room_id', '=', room_id)]")
    date_from = fields.Date(default=fields.Date.context_today, required=True)
    date_to = fields.Date()
    state = fields.Selection([('active', 'Active'), ('vacated', 'Vacated')], default='active', required=True)

    @api.constrains('bed_id', 'state')
    def _check_bed_not_double_booked(self):
        for rec in self:
            if rec.state == 'active':
                other = self.search([
                    ('bed_id', '=', rec.bed_id.id), ('state', '=', 'active'), ('id', '!=', rec.id)])
                if other:
                    raise ValidationError('This bed is already occupied by another active allocation.')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.state == 'active':
                rec.bed_id.state = 'occupied'
        return records

    def action_vacate(self):
        for rec in self:
            rec.write({'state': 'vacated', 'date_to': fields.Date.context_today(rec)})
            rec.bed_id.state = 'vacant'

    def action_activate(self):
        for rec in self:
            rec.write({'state': 'active'})
            rec.bed_id.state = 'occupied'
