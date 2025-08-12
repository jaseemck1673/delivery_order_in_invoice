# -*- coding: utf-8 -*-
""" Account Move Model"""
from odoo import models, fields


class AccountMove(models.Model):
    """" inherited account.move """
    _inherit = 'account.move'

    delivery_count = fields.Integer(string='Delivery Count', compute='_compute_delivery_count')

    def action_view_delivery_orders(self):
        """ Action method for delivery orders"""
        return self._get_action_view_delivery(self.line_ids.sale_line_ids.move_ids.move_line_ids)

    def _compute_delivery_count(self):
        for record in self:
            products = record.line_ids.product_id
            delivery_line_id = record.line_ids.sale_line_ids.move_ids.move_line_ids
            picking_ids = delivery_line_id.filtered(lambda rec: rec.product_id in products)
            record.delivery_count = len(picking_ids.picking_id)

    def _get_action_view_delivery(self, delivery_line_ids):
        self.ensure_one()
        products = self.line_ids.product_id
        stock_move_ids = delivery_line_ids.filtered(lambda rec: rec.product_id in products)
        action = self.env['ir.actions.actions']._for_xml_id("stock.action_picking_tree_all")
        if len(stock_move_ids.picking_id) > 1:
            action['domain'] = [('id', 'in', stock_move_ids.picking_id.ids)]
        elif len(stock_move_ids.picking_id) == 1:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = stock_move_ids.picking_id.id
            action['view_id'] = self.env.ref('stock.view_picking_form').id
        return action
