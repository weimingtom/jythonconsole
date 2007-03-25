import unittest
from  history import History

try:
    True, False
except NameError:
    (True, False) = (1, 0)

class MockConsole:
    def replaceRow(self, text):
        self.text = text

    def inLastLine(self):
        return True

class HistoryTestCase(unittest.TestCase):

    def setUp(self):
        self.console = MockConsole()

    def tearDown(self):
        self.console = None

    def testHistoryUp(self):
        h = History(self.console)
        h.append("one")
        h.append("two")
        h.append("three")

        h.historyUp()
        self.assertEquals("three", self.console.text)

        h.historyUp()
        self.assertEquals("two", self.console.text)

        h.historyUp()
        self.assertEquals("one", self.console.text)

        # history doesn't roll, just stops at the last item
        h.historyUp()
        self.assertEquals("one", self.console.text)

    def testHistoryDown(self):
        h = History(self.console)
        h.append("one")
        h.append("two")
        h.append("three")

        h.historyUp()
        h.historyUp()
        
        h.historyUp()
        self.assertEquals("one", self.console.text)

        h.historyDown()
        self.assertEquals("two", self.console.text)

        h.historyDown()
        self.assertEquals("three", self.console.text)

        h.historyDown()
        self.assertEquals("", self.console.text)

        # History doesn't wrap
        h.historyDown()
        self.assertEquals("", self.console.text)

    def testSkipDuplicates(self):
       h = History(self.console)
       h.append("one")
       h.append("one")
       h.append("two")
       h.append("two")
       h.append("three")
       h.append("three")

       h.historyUp()
       self.assertEquals("three", self.console.text)

       h.historyUp()
       self.assertEquals("two", self.console.text)

       h.historyUp()
       self.assertEquals("one", self.console.text)

    def testSkipEmpty(self):
        h = History(self.console)
        h.append("")
        self.assert_(len(h.history) == 0)

        h.append("\n")
        self.assert_(len(h.history) == 0)

        h.append(None)
        self.assert_(len(h.history) == 0)

if __name__ == '__main__':
    unittest.main()
