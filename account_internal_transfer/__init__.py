##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from . import models

import logging
import os
from odoo.sql_db import db_connect
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def post_load_hook():
    """ Ejecuta fix antes del upgrade completo usando el env correcto """
    _logger.info("[ceres_migration_fixes] Running post_load_hook for constraint drop and code fix")

    # Odoo garantiza que en este punto el Registry ya está inicializado
    from odoo.modules.registry import Registry
    for dbname in Registry.registries:
        registry = Registry.registries[dbname]
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})

            # 1. Dropear la constraint si existe
            _logger.info("[ceres_migration_fixes] Dropping constraint if exists...")
            cr.execute("""
                ALTER TABLE account_payment_method
                DROP CONSTRAINT IF EXISTS account_payment_method_name_code_unique;
            """)

            # 2. Renombrar códigos duplicados o problemáticos
            _logger.info("[ceres_migration_fixes] Renaming codes in account.payment.method...")
            for rec in env['account.payment.method'].search([]):
                rec.code = f"{rec.code}-old-upg"

            cr.commit()
            _logger.info("[ceres_migration_fixes] Done with post_load_hook for db: %s", dbname)
