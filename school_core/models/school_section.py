from odoo import fields, models


class SchoolSection(models.Model):
    _name = 'school.section'
    _description = 'Section / Division'
    _order = 'standard_id, name'

    name = fields.Char(required=True, help='E.g. A, B, C')
    standard_id = fields.Many2one('school.standard', string='Standard', required=True, ondelete='cascade')
    academic_year_id = fields.Many2one('school.academic.year', string='Academic Year', required=True)
    class_teacher_id = fields.Many2one('school.staff', string='Class Teacher')
    capacity = fields.Integer(default=40)
    room_no = fields.Char(string='Room No.')
    student_count = fields.Integer(compute='_compute_student_count', string='Students')

    _name_standard_year_uniq = models.Constraint(
        'UNIQUE (name, standard_id, academic_year_id)',
        'This section already exists for the standard in this academic year.')

    def _compute_student_count(self):
        # school.student is defined in school_admission; feature-detect so
        # school_core stays independently installable.
        Student = self.env.get('school.student')
        for rec in self:
            rec.student_count = Student.search_count([('section_id', '=', rec.id)]) if Student is not None else 0
