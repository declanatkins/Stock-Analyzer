# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.12
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_ModelOperations')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_ModelOperations')
    _ModelOperations = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_ModelOperations', [dirname(__file__)])
        except ImportError:
            import _ModelOperations
            return _ModelOperations
        try:
            _mod = imp.load_module('_ModelOperations', fp, pathname, description)
        finally:
            if fp is not None:
                fp.close()
        return _mod
    _ModelOperations = swig_import_helper()
    del swig_import_helper
else:
    import _ModelOperations
del _swig_python_version_info

try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

class doubleArray(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, doubleArray, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, doubleArray, name)
    __repr__ = _swig_repr

    def __init__(self, nelements):
        this = _ModelOperations.new_doubleArray(nelements)
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
    __swig_destroy__ = _ModelOperations.delete_doubleArray
    __del__ = lambda self: None

    def __getitem__(self, index):
        return _ModelOperations.doubleArray___getitem__(self, index)

    def __setitem__(self, index, value):
        return _ModelOperations.doubleArray___setitem__(self, index, value)

    def cast(self):
        return _ModelOperations.doubleArray_cast(self)
    if _newclass:
        frompointer = staticmethod(_ModelOperations.doubleArray_frompointer)
    else:
        frompointer = _ModelOperations.doubleArray_frompointer
doubleArray_swigregister = _ModelOperations.doubleArray_swigregister
doubleArray_swigregister(doubleArray)

def doubleArray_frompointer(t):
    return _ModelOperations.doubleArray_frompointer(t)
doubleArray_frompointer = _ModelOperations.doubleArray_frompointer


def add_values(values_list, n_values, company, set):
    return _ModelOperations.add_values(values_list, n_values, company, set)
add_values = _ModelOperations.add_values

def get_predicted_values(company, set):
    return _ModelOperations.get_predicted_values(company, set)
get_predicted_values = _ModelOperations.get_predicted_values

def make_single_prediction_EXTERNAL(company, set):
    return _ModelOperations.make_single_prediction_EXTERNAL(company, set)
make_single_prediction_EXTERNAL = _ModelOperations.make_single_prediction_EXTERNAL

def append_to_values(values_list, n_values, company, set):
    return _ModelOperations.append_to_values(values_list, n_values, company, set)
append_to_values = _ModelOperations.append_to_values

def update_probabilities(company, set, last_val):
    return _ModelOperations.update_probabilities(company, set, last_val)
update_probabilities = _ModelOperations.update_probabilities

def make_single_prediction_INTERNAL(last_change, last_val, company, set):
    return _ModelOperations.make_single_prediction_INTERNAL(last_change, last_val, company, set)
make_single_prediction_INTERNAL = _ModelOperations.make_single_prediction_INTERNAL

def get_expected_value(filename, prev_val):
    return _ModelOperations.get_expected_value(filename, prev_val)
get_expected_value = _ModelOperations.get_expected_value

def update_weighting_values(values_list, n_values, company, set):
    return _ModelOperations.update_weighting_values(values_list, n_values, company, set)
update_weighting_values = _ModelOperations.update_weighting_values

def read_last_line(filename):
    return _ModelOperations.read_last_line(filename)
read_last_line = _ModelOperations.read_last_line
# This file is compatible with both classic and new-style classes.


