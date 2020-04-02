"""STIX 2.1 Bundle Representation."""

from collections import OrderedDict

from ..base import _STIXBase
from ..properties import (
    IDProperty, ListProperty, STIXObjectProperty, TypeProperty,
)


class Bundle(_STIXBase):
    """For more detailed information on this object's properties, see
    `the STIX 2.1 specification <https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_nuwp4rox8c7r>`__.
    """

    _type = 'bundle'
    _properties = OrderedDict([
        ('type', TypeProperty(_type)),
        ('id', IDProperty(_type, spec_version='2.1')),
        ('objects', ListProperty(STIXObjectProperty(spec_version='2.1'))),
    ])

    def __init__(self, *args, **kwargs):
        # Add any positional arguments to the 'objects' kwarg.
        if args:
            if isinstance(args[0], list):
                kwargs['objects'] = args[0] + list(args[1:]) + kwargs.get('objects', [])
            else:
                kwargs['objects'] = list(args) + kwargs.get('objects', [])

        allow_custom = kwargs.get('allow_custom', False)
        self._allow_custom = allow_custom
        self._properties['objects'].contained.allow_custom = allow_custom
        interoperability = kwargs.get('interoperability', False)
        self.__interoperability = interoperability
        self._properties['id'].interoperability = interoperability
        self._properties['objects'].contained.interoperability = interoperability

        super(Bundle, self).__init__(**kwargs)

    def get_obj(self, obj_uuid):
        if "objects" in self._inner:
            found_objs = [elem for elem in self.objects if elem['id'] == obj_uuid]
            if found_objs == []:
                raise KeyError("'%s' does not match the id property of any of the bundle's objects" % obj_uuid)
            return found_objs
        else:
            raise KeyError("There are no objects in this empty bundle")

    def __getitem__(self, key):
        try:
            return super(Bundle, self).__getitem__(key)
        except KeyError:
            try:
                return self.get_obj(key)
            except KeyError:
                raise KeyError("'%s' is neither a property on the bundle nor does it match the id property of any of the bundle's objects" % key)
