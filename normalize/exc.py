"""
Structured exception module.

This makes structured exceptions as easy to use as string exceptions.  Simply
define an exception name and a format string; the base class takes care of the
rest.  Should you need any more sophisticated handling of an exception, it is
easy to change without affecting downstream users.
"""


class StringFormatException(Exception):
    message = "(uncustomized exception!)"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        try:
            self.formatted = self.message.format(*args, **kwargs)
        except IndexError:
            raise PositionalExceptionFormatError(
                typename=type(self).__name__,
                received=repr(args),
            )
        except KeyError, e:
            raise KeywordExceptionFormatError(
                typename=type(self).__name__,
                missing=e[0],
                passed=repr(kwargs.keys()),
            )

    def __str__(self):
        return self.formatted

    def __getattr__(self, attrname):
        try:
            return self.kwargs[attrname]
        except KeyError:
            raise AttributeError(
                "no such attribute %s of %s" % (
                    attrname, type(self).__name__,
                )
            )

    def __getitem__(self, key):
        return self.args[key]

    def __repr__(self):
        return "%s%s(%s)" % (
            "exc." if self.__module__.endswith(".exc") else "",
            type(self).__name__, ", ".join(
                tuple("%r" % x for x in self.args) +
                tuple("%s=%r" % (k, v) for k, v in self.kwargs.iteritems())
            )
        )


# exception base classes
class FieldSelectorException(StringFormatException):
    pass


class PropertyDefinitionError(StringFormatException):
    pass


class PropertyTypeDefinitionError(StringFormatException):
    pass


class StringFormatExceptionError(StringFormatException):
    pass


class SubclassError(StringFormatException):
    pass


class UsageException(StringFormatException):
    pass


# concrete exception types
class CoerceWithoutType(PropertyDefinitionError):
    message = (
        "In order to coerce types, the intended type must be known; "
        "pass isa=TYPE or isa=(TYPE, TYPE, ...) to Property()"
    )


class DefaultSignatureError(PropertyDefinitionError):
    message = (
        "default functions may take 0 or 1 arguments; {module}.{func} "
        "wants {nargs}"
    )


class DiffOptionsException(UsageException):
    message = "pass options= or DiffOptions constructor arguments; not both"


class FieldSelectorAttributeError(FieldSelectorException, AttributeError):
    message = "Could not find property specified by name: {name}"


class FieldSelectorKeyError(FieldSelectorException, KeyError):
    message = "Could not find Record specified by index: {key}"


class KeywordExceptionFormatError(StringFormatExceptionError):
    message = (
        "{typename} raised without passing {missing}; saw only: {passed}"
    )


class LazyIsFalse(PropertyDefinitionError):
    message = "To make an eager property, do not pass lazy= to Property()"


class PositionalArgumentsProhibited(PropertyDefinitionError):
    message = (
        "Positional arguments to Property constructors will only end "
        "in tears.  Convert to keyword argument form."
    )


class PositionalExceptionFormatError(StringFormatExceptionError):
    message = (
        "{typename} expects a positional format string; passed: "
        "{received}"
    )


class PropertyTypeClash(StringFormatException):
    message = (
        "Both {oldtype} and {newtype} purport to provide the mix of "
        "traits: {traitlist} (perhaps a module import error is causing "
        "module initialization to happen multiple times?)"
    )


class PropertyTypeMismatch(PropertyDefinitionError):
    message = "Can't create {selected} property using {base} constructor"


class PropertyTypeMixNotFound(StringFormatException):
    message = (
        "Failed to find a Property type which provides traits {traitlist}; "
        "try subclassing SafeProperty instead of Property in your custom "
        "Property type."
    )


class ReadOnlyAttributeError(StringFormatException, AttributeError):
    message = "{attrname} is read-only"