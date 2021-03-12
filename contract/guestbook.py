import smartpy as sp

class Guestbook(sp.Contract):
    def __init__(self):
        self.init(
            dates = sp.list([]),
            entries = sp.list([]),
            authors = sp.list([])
        )

    @sp.entry_point
    def add_entry(self, params):
        self.data.dates.push(sp.now)
        self.data.entries.push(params.e)
        self.data.authors.push(params.a)

# Tests
@sp.add_test(name = "Guestbook")
def test1():
    scenario = sp.test_scenario()
    scenario.h1("Welcome to Guestbook")
    c1 = Guestbook()
    scenario += c1
    scenario += c1.add_entry(a = 'alice', e = 'hello from alice')
    scenario += c1.add_entry(a = 'bob', e = 'hello from bob')
    scenario += c1.add_entry(a = 'charles', e = 'hello from charles')
