from odoo import fields, models, _
from odoo.exceptions import UserError


class LineCopyWizard(models.TransientModel):
    _name = 'line.copy.wizard'
    _description = 'Copy Lines'

    source = fields.Char(readonly=True)
    line_ids = fields.One2many('line.copy.wizard.line', 'wizard_id')

    def _reopen(self):
        return {
            'name': _("Copy Lines"),
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_select_all(self):
        self.line_ids.selected = True
        return self._reopen()

    def action_unselect_all(self):
        self.line_ids.selected = False
        return self._reopen()

    def action_copy(self):
        self.ensure_one()
        selected = self.line_ids.filtered('selected')
        if not selected:
            raise UserError(_("Select at least one line to copy."))
        Clipboard = self.env['line.clipboard']
        Clipboard._set_user_lines([{
            'sequence': index,
            'product_id': line.product_id.id,
            'quantity': line.quantity,
            'uom_id': line.uom_id.id,
            'price_unit': line.price_unit,
            'source': self.source,
        } for index, line in enumerate(selected)])
        return Clipboard._notify(
            _("%(count)s line(s) copied from %(source)s. Open a sale order, purchase order or transfer and click 'Paste Lines'.",
              count=len(selected), source=self.source),
            {'type': 'ir.actions.act_window_close'},
        )


class LineCopyWizardLine(models.TransientModel):
    _name = 'line.copy.wizard.line'
    _description = 'Copy Lines - Line'

    wizard_id = fields.Many2one('line.copy.wizard', required=True, ondelete='cascade')
    selected = fields.Boolean(string='Copy')
    product_id = fields.Many2one('product.product', required=True, readonly=True)
    quantity = fields.Float(digits='Product Unit', readonly=True)
    uom_id = fields.Many2one('uom.uom', string='Unit', readonly=True)
    price_unit = fields.Float(string='Unit Price', digits='Product Price', readonly=True)
