from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    contract_text = fields.Char(
        compute='_get_contract_text'
    )

    @api.depends('order_id')
    def _get_contract_text():
        for line in self:
            if line.product_id.contract_text:
                line.contract_text = line.product_id.contract_text
            else:
                line.contract_text = ""

