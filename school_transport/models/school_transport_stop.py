from odoo import fields, models


class SchoolTransportStop(models.Model):
    _name = 'school.transport.stop'
    _description = 'Transport Stop'
    _order = 'route_id, sequence'

    route_id = fields.Many2one('school.transport.route', string='Route', required=True, ondelete='cascade')
    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    pickup_time = fields.Float()
    drop_time = fields.Float()
    landmark = fields.Char()
