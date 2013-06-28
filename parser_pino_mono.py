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

mean = ['a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z', 'h', 'b', 'd']
des = ['g', 'j', 'p', 'q', 'y']
asc = ['k', 'i', 'l', 't', 'f']
cap = ['f', 'A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

if g in mean :
    ggroup = 'mean#'
    
if g in des :
    ggroup = 'des#'
        
if g in cap : 
    ggroup = 'cap#'

if g in asc :
    ggroup = 'asc#'

#else :
#    ggroup = 'asc#'


print 'beginfontchar("' + g + '", (' + w + "*width *width_" +  g  + " +px#) + (incx * (" + w2 + '-' + w + ")), " + ggroup + ", 0);"
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

                print "ang"+ znamel[1:-1] + " := angle((" + znamel[0:-1] + "Br + (incx * (" + znamel[0:-1] + "Cr -" + znamel[0:-1] + "Br))) - (" + znamel[0:-1] + "Bl + (incx * (" + znamel[0:-1] + "Cl -" + znamel[0:-1] + "Bl))));" 




print """
% pen positions 
""" 

# reading font Pen Positions

glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
#     zname = 'z'+str(i)+'r'

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
         
            print """penpos""" + znamel[1:-1] + "(dist"+znamel[1:-1] + " + (incx * (px - dist"+znamel[1:-1] + ")), ang"+znamel[1:-1] + ");"


        
# reading font Pen strokes

print """

% test new center (z) points
""" 


if g in mean :
    ggroup = 'xheight'
    
if g in des :
    ggroup = 'descender'
        
if g in cap : 
    ggroup = 'capital'

if g in cap : 
    ggroup = 'ascender'

# else :
#   ggroup = 'special'


glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
ivn = 0
stre = " ... "
strtwo = " .. "
stline = " -- "
strz = ""
zzn = []
start = []
startval = []

# create empty variable list


pointshifted= []
pointshiftedval= []

pointshiftedy = []
pointshiftedyval = []


# add iteration to string

for i in range (1,100):
  start.append("")
  startval.append(0)
  
  pointshifted.append("")
  pointshiftedval.append(0)

  pointshiftedy.append("")
  pointshiftedyval.append(0)



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
	 istart = item.attributes['start'].value   
	 istart = True
       except :
       	 istart = False


       ipn = 1   
     except : 
       inattr=inattr+1 


     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:
#         if im.value.find("start") >-1 :
#           del start[i-1]
#           start.insert(i-1,"")
         if istart == True :
           istartval = item.attributes['start'].value
           del start[i-1]
           start.insert(i-1,"start")
	   del startval[i-1]
           startval.insert(i-1,istartval)

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

nnz = 0
for zitem in zzn :
  nnz = nnz +1 


i = 0
zzn.sort()
zeile =""
zeileend =""
semi = ");"
for i in range (0,nnz-1) :
  zitem = zzn[i]
  
  zitemb = zzn[i+1]
  zitemc = zzn[i-1]

## default string

  zeile =""
  zeile = "z"+str(zitem)+ "=(x2"+ str(zitem)+ "0 *width *width_" + g + "+ (incx * (x2"+str(zitem)+"A - x2" +str(zitem)+"0)), y2"+str(zitem)+ "0 *" + ggroup + " + (incx * (y2"+str(zitem)+ "A - y2" +str(zitem)+ "0))"
  
  zeileend =""
  zeileend = 'z'+str(zzn[nnz-1])+ "=(x2"+ str(zzn[nnz-1])+ "0 *width *width_" + g + " + (incx * (x2"+str(zzn[nnz-1])+"A - x2" +str(zzn[nnz-1])+"0)), y2"+str(zzn[nnz-1])+ "0 *" + ggroup + " + (incx * (y2"+str(zzn[nnz-1]) + "A - y2" +str(zzn[nnz-1])+ "0))"
 

# parameters 

  if pointshifted[i] <> "" :
    zeile = zeile +") shifted (" + str(pointshiftedval[i]) + ",0"      

  if pointshiftedy[i] <> "" :
    zeile = zeile +") shifted (0," + str(pointshiftedyval[i])+");"       

  else: 
    zeile = zeile + semi 
  print zeile

zeile = zeileend + semi
print zeile
 



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

start = []
startval = []

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

left = []
leftvalB = []

right = []
rightvalB = []

up = []
upvalB = []

down = []
downvalB = []

penshiftedy = []
penshiftedyvalB = []

penshifted = []
penshiftedvalB = []

for i in range (1,100):

  start.append("")
  startval.append(0)

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

  left.append("")
  leftvalB.append(0)

  right.append("")
  rightvalB.append(0)

  up.append("")
  upvalB.append(0)

  down.append("")
  downvalB.append(0)
  
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
	 ileft = item.attributes['left'].value   
	 ileft = True
       except :
       	 ileft = False

       try :
	 iup = item.attributes['up'].value   
	 iup = True
       except :
       	 iup = False

       try :
	 iright = item.attributes['right'].value   
	 iright = True
       except :
       	 iright = False

       try :
	 idown = item.attributes['down'].value   
	 idown = True
       except :
       	 idown = False

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
#         if im.value.find("start") >-1 :
#           del zzstart[i-1]
#           zzstart.insert(i-1,"penstroke ")
             
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
      
         if iup == True :
           iupval = item.attributes['up'].value
           del up[i-1]
           up.insert(i-1,"up")
	   del upvalB[i-1]
           upvalB.insert(i-1,iupval)

         if ileft == True :
           ileftval = item.attributes['left'].value
           del left[i-1]
           left.insert(i-1,"left")
	   del leftvalB[i-1]
           leftvalB.insert(i-1,ileftval)

         if iright == True :
           irightval = item.attributes['right'].value
           del right[i-1]
           right.insert(i-1,"right")
	   del rightvalB[i-1]
           rightvalB.insert(i-1,irightval)

         if idown == True :
           idownval = item.attributes['down'].value
           del down[i-1]
           down.insert(i-1,"down")
	   del downvalB[i-1]
           downvalB.insert(i-1,idownval)
                  
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
% pen strokes  """




           
# reading font Pen strokes


glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
ivn = 0
stre = " ... "
strtwo = " .. "
stline = " -- "
strz = ""
zzn = []
start = []
startval = []

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

left = []
leftval = []

right = []
rightval = []

up = []
upval = []

down = []
downval = []

dir2 = []
dir2val = []

left2 = []
left2val = []

right2 = []
right2val = []

up2 = []
up2val = []

down2= []
down2val = []

penshiftedy = []
penshiftedyval = []

penshifted = []
penshiftedval = []

overx = []
overxval = []

overbase = []
overbaseval = []

cycle = []
cycleval = []

for i in range (1,100):

  start.append("")
  startval.append(0)

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

  left.append("")
  leftval.append(0)

  right.append("")
  rightval.append(0)

  up.append("")
  upval.append(0)

  down.append("")
  downval.append(0)

  dir2.append("")
  dir2val.append(0)

  left2.append("")
  left2val.append(0)

  right2.append("")
  right2val.append(0)

  up2.append("")
  up2val.append(0)
  
  down2.append("")
  down2val.append(0)

  penshiftedy.append("")
  penshiftedyval.append(0)

  penshifted.append("")
  penshiftedval.append(0)

  overx.append("")
  overxval.append(0)

  overbase.append("")
  overbaseval.append(0)

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
	 istart = item.attributes['start'].value   
	 istart = True
       except :
       	 istart = False

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
	 ileft = item.attributes['left'].value   
	 ileft = True
       except :
       	 ileft = False

       try :
	 ileft2 = item.attributes['left2'].value   
	 ileft2 = True
       except :
       	 ileft2 = False

       try :
	 iup = item.attributes['up'].value   
	 iup = True
       except :
       	 iup = False

       try :
	 iup2 = item.attributes['up2'].value   
	 iup2 = True
       except :
       	 iup2 = False

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
	 idown = item.attributes['down'].value   
	 idown = True
       except :
       	 idown = False

       try :
	 idown2= item.attributes['down2'].value   
	 idown2= True
       except :
       	 idown2= False


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
        
#	 if im.value.find("start") >-1 :
#           del zzstart[i-1]
#           zzstart.insert(i-1,"penstroke ")

         if istart == True :
           istartval = item.attributes['start'].value
           del start[i-1]
           start.insert(i-1,"penstroke ")
	   del startval[i-1]
           startval.insert(i-1,istartval)
  
         if icycle == True :
           icycleval = item.attributes['cycle'].value
           del start[i-1]
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
      
         if iup == True :
           iupval = item.attributes['up'].value
           del up[i-1]
           up.insert(i-1,"{up} ")
	   del upval[i-1]
           upval.insert(i-1,iupval)

         if ileft == True :
           ileftval = item.attributes['left'].value
           del left[i-1]
           left.insert(i-1,"{left} ")
	   del leftval[i-1]
           leftval.insert(i-1,ileftval)

         if iright == True :
           irightval = item.attributes['right'].value
           del right[i-1]
           right.insert(i-1,"{right} ")
	   del rightval[i-1]
           rightval.insert(i-1,irightval)

         if idown == True :
           idownval = item.attributes['down'].value
           del down[i-1]
           down.insert(i-1," {down} ")
	   del downval[i-1]
           downval.insert(i-1,idownval)

         if idown2 == True :
           idown2val = item.attributes['down2'].value
           del down2[i-1]
           down2.insert(i-1," {down} ")
	   del down2val[i-1]
           down2val.insert(i-1,idown2val)

         if iup2 == True :
           iup2val = item.attributes['up2'].value
           del up2[i-1]
           up2.insert(i-1,"{up} ")
	   del up2val[i-1]
           up2val.insert(i-1,iup2val)

         if ileft2 == True :
           ileft2val = item.attributes['left2'].value
           del left2[i-1]
           left2.insert(i-1,"{left} ")
	   del left2val[i-1]
           left2val.insert(i-1,ileft2val)

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


nnz = 0
for zitem in zzn :
  nnz = nnz +1 


i = 0
zzn.sort()
zeile =""
semi = ";"
for i in range (0,nnz-1) :
  zitem = zzn[i]
  zitemsuper = zzn[i+1]  
  zitemc = zzn[i-1]

## default string

  zeile =""
  zeile =  str(start[i]) +  "z"+str(zitem)+"e"  + left[i] +right[i] +up[i] +down[i] 
  zeileb =""
  zeileb = str(start[i])
  zeilec = ""
  zeilec = str(start[i]) + "z"+str(zitem)+"e" 
  if start[i+1]=="" : 

# if start, add parameters

    if dir[i] <> "" :
      zeile = zeile + " {dir "+ str(dirval[i]) + "}"      

    if penshifted[i] <> "" :
      zeile = zeile + " shifted (" + str(penshiftedval[i]) + ")"      

    if penshiftedy[i] <> "" :
      zeile = zeile + " shifted (0, y" + str(penshiftedyval[i]) + ")"      

    if overx[i] <> "" :
      zeile = zeile + " shifted (0, mean-y" + str(overxval[i]) + ") + (0, over)" 
   
    if overbase[i] <> "" :
      zeile = zeile + " shifted (0, baseline-y" + str(overbaseval[i]) + ") + (0, -over)" 

    if doubledash[i] <> "" :
      zeile = zeile + doubledash[i]    

    if tripledash[i] <> "" :
      zeile = zeile + tripledash[i]    

    if superleft[i] <> "" :
      zeile = zeile + strtwo + superleft[i]+"("+str(zitem)+"e," +str(zitemsuper)+"e, ["+str(superleftval[i]) + '+ (incx * (' + str(superleftvalB[i])+ '-' +str(superleftval[i]) + '))])' + strtwo      

    if superright[i] <> "" :
      zeile = zeile + strtwo + superright[i]+"("+str(zitem)+"e," +str(zitemsuper)+"e, ["+str(superrightval[i]) + '+ (incx * (' + str(superrightvalB[i])+ '-' +str(superrightval[i]) + '))])' + strtwo      
      
    if tensionand[i] <> "" :
      zeile = zeile + strtwo + "tension" + " ((" + str(tensionandval[i]) + '/100) + (incx * ((' + str(tensionandvalB[i]) + '/100) - (' + str(tensionandval[i]) + '/100))))' + " and ((" + str(tensionandval2[i]) + '/100) + (incx * ((' + str(tensionandval2B[i]) + '/100) - (' + str(tensionandval2[i]) + '/100))))' + strtwo

    if tension[i] <> "" :
      zeile = zeile + strtwo + "tension" + " ((" + tensionval[i] + '/100) + (incx * ((' + tensionvalB[i] + '/100) - (' + tensionval[i] + '/100))))' + strtwo 


 
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
              if overx[i] > "" :
                zeile = zeile 
              else :
                if overbase[i] > "" :
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
                        if tensionand[i] > "" :
                         zeile = zeile 

                        else :
                           zeile = zeile + stre  

    if down2[i] <> "" :
      zeile = zeile  + down2[i]  
    if up2[i] <> "" :
      zeile = zeile  + up2[i]  
    if left2[i] <> "" :
      zeile = zeile + left2[i]  
    if right2[i] <> "" :
      zeile = zeile + right2[i]  
    if dir2[i] <> "" :
      zeile = zeile + " {dir "+ str(dir2val[i]) + "}"      


   
      
# parameters before a new penpos    extra semi after else

  else: 
   
    if penshifted[i] <> "" :
      zeile = zeile + " shifted (" + str(penshiftedval[i]) + ")"       

    if penshiftedy[i] <> "" :
      zeile = zeile + " shifted (0, y" + str(penshiftedyval[i]) + ")"      

    if overx[i] <> "" :
      zeile = zeile + " shifted (0, mean-y" + str(overxval[i]) + ") + (0, over)" 
   
    if overbase[i] <> "" :
      zeile = zeile + " shifted (0, baseline-y" + str(overbaseval[i]) + ") + (0, -over)" 

    if doubledash[i] <> "" :
      zeile = zeile + doubledash[i]    

    if cycle[i] <> "" :
      zeile = zeile + " ... cycle" + semi
 
    else : 
      if tension[i] <> "" :
        zeile = zeile + strtwo + "tension" + " (" + tensionval[i] + ' + (incx * (' + tensionvalB[i] + '-' + tensionval[i] + ')))' + strtwo  + down2[i] + semi
      
    if tensionand[i] <> "" :
      zeile = zeile + strtwo + "tension" + " ((" + str(tensionandval[i]) + '/100) + (incx * ((' + str(tensionandvalB[i]) + '/100) - (' + str(tensionandval[i]) + '/100))))' + " and ((" + str(tensionandval2[i]) + '/100) + (incx * ((' + str(tensionandval2B[i]) + '/100) - (' + str(tensionandval2[i]) + '/100))))' + strtwo   + semi



      if down2[i] <> "" :
        zeile = zeile + stre + down2[i]  + semi
      if up2[i] <> "" :
        zeile = zeile + stre + up2[i]  + semi
      if left2[i] <> "" :
        zeile = zeile + stre + left2[i]  + semi
      if right2[i] <> "" :
        zeile = zeile + stre + right2[i]  + semi
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
                if overx[i] > "" :
                  zeile = zeile 
                else :
                  if overbase[i] > "" :
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
                           zeile = zeile + semi + "seckel" 

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

if overx[i+1] <> "" :
 zeile = zeile + " shifted (0, mean-y" + str(overxval[i+1]) + ") + (0, over)" 
   
if overbase[i+1] <> "" :
 zeile = zeile + " shifted (0, baseline-y" + str(overbaseval[i+1]) + ") + (0, -over)" 

if cycle[i+1] <> "" :
 zeile = zeile + " ... cycle" 

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
