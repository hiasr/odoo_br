from odoo import fields, models


class SaleOrder(models.Model):
	_inherit = "sale.order"

	state = fields.Selection(readonly=False)
	create_date_temp = fields.Datetime()