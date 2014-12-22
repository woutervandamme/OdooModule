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
    
    _columns = {
        'xx_delivery_date': fields.date(string='Delivery date'),
        #'xx_payment_method': fields.selection([('visa', 'Visa'),
        #                                       ('cash', 'Cash')],
        #                                      string='Payment method'),
        'xx_payment_method': fields.many2one('xx.payment.method',
                                             string='Payment method'),
        'xx_warranty_period': fields.many2one('xx.warranty.period',
                                              string='Warranty period'),
        'xx_delivery_method': fields.selection([('BPost', 'BPost'),
                                              ('cash', 'Cash')],
                                              string='Delivery method'),
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