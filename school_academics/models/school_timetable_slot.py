from odoo import fields, models


class SchoolTimetableSlot(models.Model):
    _name = 'school.timetable.slot'
    _description = 'Timetable Slot'
    _order = 'section_id, day_of_week, period_no'

    section_id = fields.Many2one('school.section', string='Section', required=True, ondelete='cascade')
    standard_id = fields.Many2one(related='section_id.standard_id', store=True)
    day_of_week = fields.Selection(
        [
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
        ],
        required=True,
    )
    period_no = fields.Integer(required=True)
    time_from = fields.Float(string='From')
    time_to = fields.Float(string='To')
    subject_id = fields.Many2one('school.subject', string='Subject', required=True)
    staff_id = fields.Many2one('school.staff', string='Teacher', required=True)

    _section_slot_uniq = models.Constraint(
        'UNIQUE (section_id, day_of_week, period_no)',
        'This section already has a subject scheduled for this period.')
    _staff_slot_uniq = models.Constraint(
        'UNIQUE (staff_id, day_of_week, period_no)',
        'This teacher is already scheduled for another section in this period.')
