from odoo import models, fields

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    branch_team_id = fields.Many2one('crm.team', string='Equipo Sucursal', help="Si se setea, este almacén pertenece a esta sucursal.")