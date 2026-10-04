from odoo import api, fields, models


class SchoolStandard(models.Model):
    _name = 'school.standard'
    _description = 'Standard / Grade'
    _order = 'sequence, name'

    name = fields.Char(required=True, help='E.g. Nursery, LKG, UKG, I, II, ... XII')
    sequence = fields.Integer(default=10)
    board_id = fields.Many2one('school.board', string='Board', required=True)
    section_ids = fields.One2many('school.section', 'standard_id', string='Sections')
    subject_ids = fields.Many2many(
        'school.subject', 'school_standard_subject_rel', 'standard_id', 'subject_id',
        string='Subjects')
    section_count = fields.Integer(compute='_compute_section_count')

    _name_board_uniq = models.Constraint(
        'UNIQUE (name, board_id)', 'A standard with this name already exists for this board.')

    @api.depends('section_ids')
    def _compute_section_count(self):
        for rec in self:
            rec.section_count = len(rec.section_ids)
