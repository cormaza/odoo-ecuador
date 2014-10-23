# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Christopher Ormaza, Ecuadorenlinea.net
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp import netsvc
from datetime import date, datetime, timedelta
import openerp.addons.decimal_precision as dp

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import config
from openerp.tools.translate import _
from openerp import models, fields, api, _

class account_invoice_tax(models.Model):
    
    _inherit = 'account.invoice.tax' 
    
    type_ec = fields.Selection([
                    ('iva','IVA'),
                    ('renta','Renta'),
                    ('ice','ICE'),
                    ('other','Otro'),
                     ], String='Ecuadorian Type')
    assets = fields.Boolean(String="Assets")
    imports = fields.Boolean(String="Imports")
    exports = fields.Boolean(String="Exports")
    
    @api.v8
    def compute(self, invoice):
        tax_obj = self.env['account.tax']
        res = super(account_invoice_tax, self).compute(invoice)
        if isinstance(res, dict):
            for key in res.keys():
                criteria = []
                if res[key].get('base_code_id'):
                    criteria += [('base_code_id','=', res[key].get('base_code_id'))]
                if res[key].get('tax_code_id'):
                    criteria += [('tax_code_id','=', res[key].get('tax_code_id'))]
                if criteria:
                    tax = tax_obj.search(criteria, limit=1)
                    if tax:
                        res[key].update({
                                         'type_ec': tax.type_ec,
                                         })
        return res

account_invoice_tax()

