from odoo import fields, models


class SchoolSalaryStructure(models.Model):
    _name = 'school.salary.structure'
    _description = 'Salary Structure'

    name = fields.Char(required=True)
    line_ids = fields.One2many('school.salary.structure.line', 'structure_id', string='Components')


class SchoolSalaryStructureLine(models.Model):
    _name = 'school.salary.structure.line'
    _description = 'Salary Structure Line'

    structure_id = fields.Many2one('school.salary.structure', string='Structure', required=True, ondelete='cascade')
    component_name = fields.Char(required=True)
    component_type = fields.Selection(
        [('earning', 'Earning'), ('deduction', 'Deduction')], required=True, default='earning')
    calc_type = fields.Selection(
        [('fixed', 'Fixed'), ('percent_of_basic', '% of Basic')], required=True, default='fixed')
    value = fields.Float(required=True)

    def compute_amount(self, basic_salary):
        self.ensure_one()
        if self.calc_type == 'fixed':
            return self.value
        return basic_salary * (self.value / 100.0)
