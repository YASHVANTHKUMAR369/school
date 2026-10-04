from odoo import fields, models


class SchoolGuardian(models.Model):
    _inherit = 'school.guardian'

    user_id = fields.Many2one(
        'res.users', string='Portal User', copy=False,
        domain=[('share', '=', True)],
        help='The portal login linked to this guardian, if access has been granted.')
    portal_access_state = fields.Selection(
        [
            ('not_granted', 'Not Granted'),
            ('granted', 'Granted'),
            ('revoked', 'Revoked'),
        ],
        default='not_granted', required=True, copy=False,
    )
