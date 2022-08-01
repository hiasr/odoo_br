from odoo import models, fields, api
import markdown


class ProductTemplate(models.Model):
    _inherit = "product.template"

    contract_text = fields.Html("Contract Text", translate=True)
    invoice_description = fields.Char("Invoice Description")
    academic_year = fields.Integer("Academic Year")
    to_archive = fields.Boolean()
