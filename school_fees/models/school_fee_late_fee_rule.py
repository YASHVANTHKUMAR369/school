from odoo import fields, models


class SchoolFeeLateFeeRule(models.Model):
    _name = 'school.fee.late.fee.rule'
    _description = 'Late Fee Rule'

    name = fields.Char(required=True)
    grace_days = fields.Integer(default=0)
    calc_type = fields.Selection(
        [
            ('fixed', 'Fixed Amount'),
            ('percent_per_day', 'Percentage per Day Overdue'),
            ('percent_flat', 'Flat Percentage'),
        ],
        default='fixed', required=True,
    )
    value = fields.Float(required=True)
    fee_head_id = fields.Many2one(
        'school.fee.head', string='Applies To',
        help='Leave empty to apply to all fee heads on the invoice.')
    active = fields.Boolean(default=True)

    def compute_late_fee(self, invoice_amount, days_overdue):
        self.ensure_one()
        if days_overdue <= self.grace_days:
            return 0.0
        overdue_days = days_overdue - self.grace_days
        if self.calc_type == 'fixed':
            return self.value
        if self.calc_type == 'percent_per_day':
            return invoice_amount * (self.value / 100.0) * overdue_days
        if self.calc_type == 'percent_flat':
            return invoice_amount * (self.value / 100.0)
        return 0.0
