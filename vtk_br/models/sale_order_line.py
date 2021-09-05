from odoo import fields, models, api

class SaleOrderLine(models.Model):
	_inherit="sale.order.line"

	discount = fields.Float(
        compute="_compute_discount_line",
        store=False,
        readonly=True,
    )


    @api.depends("order_id", "order_id.general_discount", "order_id.amount_untaxed")
    def _compute_discount_line(self):
        if hasattr(super(), "_compute_discount"):
            super()._compute_discount()
        for line in self:
            line.discount = line.order_id.general_discount

