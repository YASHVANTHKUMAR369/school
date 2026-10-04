from odoo import api, fields, models


class SchoolSection(models.Model):
    _inherit = 'school.section'

    student_ids = fields.One2many('school.student', 'section_id', string='Student Records')

    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)
