#!/usr/bin/env python3


class Node(list):

    ELEMENT_NODE = 1
    ATTRIBUTE_NODE = 2
    TEXT_NODE = 3
    CDATA_SECTION_NODE = 4
    ENTITY_REFERENCE_NODE = 5
    ENTITY_NODE = 6
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE = 8
    DOCUMENT_NODE = 9
    DOCUMENT_TYPE_NODE = 10
    DOCUMENT_FRAGMENT_NODE = 11
    NOTATION_NODE = 12

    def __init__(self, nodeType):
        super().__init__()
        self.nodeType = nodeType

    def toxml(self, encoding):
        return self.toprettyxml(indent='', newl='', encoding=encoding)

    def toprettyxml(self, indent='\t', newl='\n', encoding='', indentLevel=0):
        return ''


class TextNode(Node):
    def __init__(self, text):
        super().__init__(Node.TEXT_NODE)
        self.text = text

    def __str__(self):
        return self.text

    def toprettyxml(self, indent='\t', newl='\n', encoding='', indentLevel=0):
        return self.text


class Attr(Node):
    def __init__(self):
        super().__init__(Node.ATTRIBUTE_NODE)


class Element(Node):
    DEFAULTS = {}

    def __init__(
            self,
            tagName,
            namespaceURI=None,
            prefix=None,
            localName=None,
            **kwargs):
        super().__init__(Node.ELEMENT_NODE)
        self.tagName = tagName
        self._attributes = kwargs

        for key, value in self.DEFAULTS.items():
            if key not in self._attributes:
                self._attributes[key] = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attr_dict):
        self._attributes.update(attr_dict)
        for key, default in self.DEFAULTS:
            if key not in self._attributes:
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

    def openingTag(self):
        pieces = ['<', self.tagName]
        for key, value in self.attributes.items():
            pieces.append(' %s="%s"' % (key,value))
        if len(self) == 0:
            pieces.append('/>')
            return ''.join(pieces), False
        pieces.append(">")
        return ''.join(pieces), True


    def hasElementChild(self):
        for child in self:
            if child.nodeType == Node.ELEMENT_NODE:
                return True
        return False


    def toprettyxml(
        self,
        indent='\t',
        newl='\n',
        encoding='',
        indentLevel=0):

        pieces = [indent * indentLevel]

        openingTag, needsClosingTag = self.openingTag()
        if not needsClosingTag:
            return indent * indentLevel + openingTag

        pieces.append(openingTag)
        hasElementChild = self.hasElementChild()
        if hasElementChild:
            pieces.append(newl)
        for child in self:
            pieces.append(
                child.toprettyxml(
                    indent,
                    newl,
                    encoding,
                    indentLevel+1))
            if hasElementChild:
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

