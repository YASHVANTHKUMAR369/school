from odoo import api, fields, models


class SchoolHostel(models.Model):
    _name = 'school.hostel'
    _description = 'Hostel'

    name = fields.Char(required=True)
    warden_id = fields.Many2one('school.staff', string='Warden')
    address = fields.Text()
    gender_type = fields.Selection(
        [('boys', 'Boys'), ('girls', 'Girls'), ('mixed', 'Mixed')], default='boys', required=True)
    room_ids = fields.One2many('school.hostel.room', 'hostel_id', string='Rooms')
    capacity = fields.Integer(compute='_compute_capacity')

    @api.depends('room_ids.capacity')
    def _compute_capacity(self):
        for rec in self:
            rec.capacity = sum(rec.room_ids.mapped('capacity'))
