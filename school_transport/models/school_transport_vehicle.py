from odoo import fields, models


class SchoolTransportVehicle(models.Model):
    _name = 'school.transport.vehicle'
    _description = 'Transport Vehicle'

    name = fields.Char(required=True)
    registration_no = fields.Char(required=True)
    capacity = fields.Integer(default=40)
    vehicle_type = fields.Selection([('bus', 'Bus'), ('van', 'Van')], default='bus', required=True)
    driver_id = fields.Many2one('school.transport.driver', string='Driver')
    insurance_expiry = fields.Date()
    fitness_expiry = fields.Date()
    active = fields.Boolean(default=True)

    _registration_no_uniq = models.Constraint(
        'UNIQUE (registration_no)', 'A vehicle with this registration number already exists.')
