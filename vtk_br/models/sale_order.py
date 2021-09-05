from odoo import fields, models, api


class SaleOrder(models.Model):
	_inherit = "sale.order"

	state = fields.Selection(readonly=False)
	create_date_temp = fields.Datetime()
	contract_title = fields.Char()

	general_discount = fields.Float(
		string="Discount (%)",
		compute="_compute_general_discount",
		store=False,
		readonly=True,
		digits="Discount",
	)

	@api.depends('amount_untaxed', 'order_line', 'order_line.product_uom_qty')
	def _compute_general_discount(self):
		for so in self:
			if so.amount_untaxed >= 5000:
				so.general_discount = 5
				for line in so.order_line:
					line.discount = 5

	def print_contract(self):
		report_id = self.env["ir.actions.report"].search([["report_name","=","vtk_br.br_contract"]])
		pdf = report_id[0]._render_qweb_pdf(self.id)
		return pdf
	
