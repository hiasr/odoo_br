from odoo import api, models, fields, modules
import logging
from datetime import datetime, timedelta
import pandas as pd
import os

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    litus_username = fields.Char("Litus Username")

    contact_type = fields.Selection(
        string="Contact Type",
        selection=[("main_contact", "Main Contact"), ("contact", "Contact")],
    )

    spendings = fields.Monetary(compute="_compute_spendings", store=True)

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

    @api.model
    def download_mailmerge(self, records):
        df = pd.DataFrame(columns=["Bedrijf", "Naam", "Email", "cc"])

        for index in range(len(records)):
            df.loc[index, "Bedrijf"] = records[index].name
            df.loc[index, "Email"] = records[index].email
            cc_emails = list()

            for contact in records[index].child_ids:
                if contact.contact_type == "main_contact":
                    df.loc[index, "Naam"] = contact.name
                    df.loc[index, "Email"] = contact.email
                elif contact.contact_type == "contact":
                    cc_emails.append(contact.email)
            df.loc[index, "cc"] = ";".join(cc_emails)

        module_path = modules.get_module_path("vtk_br")
        filename = datetime.now().strftime("Mailmerge%H_%M_%S__%d_%m_%Y.csv")
        _logger.info(f"Saving mailmerge to {module_path}")
        df.to_csv(f"{module_path}/static/mailmerges/{filename}")

        return {
            "type": "ir.actions.act_url",
            "url": f"/vtk_br/static/mailmerges/{filename}",
            "target": "new",
        }
