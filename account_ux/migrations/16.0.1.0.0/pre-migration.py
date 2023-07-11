from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """
    """
    view = env.ref('account_ux.view_move_line_tree', raise_if_not_found=False)
    if view:
        view.unlink()
    view = env.ref('account_ux.view_move_line_tree_grouped', raise_if_not_found=False)
    if view:
        view.unlink()
