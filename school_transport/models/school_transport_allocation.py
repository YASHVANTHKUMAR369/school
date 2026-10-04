from odoo import fields, models


class SchoolTransportAllocation(models.Model):
    _name = 'school.transport.allocation'
    _description = 'Student Transport Allocation'

    student_id = fields.Many2one('school.student', string='Student', required=True, ondelete='cascade')
    academic_year_id = fields.Many2one('school.academic.year', string='Academic Year', required=True)
    route_id = fields.Many2one('school.transport.route', string='Route', required=True)
    stop_id = fields.Many2one(
        'school.transport.stop', string='Stop', required=True,
        domain="[('route_id', '=', route_id)]")
    state = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')], default='active', required=True)

    _student_year_uniq = models.Constraint(
        'UNIQUE (student_id, academic_year_id)',
        'This student already has a transport allocation for this academic year.')
