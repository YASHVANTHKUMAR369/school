from odoo import fields, models


class SchoolBoard(models.Model):
    _name = 'school.board'
    _description = 'Education Board'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Selection(
        [
            ('cbse', 'CBSE'),
            ('icse', 'ICSE'),
            ('state', 'State Board'),
            ('ib', 'IB'),
            ('other', 'Other'),
        ],
        required=True, default='cbse',
    )
    affiliation_no = fields.Char(string='Affiliation Number')
    standard_ids = fields.One2many('school.standard', 'board_id', string='Standards')

    _name_uniq = models.Constraint(
        'UNIQUE (name)', 'A board with this name already exists.')
