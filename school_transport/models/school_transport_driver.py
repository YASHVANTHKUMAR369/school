from odoo import fields, models


class SchoolTransportDriver(models.Model):
    _name = 'school.transport.driver'
    _description = 'Transport Driver'

    name = fields.Char(required=True)
    license_no = fields.Char(string='License Number', required=True)
    license_expiry = fields.Date()
    mobile = fields.Char()
    photo = fields.Image(max_width=512, max_height=512)
    active = fields.Boolean(default=True)
