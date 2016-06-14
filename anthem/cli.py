# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Anthem: make your Odoo scripts sing!')
    parser.add_argument(
        'target', type=str,
        help='the target to run in the format module::function'
    )
    parser.parse_args()
