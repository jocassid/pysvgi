#!/usr/bin/env python3

from pysvgi import Svg, Rect, Circle, Text

def basic_svg_sample():
    
    svg = Svg(300, 200)
    
    rect = Rect('100%', '100%', fill="red")
    
    circle = Circle(80, 150, 100, fill="green")
    
    text = Text('SVG', x="150", y="125", font_size="60", text_anchor="middle", 
        fill="white")
    
    svg.append(rect)
    svg.append(circle)
    svg.append(text)
    
    print(svg.document())
    

def try_viewBox():
    #svg = Svg(200, 200, viewBox="0 0 100 100")
    svg = Svg(200, 200, viewBox="0 0 100 100")
    
     
    svg.append(Circle(50, 50, 50, fill='red'))
    svg.append(Circle(50, 50, 150, fill='blue'))
    svg.append(Circle(50, 150, 50, fill='green'))
    svg.append(Circle(50, 150, 150, fill='yellow'))
    
    print('''<?xml version='1.0' encoding='utf-8'?>
        <html>
        <style>
        body{ background: black }
        svg{ border: solid white 1px }
        </style>
        <body>''')
    print(svg)
    print('''</body>
        </html>''')

def main():
    try_viewBox()

if __name__ == '__main__':
    main()
