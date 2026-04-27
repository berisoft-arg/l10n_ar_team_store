from odoo import models, api, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def default_get(self, fields_list):
        res = super(AccountMove, self).default_get(fields_list)
        # Solo para facturas de cliente o notas de crédito
        if res.get('move_type') in ('out_invoice', 'out_refund'):
            user_team = self.env.user.sale_team_id
            if user_team:
                jrnl = self.env['account.journal'].search([
                    ('type', '=', 'sale'),
                    ('branch_team_id', '=', user_team.id)
                ], limit=1)
                if jrnl:
                    res['journal_id'] = jrnl.id
        return res