from odoo import fields, models


class SchoolStaff(models.Model):
    _inherit = 'school.staff'

    department_id = fields.Many2one('school.department', string='Department')
    designation_id = fields.Many2one('school.designation', string='Designation')
    date_of_joining = fields.Date()
    employment_type = fields.Selection(
        [
            ('permanent', 'Permanent'),
            ('contract', 'Contract'),
            ('probation', 'Probation'),
        ],
        default='permanent',
    )
    pan_no = fields.Char(string='PAN Number')
    bank_name = fields.Char()
    bank_account_no = fields.Char()
    ifsc_code = fields.Char(string='IFSC Code')
    basic_salary = fields.Float()
    payslip_ids = fields.One2many('school.payslip', 'staff_id', string='Payslips')
