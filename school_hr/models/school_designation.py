from odoo import fields, models


class SchoolDesignation(models.Model):
    _name = 'school.designation'
    _description = 'Designation'

    name = fields.Char(required=True, help='E.g. Principal, PGT, TGT, PRT, Clerk, Peon, Librarian, Driver')
    department_id = fields.Many2one('school.department', string='Department')
