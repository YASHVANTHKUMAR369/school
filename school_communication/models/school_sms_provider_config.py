import json
import logging
import urllib.request

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SchoolSmsProviderConfig(models.Model):
    _name = 'school.sms.provider.config'
    _description = 'SMS Provider Configuration'

    name = fields.Char(required=True)
    api_url = fields.Char(required=True, help='HTTP endpoint of the SMS gateway (MSG91, Kaleyra, Twilio, etc.)')
    api_key = fields.Char(required=True)
    sender_id = fields.Char()
    active = fields.Boolean(default=True)

    def send_sms(self, mobile, message):
        """Generic provider-agnostic HTTP dispatch. Any Indian SMS gateway that
        accepts a simple POST with mobile/message/sender/api-key can be wired
        in here without a dedicated vendor SDK."""
        self.ensure_one()
        payload = json.dumps({
            'mobile': mobile, 'message': message, 'sender_id': self.sender_id, 'api_key': self.api_key,
        }).encode()
        request = urllib.request.Request(
            self.api_url, data=payload, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status == 200
        except Exception:
            _logger.exception('Failed to send SMS via %s to %s', self.name, mobile)
            return False
