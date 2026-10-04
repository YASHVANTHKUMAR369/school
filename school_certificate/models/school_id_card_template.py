from odoo import fields, models


class SchoolIdCardTemplate(models.Model):
    _name = 'school.id.card.template'
    _description = 'ID Card Template'

    name = fields.Char(required=True)
    standard_ids = fields.Many2many('school.standard', string='Applicable Standards')
    valid_until = fields.Date()
