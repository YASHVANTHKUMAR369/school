from odoo import fields, models


class SchoolCommunicationLog(models.Model):
    _name = 'school.communication.log'
    _description = 'Communication Log'
    _order = 'create_date desc'

    notice_id = fields.Many2one('school.notice', string='Notice', ondelete='cascade')
    channel = fields.Selection([('email', 'Email'), ('sms', 'SMS')], required=True)
    recipient_partner_id = fields.Many2one('school.guardian', string='Recipient Guardian')
    recipient_mobile = fields.Char()
    status = fields.Selection(
        [('sent', 'Sent'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending', required=True)
    sent_date = fields.Datetime()
    error_message = fields.Char()
