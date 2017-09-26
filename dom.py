#!/usr/bin/env python3


class Node(list):
    
    def toxml(self, encoding):
        return self.toprettyxml(indent='', newl='', encoding=encoding)
    
    def toprettyxml(self, indent='\t', newl='\n', encoding=''):
        return ''
        
     
class TextNode(Node):
    def __init__(self, text):
        self.text = text
        
    def __str__(self):
        return self.text
        
    def toprettyxml(self, indent='\t', newl='\n', encoding=''):
        return self.text

class Attr(Node):
    pass

class Element(Node):
    DEFAULTS = ()
    
    def __init__(
            self, 
            tagName, 
            namespaceURI=None, 
            prefix=None, 
            localName=None,
            **kwargs):  
        super().__init__()
        self.tagName = tagName
        self._attributes = kwargs

        
    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attr_dict):
        self._attributes.update(attr_dict)
        for key, default in self.DEFAULTS:
            if key in attr_dict:
                continue
            self._attributes[key] = default
            
    def setAttribute(self, name, value):
        self._attributes[name] = value
        
    def getAttribute(self, name):
        return self._attributes[name]
        
    def __setitem__(self, key, value):
        key_type = type(key)
        if key_type == int:
            super().__setitem__(key, value)
            return
        if key_type == str:
            self._attributes[key] = value
            return
        raise TypeError("Unsupported index type %s" % key_type)
        
        
    def __getitem__(self, key):
        key_type = type(key)
        if key_type == int:
            return super().__getitem__(key)
        if key_type == str:
            return self._attributes[key]
        raise TypeError("Unsupported index type %s" % key_type)
        
               
    def toprettyxml(
        self, 
        indent='\t', newl='\n', encoding='', indentLevel=0):
        
        pieces = ['<', self.tagName]
        for key, value in self.attributes.items():
            pieces.append(' %s="%s"' % (key,value))
        if len(self) == 0:
            pieces.append('/>')
            return ''.join(pieces)
        pieces.append(">")
        pieces.append(newl)
        for child in self:
            pieces.append(indent)
            pieces.append(child.toprettyxml())
            pieces.append(newl)
        pieces.append("</%s>" % self.tagName)
        return ''.join(pieces)
        
    def append(self, item):
        if isinstance(item, str):
            item = TextNode(item)
        super().append(item)
            
        
class Document:
    # I forget what the technical term is for this
    XML_LINE = "<?xml version='1.0' encoding='utf-8'?>"

