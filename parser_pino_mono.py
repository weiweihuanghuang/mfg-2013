from xml.dom import minidom
import sys

dirnamef1 = sys.argv[2]
dirnamef2 = sys.argv[3]

charname = sys.argv[1]

font_a =  dirnamef1 +"/"+charname 
font_b =  dirnamef2 +"/"+charname 

print """ 
% File parsed with ufo2mf (UFO to Metafont) by Simon Egli and Walter Egli  %

% box dimension definition %
"""
glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('advance') 

w = itemlist[0].attributes['width'].value
w = str(float(w)/100)

glif = minidom.parse(font_b)
itemlist = glif.getElementsByTagName('advance') 

w2 = itemlist[0].attributes['width'].value
w2 = str(float(w2)/100)

glyph = glif.getElementsByTagName('glyph')
g = glyph[0].attributes['name'].value 

uni = minidom.parse(font_a) 
itemlist = uni.getElementsByTagName('unicode')
u = itemlist[0].attributes['hex'].value

mean = ['a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z', 'h', 'b', 'd','bar']
des = ['g', 'j', 'p', 'q', 'y']
dept = ['g', 'j', 'p', 'q', 'y']
asc = ['bar', 'k', 'i', 'l', 't', 'f']
cap = ['f', 'A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# ggroup=""

if g in mean :
    ggroup = 'mean#'
    
if g in des :
    ggroup = 'des#'

if g in dept :
    ggroup2 = '0'
else : 
    ggroup2 = '0'

if g in cap : 
    ggroup = 'cap#'

if g in asc :
    ggroup = 'asc#'

#else :
#    ggroup = 'asc#'


print 'beginfontchar("' + g + '", (' + w + '*A_width + metapolation * (' + w + '*A_width - ' + w2 + '*B_width)) * width_' + g + "+ width_" +  g  + "R#, A_" + ggroup + " + metapolation * (B_" + ggroup + " - A_" + ggroup + "), " + ggroup2 + ");"
print """if known ps_output:
glyph_name "uni""" + u + """"; 
fi
"""

# reading l and r as pxl and pxr font A

print """ 
% point coordinates font A
"""

glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
for item in itemlist :
  for i in range (0,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       x = str(float(x)/100)
       y = str(float(y)/100)
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :
           print "px" + znamer[1:] + " := " + x + "u ; "   +  "py"+ znamer[1:] + " := " + y + "u ;"   
         if im.value.find(znamel)>-1 :
           print "px" + znamel[1:] + " := " + x + "u ; "   +  "py"+ znamel[1:] + " := " + y + "u ;"   



# reading mid points Font A

glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

print """
% reading mid points font A
""" 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :
        
                print ".5(px"+ znamel[1:] + " + px" + znamer[1:] + ") = x2" + zname[1:-1] +"0;"   
                print ".5(py"+ znamel[1:] + " + py" + znamer[1:] + ") = y2" + zname[1:-1] +"0;"   


# reading fake 100 l and r points Font A

glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

print """
% fake extra l an r for metafont
""" 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

   
     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :

                print "px"+ znamel[1:] + " = x"+ znamel[1:-1] + "Bl; py"+ znamel[1:] + " = y"+ znamel[1:-1] + "Bl; " 
                print "px"+ znamer[1:] + " = x"+ znamer[1:-1] + "Br; py"+ znamer[1:] + " = y"+ znamer[1:-1] + "Br; " 



# reading pen widhts Font A

glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

print """
% pen width
""" 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

     
     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :

                print "dist"+ znamel[1:-1] + " := length (z"+ znamel[1:-1] + "Bl-" + "z"+ znamel[1:-1] + "Br) ;" 

# reading l and r as ppxl and ppxr font B

print """ 
% point coordinates font B
"""


glif = minidom.parse(font_b)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       x = str(float(x)/100)
       y = str(float(y)/100)
       im =item.attributes['name'] 
       ipn = 1   

     except : 
       inattr=inattr+1 

     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :
           print "ppx" + znamer[1:] + " := " + x + "u ; "   +  "ppy"+ znamer[1:] + " := " + y + "u ;"   
         if im.value.find(znamel)>-1 :
           print "ppx" + znamel[1:] + " := " + x + "u ; "   +  "ppy"+ znamel[1:] + " := " + y + "u ;"   




# reading mid points Font B

glif = minidom.parse(font_b)
itemlist = glif.getElementsByTagName('point') 

print """
% reading mid points font B
""" 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

    
     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :

                print ".5(ppx"+ znamel[1:] + " + ppx" + znamer[1:] + ") = x2" + zname[1:-1] +"A;"   
                print ".5(ppy"+ znamel[1:] + " + ppy" + znamer[1:] + ") = y2" + zname[1:-1] +"A;"   



# reading fake 100 l and r points Font B

glif = minidom.parse(font_b)
itemlist = glif.getElementsByTagName('point') 

print """
% fake extra l an r for font B
""" 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

    
     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :
         
                print "ppx"+ znamel[1:] + " = x"+ znamel[1:-1] + "Cl; ppy"+ znamel[1:] + " = y"+ znamel[1:-1] + "Cl; " 
                print "ppx"+ znamer[1:] + " = x"+ znamer[1:-1] + "Cr; ppy"+ znamer[1:] + " = y"+ znamer[1:-1] + "Cr; " 





# reading pen widhts Font B

glif = minidom.parse(font_b)
itemlist = glif.getElementsByTagName('point') 

print """
% pen width Font B
""" 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

     
     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :

                print "dist"+ znamel[1:-1] + "B := length (z"+ znamel[1:-1] + "Cl-" + "z"+ znamel[1:-1] + "Cr) ;" 
                





# reading pen angle Font A

glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

print """
% pen angle Font A
""" 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     zname = 'z'+str(i)+'r'

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

    
     if ipn == 1 :
       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
         if im.value.find(znamer)>-1 :

                print "ang"+ znamel[1:-1] + " := angle((" + znamel[0:-1] + "Br + (metapolation * (" + znamel[0:-1] + "Cr -" + znamel[0:-1] + "Br))) - (" + znamel[0:-1] + "Bl + (metapolation * (" + znamel[0:-1] + "Cl -" + znamel[0:-1] + "Bl))));" 




print """

% test new vertical and horizontal option
""" 


glyph = glif.getElementsByTagName('glyph')
g = glyph[0].attributes['name'].value


mean = ['a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z', 'h', 'b', 'd']
des = ['g', 'j', 'p', 'q', 'y']
asc = ['bar','k', 'i', 'l', 't', 'f']
cap = ['f', 'A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# ggroup=""

if g in mean :
    ggroup = 'xheight'
    
if g in des :
    ggroup = 'descender'
        
if g in cap : 
    ggroup = 'capital'

if g in asc :
    ggroup = 'ascender'


glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
ivn = 0
stre = " ... "
strtwo = " .. "
stline = " -- "
strz = ""
zzn = []
startp = []
startpval = []

# create empty variable list


pointshifted= []
pointshiftedval= []

pointshiftedy = []
pointshiftedyval = []

v = []
vval = []

h = []
hval = []


# add iteration to string

for i in range (1,100):
  startp.append("")
  startpval.append(0)
  
  pointshifted.append("")
  pointshiftedval.append(0)

  pointshiftedy.append("")
  pointshiftedyval.append(0)

  v.append("")
  vval.append(0)

  h.append("")
  hval.append(0)




# search for parameter values
  
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     
     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 

       try :
	 ipointshifted = item.attributes['pointshifted'].value   
	 ipointshifted = True
       except :
       	 ipointshifted = False

       try :
	 ipointshiftedy = item.attributes['pointshiftedy'].value   
	 ipointshiftedy = True
       except :
       	 ipointshiftedy = False

       try :
	 istartp = item.attributes['startp'].value   
	 istartp = True
       except :
       	 istartp = False

       try :
	 iv = item.attributes['v'].value   
	 iv = True
       except :
       	 iv = False

       try :
	 ih = item.attributes['h'].value   
	 ih = True
       except :
       	 ih = False



       ipn = 1   
     except : 
       inattr=inattr+1 


     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:
#         if im.value.find("startp") >-1 :
#           del startp[i-1]
#           startp.insert(i-1,"")
         if istartp == True :
           istartpval = item.attributes['startp'].value
           del startp[i-1]
           startp.insert(i-1,"startp")
	   del startpval[i-1]
           startpval.insert(i-1,istartpval)

         if ipointshifted== True :
           ipointshiftedval= item.attributes['pointshifted'].value
           del pointshifted[i-1]
           pointshifted.insert(i-1,"shifted")
	   del pointshiftedval[i-1]
           pointshiftedval.insert(i-1,ipointshiftedval)

         if ipointshiftedy == True :
           ipointshiftedyval = item.attributes['pointshiftedy'].value
           del pointshiftedy[i-1]
           pointshiftedy.insert(i-1,"shifted")
	   del pointshiftedyval[i-1]
           pointshiftedyval.insert(i-1,ipointshiftedyval)

         if iv == True :
           ivval = item.attributes['v'].value
           del v[i-1]
           v.insert(i-1,"v")
	   del vval[i-1]
           vval.insert(i-1,ivval)

         if ih == True :
           ihval = item.attributes['h'].value
           del h[i-1]
           h.insert(i-1,"h")
	   del hval[i-1]
           hval.insert(i-1,ihval)



nnz = 0
for zitem in zzn :
  nnz = nnz +1 


i = 0
zzn.sort()
zeile =""
zeileend =""
semi = ");"
for i in range (0,nnz) :
  zitem = zzn[i]
  
  zitemb = zzn[i]
  zitemc = zzn[i-1]

## default string

  zeile =""

  zeileb = "ang" + str(zitem) + "V := ang" + str(zitem) + "; dist" + str(zitem) + "V := dist" + str(zitem) + ";" 
#  zeilec = "ang" + str(zitemb) + "V := ang" + str(zitemb) + ";"

#  zeile = "z"+str(zitem)+ "=(x2"+ str(zitem)+ "0 *width *width_" + g + "+ (metapolation * (x2"+str(zitem)+"A - x2" +str(zitem)+"0)), y2"+str(zitem)+ "0 *" + ggroup + " + (metapolation * (y2"+str(zitem)+ "A - y2" +str(zitem)+ "0))"
  
#  zeileend =""
#  zeileend = 'z'+str(zzn[nnz-1])+ "=(x2"+ str(zzn[nnz-1])+ "0 *width *width_" + g + " + (metapolation * (x2"+str(zzn[nnz-1])+"A - x2" +str(zzn[nnz-1])+"0)), y2"+str(zzn[nnz-1])+ "0 *" + ggroup + " + (metapolation * (y2"+str(zzn[nnz-1]) + "A - y2" +str(zzn[nnz-1])+ "0))"
 

# parameters 

#  if pointshifted[i] <> "" :
#    zeile = zeile + "dist" +str(zitem) + "vertical := length (py"  +str(zitem) + "l-py"  +str(zitem) + "r) ;"
  if h[i] <> "" :
   zeile = zeile + "dist" +str(zitem) + "V := length (px"  +str(zitem) + "l-px"  +str(zitem) + "r) ;"
   zeile = zeile + "if px" + str(zitem) + "l < px"  +str(zitem) + "r: ang" + str(zitem) + "V := 0; else: ang" + str(zitem) + "V := 180; fi" 
  
  else :
     if v[i] <> "" :
       zeile = zeile + "dist" +str(zitem) + "V := length (py"  +str(zitem) + "l-py"  +str(zitem) + "r) ;"
       zeile = zeile + "if py" + str(zitem) + "l < py"  +str(zitem) + "r: ang" + str(zitem) + "V := 90; else: ang" + str(zitem) + "V := -90; fi" 

     else: 
       zeile = zeile + zeileb

  print zeile
  




#

#zeile = zeile
#print zeile
 


####### new penpos




        
# reading font Pen strokes

print """

% test new penpos
""" 

glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 



inattr=0   
ivn = 0
strz = ""
zzn = []

# create empty variable list

stemcutter = []
stemcutterval = []


# add iteration to string

for i in range (1,100):

  stemcutter.append("")
  stemcutterval.append(0)

# search for parameter values
  
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     
     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 

       try :
	 istemcutter = item.attributes['stemcutter'].value   
	 istemcutter = True
       except :
       	 istemcutter = False

       ipn = 1   
     except : 
       inattr=inattr+1 


     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:

         if istemcutter == True :
           istemcutterval = item.attributes['stemcutter'].value
           del stemcutter[i-1]
           stemcutter.insert(i-1,"stemcutter")
	   del stemcutterval[i-1]
           stemcutterval.insert(i-1,istemcutterval)


nnz = 0
for zitem in zzn :
  nnz = nnz +1 


i = 0
zzn.sort()
zeile =""
zeileend =""
semi = ";"
close = ")"
for i in range (0,nnz) :
  zitem = zzn[i]
  
  zitemb = zzn[i]
  zitemc = zzn[i-1]

## default string

  zeile =""

  zeile = """penpos"""  +str(zitem) + "(dist" +str(zitem) + " + (A_px + metapolation * (B_px - A_px)) + ((A_skeleton/50 + metapolation * (B_skeleton/50-A_skeleton/50)) * dist" +str(zitem) + ")"


#  zeile = """penpos""" + znamel[1:-1] + "(dist" + znamel[1:-1] + " + (metapolation * (px - (dist"+znamel[1:-1] + " + (distV * (dist" + znamel[1:-1] + "V - dist" +znamel[1:-1] + "))))), (ang"+znamel[1:-1] + " + (angV * (ang" + znamel[1:-1] + "V - ang" + znamel[1:-1] +"))));"


# parameters 

  if stemcutter[i] <> "" :
    zeile = zeile + "-" + stemcutter[i] + "(" +  str(stemcutterval[i]) + ")"      
 
  else: 
     zeile = zeile 
  zeile = zeile + ", ang" +str(zitem) + ");"
  print zeile

#zeile = zeileend + semi

#print zeile
 












############




#print """
#% pen positions 
#""" 


# reading font Pen Positions

#glif = minidom.parse(font_a)
#itemlist = glif.getElementsByTagName('point') 

#inattr=0   
#for item in itemlist :
#  for i in range (1,100):
#     znamel = 'z'+str(i)+'l'
#     znamer = 'z'+str(i)+'r'
#     zname = 'z'+str(i)+'r'

#     ipn=0
#     try :
#       x = item.attributes['x'].value
#       y = item.attributes['y'].value
#       im =item.attributes['name'] 
#       ipn = 1   
#     except : 
#       inattr=inattr+1 
#        
#     if ipn == 1 :
#       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
#         if im.value.find(znamer)>-1 :
         
#            print """penpos""" + znamel[1:-1] + "(dist"+znamel[1:-1] + " + (metapolation * (px - dist"+znamel[1:-1] + ")), ang"+znamel[1:-1] + ");"
#            print """penpos""" + znamel[1:-1] + "(dist" + znamel[1:-1] + " + (metapolation * (px - (dist"+znamel[1:-1] + " + (distV * (dist" + znamel[1:-1] + "V - dist" +znamel[1:-1] + "))))), (ang"+znamel[1:-1] + " + (angV * (ang" + znamel[1:-1] + "V - ang" + znamel[1:-1] +"))));"




        
# reading font Pen strokes

print """

% test new center (z) points
""" 


glyph = glif.getElementsByTagName('glyph')
g = glyph[0].attributes['name'].value


mean = ['a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z', 'h', 'b', 'd']
des = ['g', 'j', 'p', 'q', 'y']
asc = ['bar','k', 'i', 'l', 't', 'f']
cap = ['f', 'A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# ggroup=""

if g in mean :
    ggroup = 'xheight'
    
if g in des :
    ggroup = 'descender'
        
if g in cap : 
    ggroup = 'capital'

if g in asc :
    ggroup = 'ascender'


glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
ivn = 0
stre = " ... "
strtwo = " .. "
stline = " -- "
strz = ""
zzn = []
startp = []
startpval = []

# create empty variable list


pointshifted= []
pointshiftedval= []

pointshiftedy = []
pointshiftedyval = []

v = []
vval = []

h = []
hval = []

overx = []
overxval = []

overbase = []
overbaseval = []

overcap = []
overcapval = []




# add iteration to string

for i in range (1,100):
  startp.append("")
  startpval.append(0)
  
  pointshifted.append("")
  pointshiftedval.append(0)

  pointshiftedy.append("")
  pointshiftedyval.append(0)


  v.append("")
  vval.append(0)

  h.append("")
  hval.append(0)

  overx.append("")
  overxval.append(0)

  overbase.append("")
  overbaseval.append(0)

  overcap.append("")
  overcapval.append(0)





# search for parameter values
  
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     
     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 

       try :
	 ipointshifted = item.attributes['pointshifted'].value   
	 ipointshifted = True
       except :
       	 ipointshifted = False

       try :
	 ipointshiftedy = item.attributes['pointshiftedy'].value   
	 ipointshiftedy = True
       except :
       	 ipointshiftedy = False

       try :
	 istartp = item.attributes['startp'].value   
	 istartp = True
       except :
       	 istartp = False


       try :
	 iv = item.attributes['v'].value   
	 iv = True
       except :
       	 iv = False

       try :
	 ih = item.attributes['h'].value   
	 ih = True
       except :
       	 ih = False

       try :
	 ioverx = item.attributes['overx'].value   
	 ioverx = True
       except :
       	 ioverx = False

       try :
	 ioverbase = item.attributes['overbase'].value   
	 ioverbase = True
       except :
       	 ioverbase = False

       try :
	 iovercap = item.attributes['overcap'].value   
	 iovercap = True
       except :
       	 iovercap = False





       ipn = 1   
     except : 
       inattr=inattr+1 


     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:
#         if im.value.find("startp") >-1 :
#           del startp[i-1]
#           startp.insert(i-1,"")
         if istartp == True :
           istartpval = item.attributes['startp'].value
           del startp[i-1]
           startp.insert(i-1,"startp")
	   del startpval[i-1]
           startpval.insert(i-1,istartpval)

         if ipointshifted== True :
           ipointshiftedval= item.attributes['pointshifted'].value
           del pointshifted[i-1]
           pointshifted.insert(i-1,"shifted")
	   del pointshiftedval[i-1]
           pointshiftedval.insert(i-1,ipointshiftedval)

         if ipointshiftedy == True :
           ipointshiftedyval = item.attributes['pointshiftedy'].value
           del pointshiftedy[i-1]
           pointshiftedy.insert(i-1,"shifted")
	   del pointshiftedyval[i-1]
           pointshiftedyval.insert(i-1,ipointshiftedyval)

         if iv == True :
           ivval = item.attributes['v'].value
           del v[i-1]
           v.insert(i-1,"v")
	   del vval[i-1]
           vval.insert(i-1,ivval)

         if ih == True :
           ihval = item.attributes['h'].value
           del h[i-1]
           h.insert(i-1,"h")
	   del hval[i-1]
           hval.insert(i-1,ihval)

         if ioverx == True :
           ioverxval = item.attributes['overx'].value
	   del overx[i-1]
           overx.insert(i-1,"shifted")
	   del overxval[i-1]
           overxval.insert(i-1,ioverxval)

         if ioverbase == True :
           ioverbaseval = item.attributes['overbase'].value
	   del overbase[i-1]
           overbase.insert(i-1,"shifted")
	   del overbaseval[i-1]
           overbaseval.insert(i-1,ioverbaseval)

         if iovercap == True :
           iovercapval = item.attributes['overcap'].value
	   del overcap[i-1]
           overcap.insert(i-1,"shifted")
	   del overcapval[i-1]
           overcapval.insert(i-1,iovercapval)


nnz = 0
for zitem in zzn :
  nnz = nnz +1 


i = 0
zzn.sort()
zeile =""
zeileend =""
semi = ";"
close = ")"
for i in range (0,nnz) :
  zitem = zzn[i]
  
  zitemb = zzn[i]
  zitemc = zzn[i-1]

## default string

  zeile =""

  zeile = "z"+str(zitem)+ "=((A_width + metapolation * (A_width - B_width)) * (x2"+ str(zitem)+ "0 + metapolation * (x2"+str(zitem)+"A - x2" +str(zitem)+"0) + width_" + g + "L) * width_" + g + ", (A_" + ggroup + " + metapolation * (B_" + ggroup + " - A_" + ggroup + "))*(y2"+str(zitem)+ "0 + metapolation *(y2"+str(zitem)+ "A - y2" +str(zitem)+ "0)))"

#  zeileend =""
#  zeileend = 'z'+str(zzn[nnz-1])+ "=(x2"+ str(zzn[nnz-1])+ "0 *width *width_" + g + " + (metapolation * (x2"+str(zzn[nnz-1])+"A - x2" +str(zzn[nnz-1])+"0)), y2"+str(zzn[nnz-1])+ "0 *" + ggroup + " + (metapolation * (y2"+str(zzn[nnz-1]) + "A - y2" +str(zzn[nnz-1])+ "0)))"
 

# parameters 

  if pointshifted[i] <> "" :
    zeile = zeile +" shifted (" + str(pointshiftedval[i]) + ",0)"       

#  if overx[i] <> "" :
#    zeile = zeile + " shifted (0, mean-y" + str(overxval[i]) + ") + (0, over)"    

  if overx[i] <> "" :
      zeile = zeile + " shifted (0, (A_mean + metapolation * (A_mean - B_mean)) - y" + str(zitem) + str(overxval[i]) + ") + (0, over)" 

  if overbase[i] <> "" :
      zeile = zeile + " shifted (0, - y" + str(zitem) + str(overbaseval[i]) + ") - (0, over)" 

  if overcap[i] <> "" :
      zeile = zeile + " shifted (0, (A_cap + metapolation * (A_cap - B_cap)) - y" + str(zitem) + str(overcapval[i]) + ") + (0, over)" 

 
 
  else: 
     zeile = zeile 
  zeile = zeile + semi 
  print zeile

#zeile = zeileend + semi

#print zeile
 



# reading values functions font B


glif = minidom.parse(font_b)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
ivn = 0
stre = " ... "
strtwo = " .. "
stline = " -- "
strz = ""
zzn = []

startp = []
startpval = []

doubledash = []
doubledashvalB = []

tripledash = []
tripledashvalB = []

tension = []
tensionvalB = []

tensionand = []
tensionandvalB = []
tensionandval2B = []

superright = []
superrightvalB = []

superleft = []
superleftvalB = []

dir = []
dirvalB = []

leftp = []
leftpvalB = []

right = []
rightvalB = []

upp = []
uppvalB = []

downp = []
downpvalB = []

penshiftedy = []
penshiftedyvalB = []

penshifted = []
penshiftedvalB = []

for i in range (1,100):

  startp.append("")
  startpval.append(0)

  doubledash.append("")
  doubledashvalB.append(0)

  tripledash.append("")
  tripledashvalB.append(0)

  tension.append("")
  tensionvalB.append(0)
  
  tensionand.append("")
  tensionandvalB.append(0)
  tensionandval2B.append(0)

  superright.append("")
  superrightvalB.append(0)
  
  superleft.append("")
  superleftvalB.append(0)
  
  dir.append("")
  dirvalB.append(0)

  leftp.append("")
  leftpvalB.append(0)

  right.append("")
  rightvalB.append(0)

  upp.append("")
  uppvalB.append(0)

  downp.append("")
  downpvalB.append(0)
  
  penshiftedy.append("")
  penshiftedyvalB.append(0)

  penshifted.append("")
  penshiftedvalB.append(0)


  
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 


       try :
	 idoubledash = item.attributes['doubledash'].value   
	 idoubledash = True
       except :
       	 idoubledash = False

       try :
	 itripledash = item.attributes['tripledash'].value   
	 itripledash = True
       except :
       	 itripledash = False

       try :
	 idir = item.attributes['dir'].value   
	 idir = True
       except :
       	 idir = False

       try :
	 ileftp = item.attributes['leftp'].value   
	 ileftp = True
       except :
       	 ileftp = False

       try :
	 iupp = item.attributes['upp'].value   
	 iupp = True
       except :
       	 iupp = False

       try :
	 iright = item.attributes['right'].value   
	 iright = True
       except :
       	 iright = False

       try :
	 idownp = item.attributes['downp'].value   
	 idownp = True
       except :
       	 idownp = False

       try :
	 itension = item.attributes['tension'].value   
	 itension = True
       except :
       	 itension = False

       try :
	 itensionand = item.attributes['tensionand'].value   
	 itensionand = True

       except :
       	 itensionand = False

       try :
	 isuperright = item.attributes['superright'].value   
	 isuperright = True
       except :
       	 isuperright = False

       try :
	 isuperleft = item.attributes['superleft'].value   
	 isuperleft = True
       except :
       	 isuperleft = False

       try :
	 ipenshifted = item.attributes['penshifted'].value   
	 ipenshifted = True
       except :
       	 ipenshifted = False

       try :
	 ipenshiftedy = item.attributes['penshiftedy'].value   
	 ipenshiftedy = True
       except :
       	 ipenshiftedy = False


       ipn = 1   
     except : 
       inattr=inattr+1 


     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:
#         if im.value.find("startp") >-1 :
#           del zzstartp[i-1]
#           zzstartp.insert(i-1,"penstroke ")
             
         if idoubledash == True :
           idoubledashval = item.attributes['doubledash'].value
           del doubledash[i-1]
           doubledash.insert(i-1,"doubledash")
	   del doubledashvalB[i-1]
           doubledashvalB.insert(i-1,idoubledashval)

         if itripledash == True :
           itripledashval = item.attributes['tripledash'].value
           del tripledash[i-1]
           tripledash.insert(i-1," ---")
	   del tripledashvalB[i-1]
           tripledashvalB.insert(i-1,itripledashval)

         if idir == True :
           idirval = item.attributes['dir'].value
           del dir[i-1]
           dir.insert(i-1,"dir")
	   del dirvalB[i-1]
           dirvalB.insert(i-1,idirval)
      
         if iupp == True :
           iuppval = item.attributes['upp'].value
           del upp[i-1]
           upp.insert(i-1,"up")
	   del uppvalB[i-1]
           uppvalB.insert(i-1,iuppval)

         if ileftp == True :
           ileftpval = item.attributes['leftp'].value
           del leftp[i-1]
           leftp.insert(i-1,"left")
	   del leftpvalB[i-1]
           leftpvalB.insert(i-1,ileftpval)

         if iright == True :
           irightval = item.attributes['right'].value
           del right[i-1]
           right.insert(i-1,"right")
	   del rightvalB[i-1]
           rightvalB.insert(i-1,irightval)

         if idownp == True :
           idownpval = item.attributes['downp'].value
           del downp[i-1]
           downp.insert(i-1,"down")
	   del downpvalB[i-1]
           downpvalB.insert(i-1,idownpval)
                  
         if itension == True :
           itensionval = item.attributes['tension'].value
           del tension[i-1]
           tension.insert(i-1,"tension")
	   del tensionvalB[i-1]
           tensionvalB.insert(i-1,itensionval)

         if itensionand == True :
           itensionandval = item.attributes['tensionand'].value
           del tensionand[i-1]
           tensionand.insert(i-1,"tensionand")
	   del tensionandvalB[i-1]
           del tensionandval2B[i-1]
           tensionandvalB.insert(i-1,itensionandval[:3])
           tensionandval2B.insert(i-1,itensionandval[-3:])

         if isuperright == True :
           isuperrightval = item.attributes['superright'].value
           del superright[i-1]
           superright.insert(i-1,"superright")
	   del superrightvalB[i-1]
           superrightvalB.insert(i-1,isuperrightval)

         if isuperleft == True :
           isuperleftval = item.attributes['superleft'].value
           del superleft[i-1]
           superleft.insert(i-1,"superleft")
	   del superleftvalB[i-1]
           superleftvalB.insert(i-1,isuperleftval)

         if idir == True :
           idirval = item.attributes['dir'].value
           del dir[i-1]
           dir.insert(i-1,"dir")
	   del dirvalB[i-1]
           dirvalB.insert(i-1,idirval)

         if ipenshifted == True :
           ipenshiftedval = item.attributes['penshifted'].value
           del penshifted[i-1]
           penshifted.insert(i-1,"shifted")
	   del penshiftedvalB[i-1]
           penshiftedvalB.insert(i-1,ipenshiftedval)

         if ipenshiftedy == True :
           ipenshiftedyval = item.attributes['penshiftedy'].value
           del penshiftedy[i-1]
           penshiftedy.insert(i-1,"shifted")
	   del penshiftedyvalB[i-1]
           penshiftedyvalB.insert(i-1,ipenshiftedyval)



print """
% penstrokes
"""
           
# reading font penstrokes


glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
ivn = 0
stre = " ... "
tripledash = "---"
strtwo = " .. "
stline = " -- "
strz = ""
zzn = []
startp = []
startpval = []

doubledash = []
doubledashval = []

tripledash = []
tripledashval = []

tension = []
tensionval = []

tensionand = []
tensionandval = []
tensionandval2 = []

superright = []
superrightval = []

superleft = []
superleftval = []

dir = []
dirval = []

leftp = []
leftpval = []

right = []
rightval = []

upp = []
uppval = []

downp = []
downpval = []

dir2 = []
dir2val = []

leftp2 = []
leftp2val = []

right2 = []
right2val = []

upp2 = []
upp2val = []

downp2= []
downp2val = []

penshiftedy = []
penshiftedyval = []

penshifted = []
penshiftedval = []

overx = []
overxval = []

overbase = []
overbaseval = []

overcap = []
overcapval = []


cycle = []
cycleval = []

for i in range (1,100):

  startp.append("")
  startpval.append(0)

  doubledash.append("")
  doubledashval.append(0)

  tripledash.append("")
  tripledashval.append(0)

  tension.append("")
  tensionval.append(0)
  
  tensionand.append("")
  tensionandval.append(0)
  tensionandval2.append(0)

  superright.append("")
  superrightval.append(0)
  
  superleft.append("")
  superleftval.append(0)
  
  dir.append("")
  dirval.append(0)

  leftp.append("")
  leftpval.append(0)

  right.append("")
  rightval.append(0)

  upp.append("")
  uppval.append(0)

  downp.append("")
  downpval.append(0)

  dir2.append("")
  dir2val.append(0)

  leftp2.append("")
  leftp2val.append(0)

  right2.append("")
  right2val.append(0)

  upp2.append("")
  upp2val.append(0)
  
  downp2.append("")
  downp2val.append(0)

  penshiftedy.append("")
  penshiftedyval.append(0)

  penshifted.append("")
  penshiftedval.append(0)

  overx.append("")
  overxval.append(0)

  overbase.append("")
  overbaseval.append(0)

  overcap.append("")
  overcapval.append(0)

  cycle.append("")
  cycleval.append(0)






  
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 


       try :
	 istartp = item.attributes['startp'].value   
	 istartp = True
       except :
       	 istartp = False

       try :
	 idoubledash = item.attributes['doubledash'].value   
	 idoubledash = True
       except :
       	 idoubledash = False

       try :
	 itripledash = item.attributes['tripledash'].value   
	 itripledash = True
       except :
       	 itripledash = False

       try :
	 idir = item.attributes['dir'].value   
	 idir = True
       except :
       	 idir = False

       try :
	 idir2 = item.attributes['dir2'].value   
	 idir2 = True
       except :
       	 idir2 = False

       try :
	 ileftp = item.attributes['leftp'].value   
	 ileftp = True
       except :
       	 ileftp = False

       try :
	 ileftp2 = item.attributes['leftp2'].value   
	 ileftp2 = True
       except :
       	 ileftp2 = False

       try :
	 iupp = item.attributes['upp'].value   
	 iupp = True
       except :
       	 iupp = False

       try :
	 iupp2 = item.attributes['upp2'].value   
	 iupp2 = True
       except :
       	 iupp2 = False

       try :
	 iright = item.attributes['right'].value   
	 iright = True
       except :
       	 iright = False

       try :
	 iright2 = item.attributes['right2'].value   
	 iright2 = True
       except :
       	 iright2 = False

       try :
	 idownp = item.attributes['downp'].value   
	 idownp = True
       except :
       	 idownp = False

       try :
	 idownp2= item.attributes['downp2'].value   
	 idownp2= True
       except :
       	 idownp2= False


       try :
	 itension = item.attributes['tension'].value   
	 itension = True
       except :
       	 itension = False

       try :
	 itensionand = item.attributes['tensionand'].value   
	 itensionand = True
       except :
       	 itensionand = False

       try :
	 isuperright = item.attributes['superright'].value   
	 isuperright = True
       except :
       	 isuperright = False

       try :
	 isuperleft = item.attributes['superleft'].value   
	 isuperleft = True
       except :
       	 isuperleft = False

       try :
	 ipenshifted = item.attributes['penshifted'].value   
	 ipenshifted = True
       except :
       	 ipenshifted = False

       try :
	 ipenshiftedy = item.attributes['penshiftedy'].value   
	 ipenshiftedy = True
       except :
       	 ipenshiftedy = False

       try :
	 ioverx = item.attributes['overx'].value   
	 ioverx = True
       except :
       	 ioverx = False

       try :
	 ioverbase = item.attributes['overbase'].value   
	 ioverbase = True
       except :
       	 ioverbase = False

       try :
	 iovercap = item.attributes['overcap'].value   
	 iovercap = True
       except :
       	 iovercap = False

       try :
	 icycle = item.attributes['cycle'].value   
	 icycle = True
       except :
       	 icycle = False






       ipn = 1   
     except : 
       inattr=inattr+1 


     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:
        
#	 if im.value.find("startp") >-1 :
#           del zzstartp[i-1]
#           zzstartp.insert(i-1,"penstroke ")

         if istartp == True :
           istartpval = item.attributes['startp'].value
           del startp[i-1]
           startp.insert(i-1,"penstroke ")
	   del startpval[i-1]
           startpval.insert(i-1,istartpval)
  
         if icycle == True :
           icycleval = item.attributes['cycle'].value
           del startp[i-1]
           cycle.insert(i-1,"cycle")
	   del cycleval[i-1]
           cycleval.insert(i-1,icycleval)
               
         if idoubledash == True :
           idoubledashval = item.attributes['doubledash'].value
           del doubledash[i-1]
           doubledash.insert(i-1," -- ")
	   del doubledashval[i-1]
           doubledashval.insert(i-1,idoubledashval)

         if itripledash == True :
           itripledashval = item.attributes['tripledash'].value
           del tripledash[i-1]
           tripledash.insert(i-1," ---")
	   del tripledashval[i-1]
           tripledashval.insert(i-1,itripledashval)

         if idir == True :
           idirval = item.attributes['dir'].value
           del dir[i-1]
           dir.insert(i-1,"dir")
	   del dirval[i-1]
           dirval.insert(i-1,idirval)
      
         if idir2 == True :
           idir2val = item.attributes['dir2'].value
           del dir2[i-1]
           dir2.insert(i-1,"dir")
	   del dir2val[i-1]
           dir2val.insert(i-1,idir2val)
      
         if iupp == True :
           iuppval = item.attributes['upp'].value
           del upp[i-1]
           upp.insert(i-1,"{up} ")
	   del uppval[i-1]
           uppval.insert(i-1,iuppval)

         if ileftp == True :
           ileftpval = item.attributes['leftp'].value
           del leftp[i-1]
           leftp.insert(i-1,"{left} ")
	   del leftpval[i-1]
           leftpval.insert(i-1,ileftpval)

         if iright == True :
           irightval = item.attributes['right'].value
           del right[i-1]
           right.insert(i-1,"{right} ")
	   del rightval[i-1]
           rightval.insert(i-1,irightval)

         if idownp == True :
           idownpval = item.attributes['downp'].value
           del downp[i-1]
           downp.insert(i-1," {down} ")
	   del downpval[i-1]
           downpval.insert(i-1,idownpval)

         if idownp2 == True :
           idownp2val = item.attributes['downp2'].value
           del downp2[i-1]
           downp2.insert(i-1," {down} ")
	   del downp2val[i-1]
           downp2val.insert(i-1,idownp2val)

         if iupp2 == True :
           iupp2val = item.attributes['upp2'].value
           del upp2[i-1]
           upp2.insert(i-1,"{up} ")
	   del upp2val[i-1]
           upp2val.insert(i-1,iupp2val)

         if ileftp2 == True :
           ileftp2val = item.attributes['leftp2'].value
           del leftp2[i-1]
           leftp2.insert(i-1,"{left} ")
	   del leftp2val[i-1]
           leftp2val.insert(i-1,ileftp2val)

         if iright2 == True :
           iright2val = item.attributes['right2'].value
           del right2[i-1]
           right2.insert(i-1,"{right} ")
	   del right2val[i-1]
           right2val.insert(i-1,iright2val)
                  
         if itension == True :
           itensionval = item.attributes['tension'].value
           del tension[i-1]
           tension.insert(i-1,"tension")
	   del tensionval[i-1]
           tensionval.insert(i-1,itensionval)

         if itensionand == True :
           itensionandval = item.attributes['tensionand'].value
           del tensionand[i-1]
           tensionand.insert(i-1,"tensionand")
	   del tensionandval[i-1]
	   del tensionandval2[i-1]
           tensionandval.insert(i-1,itensionandval[:3])
           tensionandval2.insert(i-1,itensionandval[-3:])

         if isuperright == True :
           isuperrightval = item.attributes['superright'].value
           del superright[i-1]
           superright.insert(i-1,"super_qr")
	   del superrightval[i-1]
           superrightval.insert(i-1,isuperrightval)

         if isuperleft == True :
           isuperleftval = item.attributes['superleft'].value
           del superleft[i-1]
           superleft.insert(i-1,"super_ql")
	   del superleftval[i-1]
           superleftval.insert(i-1,isuperleftval)

         if idir == True :
           idirval = item.attributes['dir'].value
           del dir[i-1]
           dir.insert(i-1,"dir")
	   del dirval[i-1]
           dirval.insert(i-1,idirval)

         if ipenshifted == True :
           ipenshiftedval = item.attributes['penshifted'].value
           del penshifted[i-1]
           penshifted.insert(i-1,"shifted")
	   del penshiftedval[i-1]
           penshiftedval.insert(i-1,ipenshiftedval)

         if ipenshiftedy == True :
           ipenshiftedyval = item.attributes['penshiftedy'].value
           del penshiftedy[i-1]
           penshiftedy.insert(i-1,"shifted")
	   del penshiftedyval[i-1]
           penshiftedyval.insert(i-1,ipenshiftedyval)

         if ioverx == True :
           ioverxval = item.attributes['overx'].value
	   del overx[i-1]
           overx.insert(i-1,"shifted")
	   del overxval[i-1]
           overxval.insert(i-1,ioverxval)

         if ioverbase == True :
           ioverbaseval = item.attributes['overbase'].value
	   del overbase[i-1]
           overbase.insert(i-1,"shifted")
	   del overbaseval[i-1]
           overbaseval.insert(i-1,ioverbaseval)

         if iovercap == True :
           iovercapval = item.attributes['overcap'].value
	   del overcap[i-1]
           overcap.insert(i-1,"shifted")
	   del overcapval[i-1]
           overcapval.insert(i-1,iovercapval)


nnz = 0
for zitem in zzn :
  nnz = nnz +1 


i = 0
zzn.sort()
zeile = ""
semi = ";"
zeilestart = ""


  

if tripledash == True :
 dash = "---"
else :
 dash = "..."

 
for i in range (0,nnz-1) :
  zitem = zzn[i]
  zitemsuper = zzn[i+1]  
  zitemc = zzn[i-1]

## default string

  zeile =""
  zeile =  str(startp[i]) +  "z"+str(zitem)+"e"  
  zeileb =""
  zeileb = str(startp[i])
  zeilec = ""
  zeilec = str(startp[i]) + "z"+str(zitem)+"e" 
  if startp[i+1]=="" : 
# if startp, add parameters

    dash = "..."
    if tripledash[i] <> "" :
      dash = "---"
    else :
      if doubledash[i] <> "" :
        dash = "--"
      else :
        if tension[i] <> "" :
          dash = ""
        else :
          if superleft[i] <> "" :
            dash = ""
          else :
            if superright[i] <> "" :
              dash = ""
            else :
              if dir2[i] <> "" :
                dash = ""



    if upp[i] <> "" :
      zeile = zeile + "{up}"      

    if downp[i] <> "" :
      zeile = zeile + "{down}"      

    if leftp[i] <> "" :
      zeile = zeile + "{left}"      

    if right[i] <> "" :
      zeile = zeile + "{right}"      

    if dir[i] <> "" :
      zeile = zeile + " {dir "+ str(dirval[i]) + "}"      

    if penshifted[i] <> "" :
      zeile = zeile + " shifted (" + str(penshiftedval[i]) + ")"      

    if penshiftedy[i] <> "" :
      zeile = zeile + " shifted (0, y" + str(penshiftedyval[i]) + ")"      

    if superleft[i] <> "" :
      zeile = zeile + strtwo + superleft[i]+"("+str(zitem)+"e," +str(zitemsuper)+"e, ["+str(superleftval[i]) + '+ (metapolation * (' + str(superleftvalB[i])+ '-' +str(superleftval[i]) + '))])' + strtwo      

    if superright[i] <> "" :
      zeile = zeile + strtwo + superright[i]+"("+str(zitem)+"e," +str(zitemsuper)+"e, ["+str(superrightval[i]) + '+ (metapolation * (' + str(superrightvalB[i])+ '-' +str(superrightval[i]) + '))])' + strtwo      
      
    if tensionand[i] <> "" :
      zeile = zeile + strtwo + "tension" + " ((" + str(tensionandval[i]) + '/100) + (metapolation * ((' + str(tensionandvalB[i]) + '/100) - (' + str(tensionandval[i]) + '/100))))' + " and ((" + str(tensionandval2[i]) + '/100) + (metapolation * ((' + str(tensionandval2B[i]) + '/100) - (' + str(tensionandval2[i]) + '/100))))' + strtwo

    if tension[i] <> "" :
      zeile = zeile + strtwo + "tension" + " ((" + tensionval[i] + '/100) + (metapolation * ((' + tensionvalB[i] + '/100) - (' + tensionval[i] + '/100))))' + strtwo 


 
    else : 
       if tension[i] > "" :
         zeile = zeile 
       else :
         if superright[i] > "" :
           zeile = zeile 
         else :
           if superleft[i] > "" :
             zeile = zeile 
           else :
             if tensionand[i] > "" :
               zeile = zeile 
             else :
               if penshifted[i] > "" :
                 zeile = zeile 
               else :
                  if tensionand[i] > "" :
                    zeile = zeile 
                  else :
                      zeile = zeile   
   

    if downp2[i] <> "" :
      zeile = zeile  + dash + downp2[i]  
    else:
      if upp2[i] <> "" :
        zeile = zeile  + dash + upp2[i]  
      else :
        if leftp2[i] <> "" :
          zeile = zeile  + dash + leftp2[i]  
        else :
          if right2[i] <> "" :
            zeile = zeile  + dash + right2[i]  
          else :
            if dir2[i] <> "" :
              zeile = zeile + "... {dir "+ str(dir2val[i]) + "}"      
            else:
              zeile = zeile + dash
   
      
# parameters before a new penpos    extra semi after else

  else: 
   
    if penshifted[i] <> "" :
      zeile = zeile + " shifted (" + str(penshiftedval[i]) + ")"       

    if penshiftedy[i] <> "" :
      zeile = zeile + " shifted (0, y" + str(penshiftedyval[i]) + ")"      

    if doubledash[i] <> "" :
      zeile = zeile + doubledash[i]    

    if cycle[i] <> "" :
      zeile = zeile + " ... cycle" + semi
 
    else : 
      if tension[i] <> "" :
        zeile = zeile + strtwo + "tension" + " (" + tensionval[i] + ' + (metapolation * (' + tensionvalB[i] + '-' + tensionval[i] + ')))' + strtwo  + downp2[i] + semi
      
    if tensionand[i] <> "" :
      zeile = zeile + strtwo + "tension" + " ((" + str(tensionandval[i]) + '/100) + (metapolation * ((' + str(tensionandvalB[i]) + '/100) - (' + str(tensionandval[i]) + '/100))))' + " and ((" + str(tensionandval2[i]) + '/100) + (metapolation * ((' + str(tensionandval2B[i]) + '/100) - (' + str(tensionandval2[i]) + '/100))))' + strtwo   + semi



      if downp2[i] <> "" :
        zeile = zeile + dash + downp2[i]  + semi
      if upp2[i] <> "" :
        zeile = zeile + dash + upp2[i]  + semi
      if leftp2[i] <> "" :
        zeile = zeile + dash  + leftp2[i]  + semi
      if right2[i] <> "" :
        zeile = zeile + dash + right2[i]  + semi
      if dir2[i] <> "" :
        zeile = zeile + " {dir "+ str(dir2val[i]) + "}"  + semi    

  
      else : 
        if tension[i] > "" :
          zeile = zeile 
        else :
          if superright[i] > "" :
            zeile = zeile 
          else :
            if superleft[i] > "" :
              zeile = zeile 
            else :
              if tensionand[i] > "" :
                zeile = zeile 
              else :
                if penshifted[i] > "" :
                  zeile = zeile 
                else :
                  if doubledash[i] > "" :
                    zeile = zeile 
                  else :
                    if tripledash[i] > "" :
                      zeile = zeile 
                    else :
                        zeile = zeile + semi  

    else :
       zeile = zeile + semi 
  print zeile


# parameters after final point 


  zitemb = zzn[i+1]
  zeile = "z"+str(zitemb)+"e" 

if penshifted[i+1] <> "" :
 zeile = zeile + " shifted (" + str(penshiftedval[i+1]) + ")"       

if penshiftedy[i+1] <> "" :
 zeile = zeile + " shifted (0, y" + str(penshiftedyval[i+1]) + ")"      

if tension[i] <> "" :
 zeile = zeile + strtwo + "tension" + " ((" + tensionval[i] + '/100) + (metapolation * ((' + tensionvalB[i] + '/100) - (' + tensionval[i] + '/100))))' + strtwo 

if cycle[i+1] <> "" :
 zeile = zeile + " cycle" 

else :
 zeile = zeile

# print closing z point

print zeile 
print semi


 
print """

% pen labels
penlabels(range 1 thru 99);
endchar;
"""
