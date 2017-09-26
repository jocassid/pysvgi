
from unittest import TestCase

from pysvgi import Svg
        
        
class SvgTest(TestCase):
    
    def test_init(self):
        svg = Svg()
        self.assertEqual("1.1", svg['version'])
        self.assertEqual("full", svg['baseProfile'])
        self.assertEqual("http://www.w3.org/2000/svg", svg['xmlns'])
            
    
    def test_width(self):
        svg = Svg()
        svg.width = 200
        self.assertEqual(200, svg.attributes['width'])
        self.assertEqual(200, svg.width)
        
    def test_height(self):
        svg = Svg()
        svg.height = 300
        self.assertEqual(300, svg.attributes['height'])
        self.assertEqual(300, svg.height)


