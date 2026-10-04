from odoo import api, fields, models


class SchoolConfig(models.Model):
    """Singleton-style record holding the school's letterhead/profile data.

    Every QWeb PDF report in the suite (report cards, TC, Bonafide, ID
    cards, fee receipts, ...) reads this record for consistent branding
    instead of relying on the generic Settings app (which lives in the
    base_setup module that this suite deliberately does not depend on).
    """
    _name = 'school.config'
    _description = 'School Configuration'

    name = fields.Char(string='School Name', required=True, default='My School')
    address = fields.Text(string='Address')
    logo = fields.Image(string='Logo', max_width=1024, max_height=1024)
    udise_code = fields.Char(string='UDISE Code')
    affiliation_no = fields.Char(string='Affiliation Number')
    principal_name = fields.Char(string='Principal Name')
    principal_signature = fields.Image(string='Principal Signature', max_width=512, max_height=512)

    @api.model
    def get_config(self):
        config = self.search([], limit=1)
        if not config:
            config = self.create({'name': 'My School'})
        return config
