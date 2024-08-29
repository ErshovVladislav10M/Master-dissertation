import io
import svglib
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.renderSVG import SVGCanvas, draw

with open("sample1.svg") as fp:
    svg_1_content = fp.read()

with open("sample2.svg") as fp:
    svg_2_content = fp.read()
svg_1_element = svglib.svg2rlg(io.StringIO(svg_1_content))
svg_2_element = svglib.svg2rlg(io.StringIO(svg_2_content))
width = 100
height = 100
svg_element = svglib.svg2rlg(io.StringIO(background_content))
d = Drawing(width, height) # setting the width and height
svg_1_element.scale(width / svg_1_element.width, height / svg_2_element.height)
svg_2_element.scale(width / svg_1_element.width, height / svg_2_element.height)
d.add(svg_1_element)
d.add(svg_2_element)

s = getStringIO()
c = SVGCanvas((d.width, d.height))
draw(d, c, 0, 0)
c.save(s)