import good

class BetterSchema(good.Schema):
    def __and__(self, other):
        if not callable(other):
            other = type(self)(other)
        return type(self)(lambda x: self(x) and other(x))

    def __xor__(self, other):
        if not callable(other):
            other = type(self)(other)
        # validators are expected to return bool values, right?
        # TODO: think about it. There's also a Coerce thing
        return type(self)(lambda x: bool(self(x)) ^ bool(other(x)))

    def __or__(self, other):
        if not callable(other):
            other = type(self)(other)
        return type(self)(lambda x: self(x) or other(x))

