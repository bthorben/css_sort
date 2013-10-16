import unittest
import css_sort


class CSSSortTest(unittest.TestCase):

    def testBasics(self):
        t = self.decodesto
        t("", "")
        t("{a:0;b:0;}", "{a:0;b:0;}")
        t("{b:0;a:0;}", "{a:0;b:0;}")
        t("{a:0;b:0;}", "{a:0;b:0;}")
        t("{b:0;a:0;}", "{a:0;b:0;}")
        t("{b:0;a:0;}{b:0;a:0;}", "{a:0;b:0;}{a:0;b:0;}")

    def testComments(self):
        t = self.decodesto
        t("{/*test*/b:0;\na:0;\n}", "{\na:0;\n/*test*/b:0;}")

    def testString(self):
        t = self.decodesto
        t('{b: url("test");}{b:0;a:0;}', '{b: url("test");}{a:0;b:0;}')
        t('{b: url(\'test\');}{b:0;a:0;}', '{b: url(\'test\');}{a:0;b:0;}')

    def testWhitespace(self):
        t = self.decodesto
        t("{b:0; a:0\n0;}", "{ a:0\n0;b:0;}")
        t("{b:0; a:0;}\n{b:0; a:0;}", "{ a:0;b:0;}\n{ a:0;b:0;}")
        t("{\nb:0;\na:0;\n}\n\n{b:0; a:0;}", "{\na:0;\n\nb:0;}\n\n{ a:0;b:0;}")

    def testMediaQuery(self):
        t = self.decodesto
        t("@media print{{b:0;a:0;}}\n{b:0;a:0;}",
          "@media print{{a:0;b:0;}}\n{a:0;b:0;}")
        t("@media print{{b:0;a:0\n0;}}\n{b:0;a:0\n0;}",
          "@media print{{a:0\n0;b:0;}}\n{a:0\n0;b:0;}")

    def testPrefix(self):
        t = self.decodesto
        t("{b:0;-o-a:0;}", "{-o-a:0;b:0;}")
        t("{b:0;-moz-a:0;}", "{-moz-a:0;b:0;}")
        t("{b:0;-webkit-a:0;}", "{-webkit-a:0;b:0;}")
        t("{b:0;-ms-a:0;}", "{-ms-a:0;b:0;}")

    def decodesto(self, input, expectation=None):
        self.assertEqual(css_sort.sort(input), expectation or input)

if __name__ == '__main__':
    unittest.main()
