from odoo import fields, models


class SchoolTransportRoute(models.Model):
    _name = 'school.transport.route'
    _description = 'Transport Route'

    name = fields.Char(required=True)
    vehicle_id = fields.Many2one('school.transport.vehicle', string='Vehicle')
    start_point = fields.Char()
    end_point = fields.Char()
    stop_ids = fields.One2many('school.transport.stop', 'route_id', string='Stops')
    active = fields.Boolean(default=True)
