from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(readonly=False)
    contract_title = fields.Char()
    partner_contract = fields.Boolean()
    working_year = fields.Integer(compute="_compute_working_year")

    general_discount = fields.Float(
        string="Discount (%)",
        compute="_compute_general_discount",
        store=False,
        readonly=True,
        digits="Discount",
    )

    @api.depends("create_date")
    def _compute_working_year(self):
        for so in self:
            cd = so.create_date
            if cd.month < 8:
                so.working_year = so.year - 1
            else:
                so.working_year = so.year

    @api.depends("amount_untaxed", "order_line", "order_line.product_uom_qty")
    def _compute_general_discount(self):
        for so in self:
            if so.amount_untaxed >= 6000 or so.partner_contract:
                so.general_discount = 5
                for line in so.order_line:
                    line.discount = 5
            else:
                so.general_discount = 0
                for line in so.order_line:
                    line.discount = 0

    def print_contract(self):
        report_id = self.env["ir.actions.report"].search(
            [["report_name", "=", "vtk_br.br_contract"]]
        )
        pdf = report_id[0]._render_qweb_pdf(self.id)
        return pdf
