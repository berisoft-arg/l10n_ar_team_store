from odoo import fields, models

class CrmTeam(models.Model):
    _inherit = "crm.team"

    # Campo manual para elegir el partner que representa la sucursal
    l10n_ar_afip_pos_partner_id = fields.Many2one(
        'res.partner', 
        string="Dirección Sucursal (Partner)",
        help="Seleccioná el Partner que tiene la dirección de este Punto de Venta."
    )