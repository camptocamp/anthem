# Copyright 2016 Camptocamp SA
# Copyright 2026 XCG SAS
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
from importlib.metadata import PackageNotFoundError, distribution

try:
    __version__ = distribution("anthem").version
except PackageNotFoundError:
    __version__ = "dev"

# publish the decorator so we can use 'anthem.log'
from .output import log  # noqa
