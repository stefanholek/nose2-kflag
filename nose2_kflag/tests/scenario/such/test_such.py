from nose2.tools import such

with such.A('foo test') as it1:

    @it1.should('work')
    def test(case):
        pass

    @it1.should('work also')
    def test(case):
        pass

with such.A('bar test') as it2:

    @it2.should('work')
    def test(case):
        pass

it1.createTests(globals())
it2.createTests(globals())
