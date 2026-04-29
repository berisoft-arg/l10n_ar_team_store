Sucursales por Equipo de Ventas (Argentina)


Gestión de Sucursales para Odoo (Argentina)
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
