from odoo import fields, models


class SchoolDepartment(models.Model):
    _name = 'school.department'
    _description = 'Department'

    name = fields.Char(required=True)
    head_staff_id = fields.Many2one('school.staff', string='Department Head')
