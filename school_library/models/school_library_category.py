from odoo import fields, models


class SchoolLibraryCategory(models.Model):
    _name = 'school.library.category'
    _description = 'Library Book Category'

    name = fields.Char(required=True)
