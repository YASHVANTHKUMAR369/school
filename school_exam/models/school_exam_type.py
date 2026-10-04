from odoo import fields, models


class SchoolExamType(models.Model):
    _name = 'school.exam.type'
    _description = 'Exam Type'

    name = fields.Char(required=True, help='E.g. Unit Test, Half-Yearly, Annual, Pre-Board')
    weightage = fields.Float(help='Weightage % towards the cumulative result, if applicable')
