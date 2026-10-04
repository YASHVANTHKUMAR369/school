from odoo import _, fields, models
from odoo.exceptions import UserError


class SchoolPortalGrantWizard(models.TransientModel):
    _name = 'school.portal.grant.wizard'
    _description = 'Grant Guardian Portal Access'

    guardian_ids = fields.Many2many(
        'school.guardian', string='Guardians', required=True,
        default=lambda self: self.env['school.guardian'].browse(
            self.env.context.get('active_ids', [])))

    def action_grant(self):
        self.ensure_one()
        portal_group = self.env.ref('base.group_portal')
        Users = self.env['res.users'].with_context(no_reset_password=True)
        granted = self.env['school.guardian']
        for guardian in self.guardian_ids:
            if guardian.user_id:
                continue
            if not guardian.email:
                raise UserError(_('Guardian "%s" has no email address; cannot grant portal access.') % guardian.name)
            existing_user = self.env['res.users'].sudo().search([('login', '=', guardian.email)], limit=1)
            if existing_user:
                if not existing_user.share:
                    raise UserError(_(
                        'A non-portal (internal) user already exists with the email "%s". '
                        'Portal access cannot be granted to an internal account.') % guardian.email)
                user = existing_user
            else:
                user = Users.create({
                    'name': guardian.name,
                    'login': guardian.email,
                    'email': guardian.email,
                    'group_ids': [(6, 0, [portal_group.id])],
                })
            guardian.write({'user_id': user.id, 'portal_access_state': 'granted'})
            granted |= guardian
        granted.mapped('user_id').action_reset_password()
        return {'type': 'ir.actions.act_window_close'}
