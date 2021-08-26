from odoo import models, fields


class ResPartner(models.Model):
	_inherit = "res.partner"

	litus_username = fields.Char("Litus Username")