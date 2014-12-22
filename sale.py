# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow

class SaleOrder(osv.Model):
    _inherit = 'sale.order'
    
    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._amount_all(cr, uid, ids, field_name, arg, context=context)

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'delivery_cost': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['delivery_cost'] = cur_obj.round(cr,uid,cur,order.xx_delivery_method.amount)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']+cur_obj.round(cr,uid,cur,order.xx_delivery_method.amount)
        return res
    
    
    _columns = {
        'xx_delivery_date': fields.date(string='Delivery date'),
        
        'xx_payment_method': fields.many2one('xx.payment.method',
                                             string='Payment method'),
        'xx_warranty_period': fields.many2one('xx.warranty.period',
                                              string='Warranty period'),
        'xx_delivery_method': fields.many2one('xx.delivery.method',
                                              string='Delivery method'),
    }
    
class DeliveryMethod(osv.Model):
    _name = 'xx.delivery.method'
    _rec_name = 'company'

    _columns = {
        'company': fields.char(size=128, string='company'),
        'amount': fields.float(string='Amount'),
        'sale_ids': fields.one2many('sale.order', 'xx_delivery_method',
                                    string='Sale orders')        
    }
    
    
class PaymentMethod(osv.Model):
    _name = 'xx.payment.method'
    
    _columns = {
        'name': fields.char(size=128, string='Name'),
        'writeoff': fields.boolean(string='Writeoff'),
        'sale_ids': fields.one2many('sale.order', 'xx_payment_method',
                                    string='Sale orders')
    }
    
class WarrantyPeriod(osv.Model):
    _name = 'xx.warranty.period'
    
    _rec_name = 'xx_name'
    
    def _get_years(self, cr, uid, context=None):
        res = []
        
        for item in range(1,10):
            res.append(('%s' % item, '%s Jaar' % item))

        return res
    
    _columns = { 
        'xx_name': fields.char(size=128, string='Manufacturer'),
        'xx_period': fields.selection(_get_years, string='Period'),
        'xx_amount': fields.float(string='Amount'),
    }