from odoo import _, api, models
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("team_id")
    def _compute_warehouse_id(self):
        # Primero ejecutamos el original para que cargue los valores por defecto
        super()._compute_warehouse_id()
        for sale in self:
            # Si hay equipo y tiene el partner de sucursal
            if sale.team_id and sale.team_id.l10n_ar_afip_pos_partner_id:
                warehouse = self.env["stock.warehouse"].search([
                    ('partner_id', '=', sale.team_id.l10n_ar_afip_pos_partner_id.id)
                ], limit=1)
                if warehouse:
                    sale.warehouse_id = warehouse.id

    # AGREGAMOS ESTO: Forzamos la actualización inmediata en la interfaz
    @api.onchange('team_id')
    def _onchange_team_id_warehouse(self):
        if self.team_id and self.team_id.l10n_ar_afip_pos_partner_id:
            warehouse = self.env["stock.warehouse"].search([
                ('partner_id', '=', self.team_id.l10n_ar_afip_pos_partner_id.id)
            ], limit=1)
            if warehouse:
                self.warehouse_id = warehouse.id

    @api.constrains("team_id", "warehouse_id")
    def _check_wh_branch_team(self):
        for rec in self:
            if (rec.team_id.l10n_ar_afip_pos_partner_id and 
                rec.warehouse_id.partner_id and 
                rec.team_id.l10n_ar_afip_pos_partner_id != rec.warehouse_id.partner_id):
                raise ValidationError(
                    _("El almacén seleccionado (%s) no pertenece a la dirección de la sucursal del equipo (%s).") 
                    % (rec.warehouse_id.name, rec.team_id.name)
                )

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        if self.team_id and self.team_id.l10n_ar_afip_pos_partner_id:
            jrnl = self.env['account.journal'].search([
                ('type', '=', 'sale'),
                ('l10n_ar_afip_pos_partner_id', '=', self.team_id.l10n_ar_afip_pos_partner_id.id)
            ], limit=1)
            if jrnl:
                res['journal_id'] = jrnl.id
        return res