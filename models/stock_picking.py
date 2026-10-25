from odoo import models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'line.clipboard.mixin']

    def _clipboard_get_lines(self):
        return [{
            'product_id': move.product_id.id,
            'quantity': move.product_uom_qty,
            'uom_id': move.product_uom.id,
            'price_unit': move.price_unit,
        } for move in self.move_ids.filtered(lambda m: m.state != 'cancel')]

    def _clipboard_check_can_paste(self):
        if self.state in ('done', 'cancel'):
            raise UserError(_("You cannot paste lines into a done or cancelled transfer."))

    def _clipboard_paste(self, clipboard):
        # read the state before adding draft moves, as they reset the computed picking state
        was_draft = self.state == 'draft'
        moves = self.env['stock.move'].create([{
            'picking_id': self.id,
            'product_id': line.product_id.id,
            'product_uom_qty': line.quantity,
            'product_uom': (line.uom_id or line.product_id.uom_id).id,
            'price_unit': line.price_unit,
        } for line in clipboard])
        if not was_draft:
            moves._action_confirm()
        return moves
