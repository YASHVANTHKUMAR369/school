from odoo import fields, models


class SchoolHostelRoom(models.Model):
    _name = 'school.hostel.room'
    _description = 'Hostel Room'

    hostel_id = fields.Many2one('school.hostel', string='Hostel', required=True, ondelete='cascade')
    room_no = fields.Char(required=True)
    floor = fields.Char()
    capacity = fields.Integer(default=1)
    room_type = fields.Selection(
        [('dorm', 'Dormitory'), ('shared', 'Shared'), ('single', 'Single')], default='shared', required=True)
    bed_ids = fields.One2many('school.hostel.bed', 'room_id', string='Beds')

    _hostel_room_no_uniq = models.Constraint(
        'UNIQUE (hostel_id, room_no)', 'This room number already exists in this hostel.')
