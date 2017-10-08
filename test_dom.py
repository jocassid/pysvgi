#!/usr/bin/env python3

# test_dom.py

from unittest import TestCase

from dom import Element, Node, TextNode


class NodeTest(TestCase):

    def test_append(self):
        div1 = Element('div')
        div2 = Element('div')
        div1.append(div2)
        self.assertEqual(1, len(div1))

        childElement = div1[0]
        self.assertTrue(div2 is childElement)

        p = Element('p')
        p.append('some text')
        self.assertEqual(1, len(p))

        textNode = p[0]
        self.assertTrue(isinstance(textNode, TextNode))


class TextNodeTest(TestCase):
    def test_init(self):
        node = TextNode('foo')
        self.assertTrue(hasattr(node, 'nodeType'))
        self.assertEqual(Node.TEXT_NODE, node.nodeType)


class ElementTest(TestCase):

    def test_setAttribute(self):
        foo = Element('foo')

        # Using standard DOM methods
        foo.setAttribute('alpha', '1')
        self.assertEqual('1', foo.getAttribute('alpha'))

        # Using modified __setitem__ and __getitem__
        foo['bravo'] = '2'
        self.assertEqual('2', foo['bravo'])

    def test_setDefaults(self):
        class Div(Element):
            DEFAULTS = {'class': 'content'}

            def __init__(self, **kwargs):
                super().__init__('div', **kwargs)

        div = Div(id='disclaimer')

        self.assertEqual('content', div['class'])
        self.assertEqual('disclaimer', div['id'])

    def test_toprettyxml(self):
        svg = Element('svg')
        self.assertEqual('<svg/>', svg.toprettyxml())

        svg.setAttribute('width', '200')
        self.assertEqual('<svg width="200"/>', svg.toprettyxml())

        p = Element('p')
        p.append('some text')
        self.assertEqual('<p>some text</p>', p.toprettyxml())

        div = Element('div')

        p = Element('p')
        p.append('one')
        div.append(p)
        self.assertEqual(
            '<div>\n\t<p>one</p>\n</div>',
            div.toprettyxml())

        p = Element('p')
        p.append('two')
        div.append(p)

        self.assertEqual(
            '<div>\n\t<p>one</p>\n\t<p>two</p>\n</div>',
            div.toprettyxml())

    def test_getitem(self):
        className = 'description'
        attributes = {'class': className}
        div = Element('div', **attributes)

        p = Element('p')
        div.append(p)

        href = 'http://www.python.org'
        a = Element('a', href=href)
        div.append(a)

        self.assertIs(p, div[0])
        self.assertEqual(div['class'], 'description')
        self.assertIs(a, div[1])
        self.assertEqual(href, div[1]['href'])

    def test_hasElementChildren(self):
        div = Element('div')
        div.append('foo')
        self.assertEqual(False, div.hasElementChild())

        div = Element('div')
        div.append('text child')
        div.append(Element('hr'))
        self.assertEqual(True, div.hasElementChild())
