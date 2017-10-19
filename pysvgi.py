#!/usr/bin/env python3

from dom import Element


class BaseSvgElement(Element):

    # dict to
    KWARG_TRANSLATION = {
        'font_size': 'font-size',
        'text_anchor': 'text-anchor',
        'stroke_width': 'stroke-width'
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


class RectangularElement(BaseSvgElement):

    def __init__(self, tagName, **kwargs):
        super().__init__(tagName, **kwargs)

    @property
    def width(self):
        try:
            return self['width']
        except KeyError:
            self['width'] = 0
            return 0

    @width.setter
    def width(self, value):
        self['width'] = value

    @property
    def height(self):
        try:
            return self['height']
        except KeyError:
            self['height'] = 0
            return 0

    @height.setter
    def height(self, value):
        self['height'] = value


class Line(BaseSvgElement):
    DEFAULTS = {
        'stroke-width': '1',
        'stroke': 'black'
    }

    def __init__(self, x1=0, y1=0, x2=0, y2=0, **kwargs):
        super().__init__('line', **kwargs)
        self['x1'] = x1
        self['y1'] = y1
        self['x2'] = x2
        self['y2'] = y2
        
    @property
    def x1(self):
        try:
            return self['x1']
        except KeyError:
            self['x1'] = 0
            return 0
            
    @x1.setter
    def x1(self, value):
        self['x1'] = value


class Rect(RectangularElement):
    DEFAULTS = {
        'fill': 'black',
    }

    def __init__(self, width=0, height=0, **kwargs):
        super().__init__('rect', **kwargs)
        self['width'] = width
        self['height'] = height


class Circle(BaseSvgElement):
    DEFAULTS = {
        'fill': 'black',
    }

    def __init__(self, r, cx, cy, **kwargs):
        super().__init__('circle', **kwargs)
        self['r'] = r
        self['cx'] = cx
        self['cy'] = cy


class Text(BaseSvgElement):
    DEFAULTS = {
        'fill': 'black',
    }

    def __init__(self, text, x, y, **kwargs):
        super().__init__('text', **kwargs)
        self.append(text)
        self['x'] = x
        self['y'] = y


class Ellipse(BaseSvgElement):
    DEFAULTS = {
        'fill': 'black',
    }

    def __init__(self, rx, ry, **kwargs):
        super().__init__('ellipse', **kwargs)
        self['rx'] = rx
        self['ry'] = ry
#<ellipse cx="75" cy="75" rx="20" ry="5" stroke="red" fill="transparent" stroke-width="5"/>


class Svg(RectangularElement):
    def __init__(self, width=0, height=0, **kwargs):
        super().__init__(
            'svg',
            version="1.1",
            baseProfile="full",
            xmlns="http://www.w3.org/2000/svg",
            width=width,
            height=height)
