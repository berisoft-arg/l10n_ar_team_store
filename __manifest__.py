{
    'name': 'Sucursales por Equipo de Ventas (Argentina)',
    'version': '17.0.1.1.0',
    'category': 'Localization/Argentina',
    'author': 'Ariel Ameghino/Berisoft',
    'summary': 'Gestión de sucursales basada en Equipos de Venta para Ventas, Facturación e Inventario.',
    'description': """
Gestión de Sucursales para Odoo 17 (Argentina)
==============================================
Este módulo automatiza la asignación de sucursales y restringe la validación de stock según el equipo de ventas:

Funcionalidades principales:
---------------------------
* **Ventas:** Mapeo automático de Almacén en Sale Orders basado en el Equipo de Ventas.
* **Facturación:** Selección automática del Diario de Ventas correspondiente a la sucursal del equipo.
* **Inventario (Seguridad):** - Restringe la validación de transferencias internas: solo el personal de la sucursal de destino puede validar.
    - Control de dualidad: el usuario que crea un traslado no puede validarlo (evita auto-validación).
* **Mapeo de Pickings:** Configura automáticamente el Tipo de Operación y Ubicaciones de origen/destino según el equipo del usuario en nuevos registros.
* **Reportes:** Incluye datos de la Sucursal de Despacho en los formatos de impresión de Pedidos de Venta.
    """,
    'depends': [
        'sale_management', 
        'sales_team', 
        'stock', 
        'account', 
        'l10n_ar'
    ],
    'data': [
        'security/ir_rule.xml',
        'views/account_journal_views.xml',
        'views/stock_warehouse_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/crm_team_views.xml',
        'report/sale_report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}