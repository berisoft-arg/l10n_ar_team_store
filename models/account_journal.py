from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # Un diario puede pertenecer a varios equipos
    authorized_team_ids = fields.Many2many(
        'crm.team', 
        'journal_team_rel', 
        'journal_id', 
        'team_id', 
        string='Equipos Autorizados',
        help="Si se deja vacío, el diario es global."
    )