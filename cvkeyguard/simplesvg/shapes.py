def convert_case(text):
	s = ""
	for char in text:
		if ord(char) >= ord('A') and ord(char) <= ord('Z'):
			s += "-" + chr(ord(char) - ord('A') + ord('a'))
		else:
			s += char
	return s

class Shape:
	def __init__(self, tagname, **attrs):
		self.tagname = tagname
		self.attrs = {convert_case(k): v for k, v in attrs.items()}

	def to_xml(self, xml):
		xml.element(self.tagname).attributes(self.attrs)

class Circle(Shape):
	def __init__(self, x, y, r, *args, **kwargs):
		Shape.__init__(self, "circle", cx = x, cy = y, r = r, **kwargs)

class Rectangle(Shape):
	def __init__(self, x, y, width, height, *args, **kwargs):
		Shape.__init__(self, "rect", x = x, y = y, width = width, height = height, **kwargs)

class Line(Shape):
	def __init__(self, x1, y1, x2, y2, *args, **kwargs):
		Shape.__init__(self, "line", x1 = x1, y1 = y1, x2 = x2, y2 = y2, **kwargs)

class Group(Shape):
	def __init__(self, children=[], *args, **kwargs):
		Shape.__init__(self, "g", *args, **kwargs)
		self.children=children

	def to_xml(self, xml):
		xEl=xml.element(self.tagname).attributes(self.attrs)
		for child in self.children:
			child.to_xml(xEl)

def build_path(points):
	path = ""
	for point in points:
		path += "M" if len(path) < 1 else "L"
		path += " %d,%d " % (float(point[0]), float(point[1]))
	path += "Z"
	return path

class Polygon(Shape):
	def __init__(self, points, **kwargs):
		Shape.__init__(self, "path", d = build_path(points), **kwargs)
