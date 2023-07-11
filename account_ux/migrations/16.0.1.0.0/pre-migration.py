from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """
    """
    _logger.info('UPGRADE 15->16 AXCELERE')
    env.cr.execute("""
        UPDATE account_payment_method SET code = 'new_third_party_checks_origin' WHERE code = 'new_third_party_checks' AND payment_type = 'inbound';
    """)
    view = env.ref('account_ux.view_move_line_tree', raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref('account_ux.view_move_line_tree_grouped', raise_if_not_found=False)
    if view:
        view.unlink()


