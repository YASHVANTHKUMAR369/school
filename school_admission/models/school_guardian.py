from odoo import api, fields, models


class SchoolGuardian(models.Model):
    _inherit = 'school.guardian'

    student_ids = fields.Many2many(
        'school.student', 'school_student_guardian_rel', 'guardian_id', 'student_id',
        string='Children')
    student_count = fields.Integer(compute='_compute_student_count')

    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)
