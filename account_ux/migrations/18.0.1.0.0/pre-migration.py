from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """
    The objective of this is delete the original view form the module how bring the functionality
    adding in the previous commit
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    view = env.ref("account_ux.view_account_form", raise_if_not_found=False)
    if view:
        view.unlink()
    # AXCELERE MIGRATION
    action = env.ref('account_ux.action_account_change_currency', raise_if_not_found=False)
    if action:
        action.unlink()
    view = env.ref("account_ux.view_account_change_no_exchange_currency", raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref("account_ux.view_account_change_currency", raise_if_not_found=False)
    if view:
        view.unlink()
