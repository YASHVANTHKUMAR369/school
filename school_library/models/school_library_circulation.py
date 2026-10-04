from datetime import timedelta

from odoo import api, fields, models


class SchoolLibraryCirculation(models.Model):
    _name = 'school.library.circulation'
    _description = 'Library Circulation'
    _order = 'issue_date desc'

    member_id = fields.Many2one('school.library.member', string='Member', required=True, ondelete='cascade')
    book_copy_id = fields.Many2one(
        'school.library.book.copy', string='Book Copy', required=True,
        domain="[('state', '=', 'available')]")
    book_id = fields.Many2one(related='book_copy_id.book_id', store=True)
    issue_date = fields.Date(default=fields.Date.context_today, required=True)
    due_date = fields.Date(required=True)
    return_date = fields.Date()
    fine_amount = fields.Float(compute='_compute_fine_amount', store=True)
    fine_per_day = fields.Float(default=2.0)
    state = fields.Selection(
        [
            ('issued', 'Issued'),
            ('returned', 'Returned'),
            ('overdue', 'Overdue'),
            ('lost', 'Lost'),
        ],
        default='issued', required=True,
    )

    @api.depends('due_date', 'return_date', 'fine_per_day', 'state')
    def _compute_fine_amount(self):
        today = fields.Date.context_today(self)
        for rec in self:
            end_date = rec.return_date or today
            if rec.due_date and end_date > rec.due_date and rec.state != 'lost':
                rec.fine_amount = (end_date - rec.due_date).days * rec.fine_per_day
            else:
                rec.fine_amount = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault('due_date', fields.Date.context_today(self) + timedelta(days=14))
        records = super().create(vals_list)
        records.book_copy_id.write({'state': 'issued'})
        return records

    def action_return(self):
        for rec in self:
            rec.write({'return_date': fields.Date.context_today(rec), 'state': 'returned'})
            rec.book_copy_id.state = 'available'

    def action_mark_lost(self):
        for rec in self:
            rec.write({'state': 'lost'})
            rec.book_copy_id.state = 'lost'
