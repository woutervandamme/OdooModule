
from datetime import datetime, timedelta
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow
from unittest.util import _ordered_count

class AccountInvoice(osv.Model):
    _inherit = 'account.invoice'
        
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line),
        self.amount_tax = sum(line.amount for line in self.tax_line),
        self.amount_total = self.amount_untaxed + self.amount_tax + self.xx_delivery_price

    _columns = {
            'xx_delivery_method' : fields.many2one('xx.delivery.method',string='Delivery method'),
            'xx_delivery_price' : fields.float(string="Delivery price")
              
    }
    
    
    