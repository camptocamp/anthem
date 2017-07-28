# -*- coding: utf-8 -*-
# Copyright 2016-2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from . import modules


def uninstall(ctx, module_list):
    """ uninstall module """
    modules.uninstall(ctx, module_list)
    ctx.log_line(u'Deprecated: use anthem.lyrics.modules.uninstall instead of '
                 'anthem.lyrics.uninstaller.uninstall')
