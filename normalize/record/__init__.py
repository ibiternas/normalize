from __future__ import absolute_import

from normalize.record.meta import RecordMeta


class Record(object):
    """Base class for normalize instances"""
    __metaclass__ = RecordMeta

    def __init__(self, **kwargs):
        for prop, val in kwargs.iteritems():
            meta_prop = type(self).__dict__.get(prop, None)
            if meta_prop is None:
                raise Exception(
                    "unknown property '%s' in %s" % (prop, type(self).__name__)
                )
            meta_prop.init_prop(self, val)
        missing = type(self).required - set(kwargs.keys())

        for propname in missing:
            meta_prop = type(self).__dict__[propname]
            meta_prop.init_prop(self)

    def __iter__(self):
        for name in type(self).properties.keys():
            yield (name, getattr(self, name))
