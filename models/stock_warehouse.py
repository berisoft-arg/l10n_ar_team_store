from odoo import models, fields

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    branch_team_ids = fields.Many2many(
        'crm.team', 
        string='Equipos Vinculados', 
        help="Equipos de venta que tienen permitido operar y mapear este almacén por defecto."
    )