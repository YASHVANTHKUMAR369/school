from odoo import fields, models


class SchoolFeePayment(models.Model):
    _name = 'school.fee.payment'
    _description = 'Fee Payment'
    _inherit = ['school.sequence.mixin', 'mail.thread']
    _sequence_code = 'school.fee.payment'
    _order = 'payment_date desc'

    name = fields.Char(readonly=True, copy=False, default='New')
    invoice_id = fields.Many2one('school.fee.invoice', string='Invoice', required=True, ondelete='cascade')
    student_id = fields.Many2one(related='invoice_id.student_id', store=True)
    payment_date = fields.Date(default=fields.Date.context_today, required=True)
    amount = fields.Float(required=True)
    payment_mode = fields.Selection(
        [
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
            ('upi', 'UPI'),
            ('online', 'Online'),
            ('dd', 'Demand Draft'),
        ],
        default='cash', required=True,
    )
    reference_no = fields.Char()
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='draft', required=True,
    )

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        self.invoice_id._update_payment_state()

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        self.invoice_id._update_payment_state()
