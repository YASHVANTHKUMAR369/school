from odoo import api, fields, models


class SchoolPayslip(models.Model):
    _name = 'school.payslip'
    _description = 'Payslip'
    _inherit = ['school.sequence.mixin', 'mail.thread']
    _sequence_code = 'school.payslip'
    _order = 'year desc, month desc'

    name = fields.Char(readonly=True, copy=False, default='New')
    staff_id = fields.Many2one('school.staff', string='Staff', required=True, ondelete='cascade')
    structure_id = fields.Many2one('school.salary.structure', string='Salary Structure', required=True)
    month = fields.Selection(
        [(str(i), m) for i, m in enumerate(
            ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December'], start=1)],
        required=True,
    )
    year = fields.Integer(required=True, default=lambda self: fields.Date.context_today(self).year)
    line_ids = fields.One2many('school.payslip.line', 'payslip_id', string='Lines')
    gross_pay = fields.Float(compute='_compute_totals', store=True)
    total_deduction = fields.Float(compute='_compute_totals', store=True)
    net_pay = fields.Float(compute='_compute_totals', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('computed', 'Computed'), ('confirmed', 'Confirmed'), ('paid', 'Paid')],
        default='draft', required=True, tracking=True,
    )

    _staff_month_year_uniq = models.Constraint(
        'UNIQUE (staff_id, month, year)', 'A payslip for this staff member and month already exists.')

    @api.depends('line_ids.amount', 'line_ids.component_type')
    def _compute_totals(self):
        for rec in self:
            earnings = sum(rec.line_ids.filtered(lambda l: l.component_type == 'earning').mapped('amount'))
            deductions = sum(rec.line_ids.filtered(lambda l: l.component_type == 'deduction').mapped('amount'))
            rec.gross_pay = earnings
            rec.total_deduction = deductions
            rec.net_pay = earnings - deductions

    def action_compute(self):
        for rec in self:
            rec.line_ids.unlink()
            lines = [
                (0, 0, {
                    'component_name': line.component_name,
                    'component_type': line.component_type,
                    'amount': line.compute_amount(rec.staff_id.basic_salary),
                }) for line in rec.structure_id.line_ids
            ]
            rec.write({'line_ids': lines, 'state': 'computed'})

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_mark_paid(self):
        self.write({'state': 'paid'})


class SchoolPayslipLine(models.Model):
    _name = 'school.payslip.line'
    _description = 'Payslip Line'

    payslip_id = fields.Many2one('school.payslip', string='Payslip', required=True, ondelete='cascade')
    component_name = fields.Char(required=True)
    component_type = fields.Selection(
        [('earning', 'Earning'), ('deduction', 'Deduction')], required=True)
    amount = fields.Float(required=True)
