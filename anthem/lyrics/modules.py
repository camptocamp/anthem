# Copyright 2016-2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from ..exceptions import AnthemError


def uninstall(ctx, module_list):
    """uninstall module"""
    if not module_list:
        raise AnthemError("You have to provide a list of " "module's name to uninstall")

    mods = ctx.env["ir.module.module"].search(
        [
            ("name", "in", module_list),
            ("state", "not in", ["uninstalled", "uninstallable"]),
        ]
    )
    try:
        mods.button_immediate_uninstall()
    except Exception:
        raise AnthemError("Cannot uninstall modules. See the logs")


def update_translations(ctx, module_list, overwrite=False):
    """Update translations from module list"""
    if not isinstance(module_list, list):
        raise AnthemError(
            "You have to provide a list of " "module's name to update the translations"
        )
    if overwrite:
        ctx.log_line("All previous translations will be dropped for requested addons")
        nuke_translations(ctx, module_list)
    ir_module = ctx.env["ir.module.module"]
    if hasattr(ir_module, "update_translations"):
        # Odoo version <= 10.0
        method_name = "update_translations"
    else:
        # Odoo version >= 11.0
        method_name = "_update_translations"

    domain = [("name", "in", module_list)]
    mods = ctx.env["ir.module.module"].search(domain)
    ctx.log_line("Reloading translations for %s" % str(module_list))
    mods.with_context(overwrite=overwrite)
    getattr(mods, method_name)()


def nuke_translations(ctx, module_list):
    """Remove translations from module list"""
    if not isinstance(module_list, list):
        raise AnthemError(
            "You have to provide a list of module's name to remove the translations"
        )
    ctx.env["ir.translation"].search([("module", "in", module_list)]).unlink()
