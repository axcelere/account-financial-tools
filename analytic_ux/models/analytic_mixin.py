# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools.float_utils import float_round

class AnalyticMixin(models.AbstractModel):
    _inherit = 'analytic.mixin'

    def _sanitize_values(self, vals, decimal_precision):
        """ Normalize the float of the distribution """
        if 'analytic_distribution' in vals:
            vals['analytic_distribution'] = vals.get('analytic_distribution') and {
                account_id: float_round(int(distribution), decimal_precision) for account_id, distribution in vals['analytic_distribution'].items()}
        return vals
