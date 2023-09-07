from operator import methodcaller
from collections import OrderedDict


viewkeys = methodcaller("keys")
viewvalues = methodcaller("values")
viewitems = methodcaller("items")


def iterkeys(d: OrderedDict, **kw):
    return iter(d.keys(**kw))


def itervalues(d: OrderedDict, **kw):
    return iter(d.values(**kw))


def iteritems(d: OrderedDict, **kw):
    return iter(d.items(**kw))


def iterlists(d: OrderedDict, **kw):
    return iter(d.lists(**kw))