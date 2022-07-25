from odoo import api, models, fields
from datetime import datetime, timedelta


class ResPartner(models.Model):
    _inherit = "res.partner"

    litus_username = fields.Char("Litus Username")
    main_contact = fields.Boolean("Main Contact Person")
    spendings = fields.Monetary(compute="_compute_spendings")

    @api.depends("child_ids.sale_order_ids")
    def _compute_spendings(self):
        for record in self:
            spendings = 0
            if record.is_company:
                for contact in record.child_ids:
                    for so in contact.sale_order_ids:
                        if datetime.now() < so.create_date + timedelta(
                            days=365
                        ) and so.state in ["done", "sale"]:
                            spendings += so.amount_untaxed
            record.spendings = spendings
