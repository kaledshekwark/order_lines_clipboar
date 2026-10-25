from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'line.clipboard.mixin']

    def _clipboard_get_lines(self):
        return [{
            'product_id': line.product_id.id,
            'quantity': line.product_uom_qty,
            'uom_id': line.product_uom_id.id,
            'price_unit': line.price_unit,
        } for line in self.order_line.filtered(lambda l: not l.display_type and l.product_id)]

    def _clipboard_check_can_paste(self):
        if self.state == 'cancel' or self.locked:
            raise UserError(_("You cannot paste lines into a cancelled or locked order."))

    def _clipboard_paste(self, clipboard):
        vals_list = []
        for line in clipboard:
            vals = {
                'order_id': self.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.quantity,
                'product_uom_id': (line.uom_id or line.product_id.uom_id).id,
            }
            # no price copied (e.g. from a transfer): let Odoo compute it from the pricelist
            if line.price_unit:
                vals['price_unit'] = line.price_unit
            vals_list.append(vals)
        return self.env['sale.order.line'].create(vals_list)
