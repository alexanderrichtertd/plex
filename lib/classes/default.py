



class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(*args, **kwargs)
            return cls.__instance


class Singleton:
    class __Singleton:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not Singleton.instance:
            Singleton.instance = Singleton.__Singleton(arg)
        else:
            Singleton.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)


# http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Metaprogramming.html
# http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html


# def singleton(klass):
#     "Simple replacement of object creation operation"
#     def getinstance(*args, **kw):
#         if not hasattr(klass, 'instance'):
#             klass.instance = klass(*args, **kw)
#         return klass.instance
#     return getinstance

# def singleton(klass):
#     """
#     More powerful approach: Change the behavior
#     of the instances AND the class object.
#     """
#     class Decorated(klass):
#         def __init__(self, *args, **kwargs):
#             if hasattr(klass, '__init__'):
#                 klass.__init__(self, *args, **kwargs)
#         def __repr__(self) : return klass.__name__ + " obj"
#         __str__ = __repr__
#     Decorated.__name__ = klass.__name__
#     class ClassObject:
#         def __init__(cls):
#             cls.instance = None
#         def __repr__(cls):
#             return klass.__name__
#         __str__ = __repr__
#         def __call__(cls, *args, **kwargs):
#             print str(cls) + " __call__ "
#             if not cls.instance:
#                 cls.instance = Decorated(*args, **kwargs)
#             return cls.instance
#     return ClassObject()

# @singleton
# class ASingleton: pass

# a = ASingleton()
# b = ASingleton()
# print(a, b)
# print a.__class__.__name__
# print ASingleton
# assert a is b

# @singleton
# class BSingleton:
#     def __init__(self, x):
#         self.x = x

# c = BSingleton(11)
# d = BSingleton(22)
# assert c is d
# assert c is not a

""" Output:
ASingleton __call__
ASingleton __call__
(ASingleton obj, ASingleton obj)
ASingleton
ASingleton
BSingleton __call__
BSingleton __call__
"""

# DICTONARY
# with add
# doesnt break on wrong argument
