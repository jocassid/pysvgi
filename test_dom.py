#!/usr/bin/env python3

# test_dom.py

from unittest import TestCase

from dom import Element, TextNode


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
        
        
        
class ElementTest(TestCase):
    
    def test_setAttribute(self):
        foo = Element('foo')
        
        # Using standard DOM methods
        foo.setAttribute('alpha', '1')
        self.assertEqual('1', foo.getAttribute('alpha'))
        
        # Using modified __setitem__ and __getitem__
        foo['bravo'] = '2'
        self.assertEqual('2', foo['bravo'])
        
        
    def test_toprettyxml(self):     
        svg = Element('svg')
        self.assertEqual('<svg/>', svg.toprettyxml())
        
        svg.setAttribute('width', '200')
        self.assertEqual('<svg width="200"/>', svg.toprettyxml())
        
        
    def test_getitem(self):
        self.fail("Not implemented")
        
        
    
        
        
        
