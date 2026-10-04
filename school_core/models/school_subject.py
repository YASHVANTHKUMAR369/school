from odoo import fields, models


class SchoolSubject(models.Model):
    _name = 'school.subject'
    _description = 'Subject'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char()
    subject_type = fields.Selection(
        [
            ('scholastic', 'Scholastic'),
            ('co_scholastic', 'Co-Scholastic'),
        ],
        default='scholastic', required=True,
    )
    is_elective = fields.Boolean(string='Elective')
    standard_ids = fields.Many2many(
        'school.standard', 'school_standard_subject_rel', 'subject_id', 'standard_id',
        string='Standards')
