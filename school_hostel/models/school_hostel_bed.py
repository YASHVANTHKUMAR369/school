from odoo import fields, models


class SchoolHostelBed(models.Model):
    _name = 'school.hostel.bed'
    _description = 'Hostel Bed'

    room_id = fields.Many2one('school.hostel.room', string='Room', required=True, ondelete='cascade')
    hostel_id = fields.Many2one(related='room_id.hostel_id', store=True)
    bed_no = fields.Char(required=True)
    state = fields.Selection(
        [('vacant', 'Vacant'), ('occupied', 'Occupied'), ('maintenance', 'Maintenance')],
        default='vacant', required=True)

    _room_bed_no_uniq = models.Constraint(
        'UNIQUE (room_id, bed_no)', 'This bed number already exists in this room.')
