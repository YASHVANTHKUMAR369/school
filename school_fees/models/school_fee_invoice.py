from odoo import api, fields, models


class SchoolFeeInvoice(models.Model):
    _name = 'school.fee.invoice'
    _description = 'Fee Invoice'
    _inherit = ['school.sequence.mixin', 'mail.thread', 'mail.activity.mixin']
    _sequence_code = 'school.fee.invoice'
    _order = 'invoice_date desc'

    name = fields.Char(readonly=True, copy=False, default='New')
    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    academic_year_id = fields.Many2one('school.academic.year', string='Academic Year', required=True)
    invoice_date = fields.Date(default=fields.Date.context_today, required=True)
    due_date = fields.Date(required=True)
    line_ids = fields.One2many('school.fee.invoice.line', 'invoice_id', string='Fee Lines')
    payment_ids = fields.One2many('school.fee.payment', 'invoice_id', string='Payments')
    late_fee_rule_id = fields.Many2one('school.fee.late.fee.rule', string='Late Fee Rule')
    late_fee_amount = fields.Float(compute='_compute_late_fee_amount', store=True)
    total_amount = fields.Float(compute='_compute_amounts', store=True)
    amount_paid = fields.Float(compute='_compute_amounts', store=True)
    amount_due = fields.Float(compute='_compute_amounts', store=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('partially_paid', 'Partially Paid'),
            ('paid', 'Paid'),
            ('overdue', 'Overdue'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft', required=True, tracking=True,
    )

    @api.depends('line_ids.amount', 'payment_ids.amount', 'payment_ids.state', 'late_fee_amount')
    def _compute_amounts(self):
        for rec in self:
            lines_total = sum(rec.line_ids.mapped('amount'))
            rec.total_amount = lines_total + rec.late_fee_amount
            paid = sum(rec.payment_ids.filtered(lambda p: p.state == 'confirmed').mapped('amount'))
            rec.amount_paid = paid
            rec.amount_due = rec.total_amount - paid

    @api.depends('due_date', 'late_fee_rule_id', 'state')
    def _compute_late_fee_amount(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.late_fee_rule_id and rec.due_date and today > rec.due_date and rec.state in ('posted', 'partially_paid', 'overdue'):
                days_overdue = (today - rec.due_date).days
                lines_total = sum(rec.line_ids.mapped('amount'))
                rec.late_fee_amount = rec.late_fee_rule_id.compute_late_fee(lines_total, days_overdue)
            else:
                rec.late_fee_amount = 0.0

    def action_post(self):
        self.write({'state': 'posted'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def _update_payment_state(self):
        for rec in self:
            if rec.state in ('draft', 'cancelled'):
                continue
            if rec.amount_due <= 0:
                rec.state = 'paid'
            elif rec.amount_paid > 0:
                rec.state = 'partially_paid'
            else:
                rec.state = 'posted'

    @api.model
    def _cron_update_overdue_invoices(self):
        today = fields.Date.context_today(self)
        invoices = self.search([
            ('state', 'in', ('posted', 'partially_paid')),
            ('due_date', '<', today),
            ('amount_due', '>', 0),
        ])
        invoices._compute_late_fee_amount()
        invoices._compute_amounts()
        invoices.write({'state': 'overdue'})


class SchoolFeeInvoiceLine(models.Model):
    _name = 'school.fee.invoice.line'
    _description = 'Fee Invoice Line'

    invoice_id = fields.Many2one('school.fee.invoice', string='Invoice', required=True, ondelete='cascade')
    fee_head_id = fields.Many2one('school.fee.head', string='Fee Head', required=True)
    amount = fields.Float(required=True)
    discount = fields.Float()
