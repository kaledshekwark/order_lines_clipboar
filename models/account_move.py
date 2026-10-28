from odoo import Command, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'line.clipboard.mixin']

    def _clipboard_get_lines(self):
        return [{
            'product_id': line.product_id.id,
            'quantity': line.quantity,
            'uom_id': line.product_uom_id.id,
            'price_unit': line.price_unit,
        } for line in self.invoice_line_ids.filtered(lambda l: l.display_type == 'product' and l.product_id)]

    def _clipboard_check_can_paste(self):
        if not self.is_invoice(include_receipts=True):
            raise UserError(_("You can only paste lines into customer invoices, vendor bills or credit notes."))
        if self.state != 'draft':
            raise UserError(_("You can only paste lines into a draft invoice or bill."))

    def _clipboard_paste(self, clipboard):
        commands = []
        for line in clipboard:
            vals = {
                'display_type': 'product',
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'product_uom_id': (line.uom_id or line.product_id.uom_id).id,
            }
            # no price copied (e.g. from a transfer): let Odoo compute it from the product
            if line.price_unit:
                vals['price_unit'] = line.price_unit
            commands.append(Command.create(vals))
        # write through the move so accounts, taxes and totals are recomputed
        self.write({'invoice_line_ids': commands})
        return self.invoice_line_ids[-len(commands):]
