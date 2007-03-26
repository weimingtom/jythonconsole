import unittest
import jintrospect
from java.lang import String

class JIntrospectTestCase(unittest.TestCase):

    def testGetAutoCompleteList(self):
        s = String("Unit Test")
        list = jintrospect.getAutoCompleteList("s", locals())
        self.assertNotEmpty(list)
        self.assertContains(list, "contains")

    def testGetCallTipJava(self):
        s = String("Unit Test")
        tip = jintrospect.getCallTipJava("s.contains", locals())
        self.assertEquals("contains(java.lang.CharSequence) -> boolean", tip[2])

    def testGetPackageName(self):
        package_name = jintrospect.getPackageName("import java.")
        self.assertEquals("java", package_name)

        package_name = jintrospect.getPackageName("from java.awt import")
        self.assertEquals("java.awt", package_name)

    def testCompletePackageName(self):
        try:
            list = jintrospect.completePackageName("bogus")
            fail("Expecting import error.")
        except ImportError:
            pass

        list = jintrospect.completePackageName("java")
        self.assertNotEmpty(list)
        self.assertContains(list, "awt")

        list = jintrospect.completePackageName("java.util")
        self.assertNotEmpty(list)
        self.assertContains(list, "ArrayList")

    def testIsPython(self):
        s = String("Java String")
        self.assert_(not jintrospect.ispython(s))

        self.assert_(jintrospect.ispython(jintrospect))

    def testIsPython22(self):
        # NOTE: This will fail with AP 2.1.  Would it fail for old version too?             
        ps = "python string"
        self.assert_(jintrospect.ispython(ps))

        d = {}
        self.assert_(jintrospect.ispython(d))


    # note: static methods and fields are tested in static_test_case

    def assertNotEmpty(self, list):
        if list == None:
            self.fail("list is None")
        if len(list) < 1:
            self.fail("list is empty")

    def assertContains(self, list, value):
        try:
            list.index(value)
        except ValueError:
            self.fail("list does not contain %s" % value)

if __name__ == '__main__':
    unittest.main()
