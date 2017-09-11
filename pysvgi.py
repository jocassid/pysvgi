
class Node(list):
    pass
        
     
class TextNode(Node):
    def __init__(self, text):
        self.text = text
        
    def __str__(self):
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
        self.attributes = {}
        self.setAttributes(**kwargs)
        
    def setAttributes(self, **kwargs):
        self.attributes.update(kwargs)
        for key, default in self.DEFAULTS:
            if key in kwargs:
                continue
            self.attributes[key] = default
            
    def __str__(self):
        pieces = ['<', self.tagName]
        for key, value in self.attributes.items():
            pieces.append(' %s="%s"' % (key,value))
        if len(self) == 0:
            pieces.append('/>')
            return ''.join(pieces)
        pieces.append(">")
        for child in self:
            pieces.append(str(child))
        pieces.append("</%s>" % self.tagName)
        return ''.join(pieces)


class BaseSvgElement(Element):
    
    # dict to 
    KWARG_TRANSLATION = {
        'font_size':'font-size',
        'text_anchor':'text-anchor'
    }
    def __init__(
            self, 
            tagName, 
            namespaceURI=None, 
            prefix=None, 
            localName=None,
            **kwargs): 
        for key in self.KWARG_TRANSLATION:
            if key not in kwargs:
                continue
            value = kwargs.pop(key)
            new_key = self.KWARG_TRANSLATION[key]
            if new_key in kwargs:
                raise KeyError("%s already in kwargs")
            kwargs[new_key] = value
        super().__init__(tagName, namespaceURI, prefix, localName, **kwargs)
        

class Rect(BaseSvgElement):
    DEFAULTS = (
        ('fill', 'black'),
    )
    
    def __init__(self, width=0, height=0, **kwargs):
        super().__init__('rect', **kwargs)
        self.attributes['width'] = width
        self.attributes['height'] = height
        
    @property
    def width(self):
        try:
            return self.attributes['width']
        except KeyError:
            self.attributes['width'] = 0
            return 0
            
    @width.setter
    def width(self, value):
        self.attributes['width'] = value
        
        
class Circle(BaseSvgElement):
    DEFAULTS = (
        ('fill', 'black'),
    )
        
    def __init__(self, r, cx, cy, **kwargs):
        super().__init__('circle', **kwargs)
        self.attributes['r'] = r
        self.attributes['cx'] = cx
        self.attributes['cy'] = cy

        
class Text(BaseSvgElement):
    DEFAULTS = (
        ('fill', 'black'),
    )    
    
    def __init__(self, text, **kwargs):
        super().__init__('text', **kwargs)
        textNode = TextNode(text)
        self.append(textNode)

class Ellipse(BaseSvgElement):
    DEFAULTS = (
        ('fill', 'black'),
    )  
    
    def __init__(self, rx, ry, **kwargs):
        super().__init__('ellipse', **kwargs)
        self.attributes['rx'] = rx
        self.attributes['ry'] = ry
#<ellipse cx="75" cy="75" rx="20" ry="5" stroke="red" fill="transparent" stroke-width="5"/>

class Svg(BaseSvgElement):
    def __init__(self, width=0, height=0, **kwargs):
        super().__init__('svg', **kwargs)
        self.attributes['version'] = "1.1"
        self.attributes['baseProfile'] = "full"
        self.attributes['xmlns'] = "http://www.w3.org/2000/svg"
        self.attributes['width'] = width
        self.attributes['height'] = height
            
    def document(self):
        pieces = ["<?xml version='1.0' encoding='utf-8'?>"]
        pieces.append(str(self))
        return "\n".join(pieces)
        
    
                                             
                                             
