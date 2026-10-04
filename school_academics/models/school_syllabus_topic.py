from odoo import fields, models


class SchoolSyllabusTopic(models.Model):
    _name = 'school.syllabus.topic'
    _description = 'Syllabus Topic'
    _order = 'standard_id, subject_id, planned_date'

    subject_id = fields.Many2one('school.subject', string='Subject', required=True)
    standard_id = fields.Many2one('school.standard', string='Standard', required=True)
    staff_id = fields.Many2one('school.staff', string='Teacher')
    unit_name = fields.Char(required=True)
    topic_name = fields.Char(required=True)
    planned_date = fields.Date()
    completed_date = fields.Date()
    state = fields.Selection(
        [
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='pending', required=True,
    )

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        self.write({'state': 'completed', 'completed_date': fields.Date.context_today(self)})
