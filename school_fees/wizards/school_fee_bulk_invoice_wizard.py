from odoo import fields, models


class SchoolFeeBulkInvoiceWizard(models.TransientModel):
    _name = 'school.fee.bulk.invoice.wizard'
    _description = 'Bulk Generate Fee Invoices'

    structure_id = fields.Many2one('school.fee.structure', string='Fee Structure', required=True)
    due_date = fields.Date(required=True, default=fields.Date.context_today)

    def action_generate(self):
        self.ensure_one()
        structure = self.structure_id
        students = self.env['school.student'].search([
            ('standard_id', '=', structure.standard_id.id),
            ('academic_year_id', '=', structure.academic_year_id.id),
            ('state', '=', 'active'),
        ])
        Invoice = self.env['school.fee.invoice']
        created = Invoice
        for student in students:
            invoice = Invoice.create({
                'student_id': student.id,
                'academic_year_id': structure.academic_year_id.id,
                'due_date': self.due_date,
                'line_ids': [(0, 0, {
                    'fee_head_id': line.fee_head_id.id,
                    'amount': line.amount,
                }) for line in structure.line_ids],
            })
            invoice.action_post()
            created |= invoice
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'school.fee.invoice',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created.ids)],
        }
