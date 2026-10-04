from odoo import fields, models


class SchoolGradeScale(models.Model):
    _name = 'school.grade.scale'
    _description = 'Grade Scale'

    name = fields.Char(required=True, help='E.g. CBSE 9-Point Scale')
    line_ids = fields.One2many('school.grade.scale.line', 'grade_scale_id', string='Grade Bands')

    def get_grade(self, percentage):
        self.ensure_one()
        for line in self.line_ids.sorted('min_percent', reverse=True):
            if line.min_percent <= percentage <= line.max_percent:
                return line
        return self.env['school.grade.scale.line']


class SchoolGradeScaleLine(models.Model):
    _name = 'school.grade.scale.line'
    _description = 'Grade Scale Line'
    _order = 'min_percent desc'

    grade_scale_id = fields.Many2one('school.grade.scale', string='Grade Scale', required=True, ondelete='cascade')
    grade = fields.Char(required=True, help='E.g. A1, A2, B1...')
    min_percent = fields.Float(required=True)
    max_percent = fields.Float(required=True)
    grade_point = fields.Float()
