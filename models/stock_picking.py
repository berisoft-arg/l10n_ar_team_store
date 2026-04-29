from odoo import models, api, exceptions, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def default_get(self, fields_list):
        res = super(StockPicking, self).default_get(fields_list)
        # Obtenemos el equipo del usuario actual
        user_team = self.env['crm.team'].search([('member_ids', '=', self.env.user.id)], limit=1)
        
        if user_team:
            # Buscamos el almacén que tenga vinculado este equipo en el Many2many
            warehouse = self.env['stock.warehouse'].search([
                ('branch_team_ids', 'in', user_team.id)
            ], limit=1)
            
            if warehouse:
                # Buscamos el tipo de operación interno de ese almacén específico
                picking_type = self.env['stock.picking.type'].search([
                    ('code', '=', 'internal'),
                    ('warehouse_id', '=', warehouse.id)
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
        Si el destino es otra sucursal, cambiamos el picking_type_id para que
        aparezca en el tablero (Dashboard) de la sucursal que recibe.
        """
        if self.location_dest_id and self.picking_type_id.code == 'internal':
            dest_wh = self.location_dest_id.warehouse_id or self.location_dest_id.location_id.warehouse_id
            
            if dest_wh and dest_wh != self.picking_type_id.warehouse_id:
                new_type = self.env['stock.picking.type'].search([
                    ('code', '=', 'internal'),
                    ('warehouse_id', '=', dest_wh.id)
                ], limit=1)
                
                if new_type:
                    old_src = self.location_id
                    self.picking_type_id = new_type
                    # Mantenemos el origen (ej. AD) aunque cambie el tipo de operación
                    self.location_id = old_src

    @api.onchange('picking_type_id')
    def _onchange_picking_type_id_set_locations(self):
        """ Setea ubicaciones solo si están vacías para no pisar el onchange anterior """
        if self.picking_type_id:
            if not self.location_id:
                self.location_id = self.picking_type_id.default_location_src_id
            if not self.location_dest_id:
                self.location_dest_id = self.picking_type_id.default_location_dest_id

    def button_validate(self):
        """ Restricciones de seguridad para el entorno de sucursales """
        for picking in self:
            if picking.picking_type_id.code == 'internal':
                # 1. El que envía no puede validar la recepción
                if picking.create_uid == self.env.user:
                    raise exceptions.UserError(
                        _("Seguridad: El usuario que creó el envío no puede validar la recepción. "
                          "Debe hacerlo un responsable en el destino."))

                # 2. Solo usuarios vinculados al almacén de destino pueden validar
                dest_location = picking.location_dest_id
                dest_wh = dest_location.warehouse_id or dest_location.location_id.warehouse_id
                
                if not dest_wh:
                    raise exceptions.UserError(_("La ubicación de destino no está vinculada a un almacén."))

                # Verificamos si el equipo del usuario está en la lista de equipos del almacén destino
                user_team = self.env['crm.team'].search([('member_ids', '=', self.env.user.id)], limit=1)
                
                if not user_team or user_team not in dest_wh.branch_team_ids:
                    raise exceptions.UserError(
                        _("Acceso Denegado: Tu equipo (%s) no tiene permiso para validar en %s.") 
                        % (user_team.name if user_team else "Sin Equipo", dest_wh.name)
                    )
            
        return super(StockPicking, self).button_validate()