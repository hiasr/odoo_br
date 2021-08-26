from odoo import models, fields


class ProductTemplate(models.Model):
	_inherit = 'product.template'
	
	contract_text = fields.Char("Text to put on Contract")