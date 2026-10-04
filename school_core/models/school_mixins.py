from odoo import api, fields, models


class SchoolSequenceMixin(models.AbstractModel):
    """Abstract helper that assigns a code from an ir.sequence on create.

    Concrete models set `_sequence_code` to the ir.sequence's `code` and
    hold the human-readable value in a field named by `_sequence_field`.
    """
    _name = 'school.sequence.mixin'
    _description = 'School Sequence Mixin'

    _sequence_code = None
    _sequence_field = 'name'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self._sequence_code and not vals.get(self._sequence_field):
                vals[self._sequence_field] = self.env['ir.sequence'].next_by_code(
                    self._sequence_code) or '/'
        return super().create(vals_list)


class SchoolStateMixin(models.AbstractModel):
    """Abstract helper providing a common draft/confirm/cancel workflow."""
    _name = 'school.state.mixin'
    _description = 'School State Mixin'

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='draft',
        required=True,
        tracking=True,
    )

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_set_draft(self):
        self.write({'state': 'draft'})
