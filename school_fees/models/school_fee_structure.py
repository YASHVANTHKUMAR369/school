from odoo import api, fields, models


class SchoolFeeStructure(models.Model):
    _name = 'school.fee.structure'
    _description = 'Fee Structure'

    name = fields.Char(compute='_compute_name', store=True)
    academic_year_id = fields.Many2one('school.academic.year', string='Academic Year', required=True)
    standard_id = fields.Many2one('school.standard', string='Standard', required=True)
    line_ids = fields.One2many('school.fee.structure.line', 'structure_id', string='Fee Lines')
    total_amount = fields.Float(compute='_compute_total_amount', store=True)

    _standard_year_uniq = models.Constraint(
        'UNIQUE (standard_id, academic_year_id)',
        'A fee structure for this standard and academic year already exists.')

    @api.depends('standard_id', 'academic_year_id')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.standard_id.name} - {rec.academic_year_id.name}" if rec.standard_id and rec.academic_year_id else 'New'

    @api.depends('line_ids.amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('amount'))


class SchoolFeeStructureLine(models.Model):
    _name = 'school.fee.structure.line'
    _description = 'Fee Structure Line'

    structure_id = fields.Many2one('school.fee.structure', string='Fee Structure', required=True, ondelete='cascade')
    fee_head_id = fields.Many2one('school.fee.head', string='Fee Head', required=True)
    amount = fields.Float(required=True)
    due_date = fields.Date()
    frequency = fields.Selection(
        [
            ('one_time', 'One Time'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('annual', 'Annual'),
        ],
        default='annual', required=True,
    )
