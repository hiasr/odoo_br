from odoo import models, fields


class ProductTemplate(models.Model):
	_inherit = 'product.template'
	
	contract_text = fields.Char("Contract Text")
	invoice_description = fields.Char("Invoice Description")