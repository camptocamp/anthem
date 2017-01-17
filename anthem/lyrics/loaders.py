# -*- coding: utf-8 -*-
# Copyright 2016-2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import codecs
import csv

from ..exceptions import AnthemError


def load_csv(ctx, model, path, dialect='excel', **fmtparams):
    """ Load a CSV from a filename

    Usage example::

      from pkg_resources import Requirement, resource_string

      req = Requirement.parse('my-project')
      load_csv(ctx, ctx.env['res.users'],
               resource_string(req, 'data/users.csv'),
               delimiter=',')

    """
    with open(path, 'rb') as data:
        load_csv_stream(ctx, model, data, dialect=dialect, **fmtparams)


def csv_unireader(f, encoding="utf-8", **fmtparams):
    data = csv.reader(
        codecs.iterencode(codecs.iterdecode(f, encoding), "utf-8"), **fmtparams
    )
    for row in data:
        yield [e.decode("utf-8") for e in row]


def load_csv_stream(ctx, model, data, dialect='excel', encoding='utf-8',
                    **fmtparams):
    """ Load a CSV from a stream

    Usage example::

      from pkg_resources import Requirement, resource_stream

      req = Requirement.parse('my-project')
      load_csv_stream(ctx, ctx.env['res.users'],
                      resource_stream(req, 'data/users.csv'),
                      delimiter=',')

    """
    data = csv_unireader(data, encoding=encoding, **fmtparams)
    head = data.next()
    values = list(data)
    if values:
        if isinstance(model, basestring):
            model = ctx.env[model]
        result = model.load(head, values)
        ids = result['ids']
        if not ids:
            messages = u'\n'.join(
                u'- %s' % msg for msg in result['messages']
            )
            ctx.log_line(u"Failed to load CSV "
                         u"in '%s'. Details:\n%s" %
                         (model._name, messages))
            raise AnthemError(u'Could not import CSV. See the logs')
        else:
            ctx.log_line(u"Imported %d records in '%s'" %
                         (len(ids), model._name))
