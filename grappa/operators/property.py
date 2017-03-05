from ..operator import Operator


class PropertyOperator(Operator):
    """
    Asserts if a given object has property or properties.

    Example::

        class Foo(object):
            bar = 'foo'

            def baz():
                pass

        # Should style
        Foo() | should.have.property('bar')
        Foo() | should.have.properties('bar', 'baz')
        Foo() | should.have.properties.present.equal.to('bar', 'baz')

        # Should style - negation form
        Foo() | expect.to_not.have.property('bar')
        Foo() | expect.to_not.have.properties('bar', 'baz')
        Foo() | expect.to_not.have.properties.present.equal.to('bar', 'baz')

        # Expect style
        Foo() | expect.to.have.property('bar')
        Foo() | expect.to.have.properties('bar', 'baz')
        Foo() | expect.to.have.properties.present.equal.to('bar', 'baz')

        # Expect style - negation form
        Foo() | expect.to_not.have.property('bar')
        Foo() | expect.to_not.have.properties('bar', 'baz')
        Foo() | expect.to_not.have.properties.present.equal.to('bar', 'baz')
    """

    # Is the operator a keyword
    kind = Operator.Type.MATCHER

    # Operator keywords
    operators = ('properties', 'property')

    # Operaror chain aliases
    aliases = ('present', 'equal', 'to')

    # Error message templates
    expected_message = Operator.Dsl.Message(
        'a property with name "{value}"',
        'a number that is within the given range',
    )

    subject_message = Operator.Dsl.Message(
        'an unexpected range number {value}',
    )

    def after_success(self, obj, *keys):
        if self.ctx.negate:
            return

        # Get attribute keys
        self.ctx.value = [getattr(obj, x) for x in keys]

        if len(keys) == 1:
            self.ctx.value = self.ctx.value[0]

    def match(self, subject, *args, **kwargs):
        success_reasons = []
        for name in args:
            has_property, reason = self._has_property(subject, name)
            if not has_property:
                return False, [reason]
            else:
                success_reasons.append(reason)

        for name, value in kwargs.items():
            has_property, reason = self._has_property(subject, name, value)
            if not has_property:
                return False, [reason]
            else:
                success_reasons.append(reason)

        return True, success_reasons

    def _has_property(self, subject, name, *args):
        if args:
            try:
                value = getattr(subject, name)
            except AttributeError:
                return False, 'property {0!r} not found'.format(name)
            else:
                expected_value = args[0]
                result, _ = expected_value._match(value)
                if not result:
                    return False, 'property {0!r} {1!r} not found'.format(
                        name, expected_value)
                return True, 'property {0!r} {1!r} found'.format(
                    name, expected_value)

        if not hasattr(subject, name):
            return False, 'property {0!r} not found'.format(name)
        return True, 'property {0!r} found'.format(name)
