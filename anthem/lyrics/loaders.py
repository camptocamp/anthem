# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import csv

from ..exceptions import AnthemError


def load_csv(ctx, model_name, path, dialect='excel', **fmtparams):
    """ Load a CSV from a filename

    Usage example::

      from pkg_resources import Requirement, resource_string

      req = Requirement.parse('my-project')
      load_csv(ctx, 'res.users',
               resource_string(req, 'data/users.csv'),
               delimiter=',')

    """
    with open(path, 'rb') as data:
        load_csv_stream(ctx, model_name, data, dialect=dialect, **fmtparams)


def load_csv_stream(ctx, model_name, data, dialect='excel', **fmtparams):
    """ Load a CSV from a stream

    Usage example::

      from pkg_resources import Requirement, resource_stream

      req = Requirement.parse('my-project')
      load_csv_stream(ctx, 'res.users',
                      resource_stream(req, 'data/users.csv'),
                      delimiter=',')

    """
    data = csv.reader(data, dialect=dialect, **fmtparams)
    head = data.next()
    values = list(data)
    if values:
        result = ctx.env[model_name].load(head, values)
        ids = result['ids']
        if not ids:
            messages = u'\n'.join(
                u'- %s' % msg for msg in result['messages']
            )
            ctx.log_line(u"Failed to load CSV "
                         u"in '%s'. Details:\n%s" %
                         (model_name, messages))
            raise AnthemError(u'Could not import CSV. See the logs')
        else:
            ctx.log_line(u"Imported %d records in '%s'" %
                         (len(ids), model_name))
