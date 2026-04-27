from odoo import models, api, exceptions, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def default_get(self, fields_list):
        res = super(StockPicking, self).default_get(fields_list)
        user_team = self.env['crm.team'].search([('member_ids', '=', self.env.user.id)], limit=1)
        
        if user_team and user_team.l10n_ar_afip_pos_partner_id:
            partner_id = user_team.l10n_ar_afip_pos_partner_id.id
            picking_type = self.env['stock.picking.type'].search([
                ('code', '=', 'internal'),
                ('warehouse_id.partner_id', '=', partner_id)
            ], limit=1)
            
            if picking_type:
                res.update({
                    'picking_type_id': picking_type.id,
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id': picking_type.default_location_dest_id.id,
                })
        return res

    @api.onchange('location_dest_id')
    def _onchange_location_dest_id_switch_dashboard(self):
        """
        Si el destino cambia a otra sucursal, pasamos el picking al tablero 
        de destino para que el receptor vea el aviso de mercadería entrante.
        """
        if self.location_dest_id and self.picking_type_id.code == 'internal':
            # Buscamos el almacén de destino
            dest_wh = self.location_dest_id.warehouse_id or self.location_dest_id.location_id.warehouse_id
            
            # Si el destino es un almacén distinto al del tipo de operación actual
            if dest_wh and dest_wh != self.picking_type_id.warehouse_id:
                new_type = self.env['stock.picking.type'].search([
                    ('code', '=', 'internal'),
                    ('warehouse_id', '=', dest_wh.id)
                ], limit=1)
                
                if new_type:
                    # Guardamos el origen actual para que no lo pise el onchange de picking_type
                    old_src = self.location_id
                    self.picking_type_id = new_type
                    # Forzamos a mantener el origen de AD
                    self.location_id = old_src

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id_set_locations(self):
        if self.picking_type_id:
            # Solo seteamos si están vacíos para no pisar el cambio de sucursal
            if not self.location_id:
                self.location_id = self.picking_type_id.default_location_src_id
            if not self.location_dest_id:
                self.location_dest_id = self.picking_type_id.default_location_dest_id

    def button_validate(self):
        for picking in self:
            if picking.picking_type_id.code == 'internal':
                # Bloqueo de auto-validación
                if picking.create_uid == self.env.user:
                    raise exceptions.UserError(
                        _("Control: No podés validar lo que vos mismo enviaste. "
                          "Debe validar el personal de la sucursal de destino."))

                # Validación de pertenencia a sucursal de destino
                dest_location = picking.location_dest_id
                dest_wh = dest_location.warehouse_id or dest_location.location_id.warehouse_id
                
                if not dest_wh or not dest_wh.partner_id:
                    raise exceptions.UserError(_("El almacén de destino no tiene sucursal asignada."))

                user_teams = self.env['crm.team'].search([('member_ids', '=', self.env.user.id)])
                user_branch_partners = user_teams.mapped('l10n_ar_afip_pos_partner_id')

                if dest_wh.partner_id not in user_branch_partners:
                    raise exceptions.UserError(
                        _("Solo los usuarios de la sucursal destino (%s) pueden validar.") % dest_wh.partner_id.name)
            
        return super(StockPicking, self).button_validate()