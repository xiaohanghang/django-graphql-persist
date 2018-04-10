import re

__all__ = ['query_key_handler']


versioning_regex = re.compile(r'\.(?!\d)', re.IGNORECASE)


def query_key_handler(query_id, request):
    if request.version is None:
        return query_id

    versioning_prefix = versioning_regex.split(request.version)
    return versioning_prefix + [query_id]


class QueryKey:

    def __init__(self, keys):
        self._keys = keys

    def __iter__(self):
        return iter(self._keys)

    def __len__(self):
        return len(self._keys)

    def __getitem__(self, index):
        value = self._keys[index]
        if isinstance(index, slice):
            return QueryKey(value)
        return value

    def __add__(self, keys):
        return QueryKey(self._keys + keys)

    def __repr__(self):
        return list.__repr__(self._keys)

    def __str__(self):
        return '.'.join(self._keys)

    def qslice(self, end):
        return self[:end - 1] + self[-1:]._keys
