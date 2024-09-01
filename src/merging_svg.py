from svglib.svglib import svg2rlg
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.renderSVG import SVGCanvas, draw

svg_1_element = svg2rlg("./result/accuracy.svg")
svg_2_element = svg2rlg("./result/accuracy2.svg")

width = max(svg_1_element.width, svg_2_element.width)
height = svg_1_element.height + svg_2_element.height
d = Drawing(width, height)

svg_1_element.scale(1, 1)
svg_2_element.scale(1, 1)
svg_2_element.translate(0, svg_2_element.height)

d.add(svg_1_element)
d.add(svg_2_element)

c = SVGCanvas((d.width, d.height))
draw(d, c, 0, 0)
c.save("./result/res.svg")
