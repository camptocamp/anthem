# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html)
import argparse
import importlib


def main():
    parser = argparse.ArgumentParser(
        description='Anthem: make your Odoo scripts sing!')
    parser.add_argument(
        'target', type=str,
        help='the target to run in the format module::function'
    )
    args = parser.parse_args()
    run(args.target)


def run(target):
    mod_name, func_name = target.split('::')
    module = importlib.import_module(mod_name)
    func = getattr(module, func_name)
    func()
