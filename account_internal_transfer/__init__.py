##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from . import models

import logging
import os
from odoo.sql_db import db_connect
from odoo.api import Environment, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def _post_load_hook():
    """ Ejecuta fix antes del upgrade completo """
    dbname = os.environ.get("DB_NAME")
    if not dbname:
        _logger.warning("[ceres_migration_fixes] DB_NAME not found in environment")
        return

    try:
        with db_connect(dbname).cursor() as cr:
            _logger.info("[ceres_migration_fixes] Dropping constraint account_payment_method_name_code_unique if exists...")
            cr.execute("""
                ALTER TABLE account_payment_method
                DROP CONSTRAINT IF EXISTS account_payment_method_name_code_unique;
            """)
            cr.commit()

        # Reabrimos la conexión con el mismo cursor para acceder a Odoo ORM
        with db_connect(dbname).cursor() as cr:
            env = Environment(cr, SUPERUSER_ID, {})
            _logger.info("[ceres_migration_fixes] Renaming duplicated codes in account.payment.method...")
            for rec in env['account.payment.method'].search([]):
                rec.code = f"{rec.code}-old-upg"
            cr.commit()

        _logger.info("[ceres_migration_fixes] Constraint dropped and codes renamed.")

    except Exception as e:
        _logger.exception("[ceres_migration_fixes] Error during post_load_hook: %s", e)
