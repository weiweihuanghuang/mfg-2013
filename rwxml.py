import  web
from xml.dom import minidom
import codecs


xmldoc = minidom.parse('A_.xml')
itemlist = xmldoc.getElementsByTagName('point') 

inum=0
for s in itemlist :
					# hier ein +1 nummerierungs loop einbauen !!
        inum=inum+1
	s.attributes['point']= "p" + str(inum)   	# adding new attributes and values
	print s.toxml()			# adding new attributes and values




  with codecs.open("out.xml", "w", "utf-8") as out:
     xmldoc.writexml(out)

