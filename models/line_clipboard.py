from odoo import api, fields, models, _
from odoo.exceptions import UserError


class LineClipboard(models.Model):
    _name = 'line.clipboard'
    _description = 'Copied Order Line'
    _order = 'sequence, id'

    user_id = fields.Many2one('res.users', required=True, default=lambda self: self.env.user, index=True, ondelete='cascade')
    sequence = fields.Integer(default=10)
    product_id = fields.Many2one('product.product', required=True, ondelete='cascade')
    quantity = fields.Float(digits='Product Unit', required=True)
    uom_id = fields.Many2one('uom.uom', string='Unit')
    price_unit = fields.Float(digits='Product Price')
    source = fields.Char(help="Document the line was copied from")

    @api.model
    def _get_user_lines(self):
        lines = self.search([('user_id', '=', self.env.uid)])
        if not lines:
            raise UserError(_("Your clipboard is empty. Use 'Copy Lines' on a sale order, purchase order, transfer or invoice first."))
        return lines

    @api.model
    def _set_user_lines(self, vals_list):
        """Replace the current user's clipboard content."""
        self.search([('user_id', '=', self.env.uid)]).unlink()
        return self.create(vals_list)

    @api.model
    def _notify(self, message, next_action):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': message,
                'type': 'success',
                'sticky': False,
                'next': next_action,
            },
        }


class LineClipboardMixin(models.AbstractModel):
    """Copy / paste of product lines, shared by sale orders, purchase orders and transfers."""
    _name = 'line.clipboard.mixin'
    _description = 'Line Clipboard Mixin'

    def _clipboard_get_lines(self):
        """Return a list of dicts (product_id, quantity, uom_id, price_unit) for the copy wizard."""
        raise NotImplementedError()

    def _clipboard_paste(self, clipboard):
        """Create document lines from the given line.clipboard records."""
        raise NotImplementedError()

    def _clipboard_check_can_paste(self):
        return True

    def action_open_copy_lines_wizard(self):
        self.ensure_one()
        lines = self._clipboard_get_lines()
        if not lines:
            raise UserError(_("This document has no product lines to copy."))
        wizard = self.env['line.copy.wizard'].create({
            'source': self.display_name,
            'line_ids': [(0, 0, dict(vals, selected=True)) for vals in lines],
        })
        return wizard._reopen()

    def action_paste_clipboard_lines(self):
        self.ensure_one()
        self._clipboard_check_can_paste()
        clipboard = self.env['line.clipboard']._get_user_lines()
        self._clipboard_paste(clipboard)
        return clipboard._notify(
            _("%s line(s) pasted.", len(clipboard)),
            {'type': 'ir.actions.client', 'tag': 'soft_reload'},
        )
