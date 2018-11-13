# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, api,fields, models, _
        
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    picking_code = fields.Selection('stock.picking.type', related='picking_type_id.code', string='Code')

    @api.multi
    def print_deliveryorder(self, data):
        return self.env.ref('delivery_note_report.delivery_note_report_unique').report_action(self)

    @api.multi
    def get_lotNumber(self,line):
        lot_numbers = []
        for poid in line.move_line_ids:
            lot_numbers.append(poid.lot_id.name)
        if lot_numbers:
            return ','.join(set(lot_numbers))
        return ''

    def get_invoice_address(self):
        sale_id = self.env['sale.order'].search([('name','=',self.origin)])
        if sale_id:
            return sale_id.partner_invoice_id

    def get_delivery_address(self):
        sale_id = self.env['sale.order'].search([('name','=',self.origin)])
        if sale_id: 
            return sale_id.partner_shipping_id

    def get_total_net_weight(self):
        total = 0.0
        for moveline in self.move_lines:
            total += moveline.product_id.net_weight
        return str(total)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    net_weight = fields.Float(string='Net Weight')

class ProductTemplateInh(models.Model):
    _inherit = 'product.template'
    
    custom_tarrif = fields.Char(string='Custom Tarrif No.')

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def print_invoiceyorder(self, data):
        return self.env.ref('delivery_note_report.invoice_report_unique').report_action(self)

    @api.multi
    def get_lot_num(self,product_id):
        lot_numbers = []
        if self.origin:
            
            sale_id = self.env['sale.order'].search([('name','=',self.origin)])
            if sale_id:
                for picking_id in sale_id.picking_ids:
                    if picking_id.pack_operation_product_ids:
                        for poid in picking_id.pack_operation_product_ids:
                            if poid.product_id.id == product_id.id:
                                if poid.pack_lot_ids:
                                    for p_lot_id in poid.pack_lot_ids:
                                        if p_lot_id.lot_id:
                                            lot_numbers.append(p_lot_id.lot_id.name)
        if lot_numbers:
            return ','.join(set(lot_numbers))
        return ''




class ResPartnerReport(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def get_bank_account(self,currency_id):
        bank_data = self.env['res.partner.bank'].search([('partner_id', '=', self.id),('currency_id', '=', currency_id.id)])
        return bank_data