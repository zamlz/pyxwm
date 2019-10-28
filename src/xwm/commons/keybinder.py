
class KeyFunc(object):

    def __init__(self, op, args=[], kwargs={}):
        self._op = op
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        return self._op(*self._args, **self._kwargs)


class KeyBinder(dict):

    def __init__(self, modifier='Alt'):
        self.mod = modifier

    def __setitem__(self, key, item):
        assert type(item) is KeyFunc, "Must be type {}".format(KeyFunc)
        super(KeyBinder, self).__setitem__(key, item)

    def bind(self, key, args=[], kwargs={}):
        def func_binder(method):
            self[key] = KeyFunc(method, args, kwargs)
            return method
        return func_binder
