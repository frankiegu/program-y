import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.explode import TemplateExplodeNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.template.base import TemplateTestsBaseClass

class MockTemplateExplodeNode(TemplateExplodeNode):

    def __init__(self):
        TemplateExplodeNode.__init__(self)

    def resolve_to_string(self, bot, clientid):
        raise Exception ("This is an error")

class TemplateExplodeNodeTests(TemplateTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateExplodeNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("Hello World"))
        self.assertEqual(root.resolve(self.bot, self.clientid), "H e l l o W o r l d")

    def test_to_xml(self):
        root = TemplateNode()
        node = TemplateExplodeNode()
        root.append(node)
        node.append(TemplateWordNode("Test"))

        xml = root.xml_tree(self.bot, self.clientid)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><explode>Test</explode></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateExplodeNode()
        root.append(node)

        result = root.resolve(self.bot, self.clientid)
        self.assertIsNotNone(result)
        self.assertEquals("", result)