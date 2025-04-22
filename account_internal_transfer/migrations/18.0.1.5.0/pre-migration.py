from odoo import SUPERUSER_ID, api
import logging
_logger = logging.getLogger(__name__)

def migrate(cr, version):
    """
    The objective of this is delete the original view form the module how bring the functionality
    adding in the previous commit
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info('DROP CONSTRAINT IF EXISTS account_payment_method_name_code_unique')
    env.cr.execute('''
        ALTER TABLE account_payment_method
        DROP CONSTRAINT IF EXISTS account_payment_method_name_code_unique;
    ''')
    for rec in env['account.payment.method'].search([]):
        rec.write({'code': '%s-%s' % (rec.code, 'old')})
