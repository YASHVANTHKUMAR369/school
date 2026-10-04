from odoo import fields, models


class SchoolLibraryBookCopy(models.Model):
    _name = 'school.library.book.copy'
    _description = 'Library Book Copy'

    book_id = fields.Many2one('school.library.book', string='Book', required=True, ondelete='cascade')
    accession_no = fields.Char(string='Accession Number', required=True)
    barcode = fields.Char()
    state = fields.Selection(
        [
            ('available', 'Available'),
            ('issued', 'Issued'),
            ('lost', 'Lost'),
            ('damaged', 'Damaged'),
        ],
        default='available', required=True,
    )

    _accession_no_uniq = models.Constraint(
        'UNIQUE (accession_no)', 'A book copy with this accession number already exists.')
