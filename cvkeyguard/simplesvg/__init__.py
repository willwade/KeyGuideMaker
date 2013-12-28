from simplesvg.shapes import *
from StringIO import StringIO
import xml4h

def px(value):
	return str(value) + "px"

def rgb(r, g, b):
	return "rgb(%d,%d,%d)" % (r,g,b)

class SVG:
	def __init__(self, width, height, children = [],):
		self.width = width
		self.height = height
		self.children = children

	def __str__(self):
		return self.to_xml()
		
	def to_xml(self):
		attrs = {"xmlns": "http://www.w3.org/2000/svg", "version": "1.1", "width": px(self.width), "height": px(self.height)}
		xml = xml4h.build("svg").attributes(attrs)
		for child in self.children:
			child.to_xml(xml)
		io = StringIO()
		xml.write(writer = io)
		return io.getvalue()

	def circle(self, x, y, r, **kwargs):
		shape = Circle(x, y, r, **kwargs)
		self.children.append(shape)
		return shape

	def rectangle(self, x, y, width, height, **kwargs):
		shape = Rectangle(x, y, width, height, **kwargs)
		self.children.append(shape)
		return shape

	def line(self, x1, y1, x2, y2, **kwargs):
		shape = Line(x1, y1, x2, y2, **kwargs)
		self.children.append(shape)
		return shape

	def group(self, children=[], **kwargs):
		shape = Group(children, **kwargs)
		self.children.append(shape)
		return shape

	def polygon(self, points, **kwargs):
		shape = Polygon(points, **kwargs)
		self.children.append(shape)
		return shape
