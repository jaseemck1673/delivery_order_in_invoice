# -*- coding: utf-8 -*-
""" Account Move Model"""

from odoo import models, fields, api


class AccountMove(models.Model):
    """" inherited account.move """
    _inherit = 'account.move'

    delivery_count = fields.Integer(string='Delivery Count', compute='_compute_delivery_count')

    def action_view_delivery_orders(self):
        """ Action method for delivery orders"""
        return self._get_action_view_delivery(self.line_ids.sale_line_ids.order_id.picking_ids)

    def _compute_delivery_count(self):
        for record in self:
            record.delivery_count = len(record.line_ids.sale_line_ids.order_id.picking_ids)

    def _get_action_view_delivery(self, deliveries):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id("stock.action_picking_tree_all")
        if len(deliveries) > 1:
            action['domain'] = [('id', 'in', deliveries.ids)]
        elif len(deliveries) == 1:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = deliveries.id
            action['view_id'] = self.env.ref('stock.view_picking_form').id
        return action
