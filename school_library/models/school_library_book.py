from odoo import api, fields, models


class SchoolLibraryBook(models.Model):
    _name = 'school.library.book'
    _description = 'Library Book'

    title = fields.Char(required=True)
    author = fields.Char()
    isbn = fields.Char(string='ISBN')
    category_id = fields.Many2one('school.library.category', string='Category')
    publisher = fields.Char()
    edition = fields.Char()
    copy_ids = fields.One2many('school.library.book.copy', 'book_id', string='Copies')
    total_copies = fields.Integer(compute='_compute_total_copies')
    available_copies = fields.Integer(compute='_compute_total_copies')

    @api.depends('copy_ids.state')
    def _compute_total_copies(self):
        for rec in self:
            rec.total_copies = len(rec.copy_ids)
            rec.available_copies = len(rec.copy_ids.filtered(lambda c: c.state == 'available'))
