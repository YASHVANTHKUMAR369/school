from odoo import api, fields, models

SEQUENCE_CODE_BY_TYPE = {
    'tc': 'school.certificate.tc',
    'bonafide': 'school.certificate.bonafide',
    'id_card': 'school.certificate.id_card',
}


class SchoolCertificate(models.Model):
    _name = 'school.certificate'
    _description = 'Certificate'
    _inherit = ['mail.thread']
    _order = 'issue_date desc'

    certificate_type = fields.Selection(
        [('tc', 'Transfer Certificate'), ('bonafide', 'Bonafide Certificate'), ('id_card', 'ID Card')],
        required=True, default='bonafide',
    )
    certificate_no = fields.Char(readonly=True, copy=False)
    student_id = fields.Many2one('school.student', string='Student', required=True)
    academic_year_id = fields.Many2one('school.academic.year', string='Academic Year', required=True)
    issue_date = fields.Date(default=fields.Date.context_today, required=True)
    reason = fields.Text(string='Reason for Leaving')
    whole_school_attendance = fields.Float(string='Attendance %')
    conduct = fields.Selection(
        [('excellent', 'Excellent'), ('good', 'Good'), ('satisfactory', 'Satisfactory')])
    qualified_for_promotion = fields.Boolean(default=True)
    last_class_studied = fields.Char()
    date_of_leaving = fields.Date()
    state = fields.Selection(
        [('draft', 'Draft'), ('issued', 'Issued'), ('cancelled', 'Cancelled')],
        default='draft', required=True, tracking=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            cert_type = vals.get('certificate_type', 'bonafide')
            code = SEQUENCE_CODE_BY_TYPE.get(cert_type)
            if code and not vals.get('certificate_no'):
                vals['certificate_no'] = self.env['ir.sequence'].next_by_code(code) or '/'
        return super().create(vals_list)

    def action_issue(self):
        self.ensure_one()
        self.write({'state': 'issued'})
        if self.certificate_type == 'tc':
            self.student_id.write({'state': 'tc_issued', 'active': False})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
