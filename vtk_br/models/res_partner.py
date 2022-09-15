from odoo import api, models, fields, modules
import logging
from datetime import datetime, timedelta
import pandas as pd
from ..lib import litus
import os

_logger = logging.getLogger(__name__)
API_KEY = os.getenv("API_KEY")


class ResPartner(models.Model):
    _inherit = "res.partner"

    litus_username = fields.Char("Litus Username")
    litus_id = fields.Integer("Litus ID")

    contact_type = fields.Selection(
        string="Contact Type",
        selection=[("main_contact", "Main Contact"), ("contact", "Contact")],
    )

    spendings = fields.Monetary(compute="_compute_spendings", store=True)

    @api.model
    def create(self, vals):
        result = super(ResPartner, self).create(vals)
        if result.is_company:
            litus.create_company(result.name)
        else:
            if not result.email:
                raise Warning("Contact should have an email")
            litus.create_contact(
                result.name, result.email, result.parent_id.get_company_id_litus()
            )
        return result

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

    def create_company_litus(self):
        id = litus.create_company(self.name)
        self.litus_id = id
        return id

    def get_company_id_litus(self):
        if self.litus_id:
            return self.litus_id

        id = litus.get_company_id(self.name)
        if id is not None:
            return id
        else:
            return self.create_company_litus()

    def create_contact_litus(self):
        id = litus.create_company(self.name)
        _logger.info(f"Created new contact with id {id}")
        self.litus_id = id
        return id

    def get_contact_id_litus(self):
        if self.litus_id:
            return self.litus_id

        company_id = self.parent_id.get_company_id_litus()
        _logger.info(f"Company id is {company_id}")
        return litus.create_contact(self.name, self.email, company_id)

    @api.model
    def send_activation_link(self, records):
        for record in records:
            if record.is_company:
                continue

            litus_id = record.get_contact_id_litus()
            _logger.info(
                f"Sending activation link for {record.name} with id {litus_id}"
            )
            litus.send_activation(litus_id)
