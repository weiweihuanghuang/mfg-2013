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

mean = ['a', 'c', 'e', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'x', 'z']
des = ['g', 'j', 'p', 'q', 'y']
cap = [ 'f', 'A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

if g in mean :
    ggroup = 'mean#'
    
if g in des :
    ggroup = 'des#'
        
if g in cap : 
    ggroup = 'cap#'

print 'beginfontchar("' + g + '", ' + w + " + (incx * (" + w2 + '-' + w + ")), " + ggroup + ", 0);"


print """

% einbauen : mean# aus Tabelle mit buchstaben gruppierungen link,;
% tabelle mit gruppierung: <glyph name="p" = mean# 
% tabelle mit gruppierung: <glyph name="A" = cap# 

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




# dist = sqrt((y100l-y100r)*(y100l-y100r)+(x100r-x100l)*(x100r-x100l));

# px10l=x100l; py10l=y100l;
# px10r=x100r; py10r=y100r;



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

#         ang = x100l - y100r;



# reading pen angle Font B

# glif = minidom.parse(font_a)
# itemlist = glif.getElementsByTagName('point') 

# print """
# % pen angle Font B
# """ 

# inattr=0   
# for item in itemlist :
#   for i in range (1,100):
#      znamel = 'z'+str(i)+'l'
#      znamer = 'z'+str(i)+'r'
#      zname = 'z'+str(i)+'r'
# 
#     ipn=0
#     try :
#       x = item.attributes['x'].value
#       y = item.attributes['y'].value
#       im =item.attributes['name'] 
#       ipn = 1   
#     except : 
#       inattr=inattr+1 
#
#    
#     if ipn == 1 :
#       if im.value.find(znamer)>-1 or im.value.find(znamel)>-1: 
#         if im.value.find(znamer)>-1 :
#         
#                print "ang"+ znamel[1:-1] + "B := angle(" + znamel[0:-1] + "Cr" + " - " + znamel[0:-1] + "Cl);"



# reading transformation


glif = minidom.parse(font_a)
itemlist = glif.getElementsByTagName('point') 

print """
% center points and transformation
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

                print znamel[0:-1] + "=(x2"+znamel[1:-1] + "0 + (incx * (x2"+znamel[1:-1]+"A - x2" + znamel[1:-1]+"0)), y2"+znamel[1:-1] + "0 + (incx * (y2"+znamel[1:-1] + "A - y2" + znamel[1:-1] + "0)));"


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
         
# mono      print """penpos""" + znamel[1:-1] + "(dist"+znamel[1:-1] + " + (incx * (px - dist"+znamel[1:-1] + ")), ang"+znamel[1:-1] + ");"
            print """penpos""" + znamel[1:-1] + "(dist"+znamel[1:-1] + " + (incx * (dist"+znamel[1:-1] + "B - dist"+znamel[1:-1] + ")), ang"+znamel[1:-1] + ");"      # stereo


print """
% pen strokes  """

# reading values functions font B


glif = minidom.parse(font_b)
itemlist = glif.getElementsByTagName('point') 

inattr=0   
ivn = 0
zzn = []

zztens = []
zztensval_b =[]

zzdir = []
zzdirval_b =[]

zzsuper_qr = []
zzsuper_qrval_b = []

zzsuper_ql = []
zzsuper_qlval_b = []


for i in range (1,100):

  zztens.append("")
  zztensval_b.append(0)
  
  zzdir.append("")
  zzdirval_b.append(0)

  zzsuper_qr.append("")
  zzsuper_qrval_b.append(0)  



  zzsuper_ql.append("")
  zzsuper_qlval_b.append(0)  
      

      
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'    

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 

     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:
         
           
         if im.value.find("tension") >-1 :
           iposa = im.value.find("tension")
           iposk = im.value.find(",")
           itens = int(im.value[iposa+7:iposk])
           del zztens[i-1]
           zztens.insert(i-1,"tension")
           del zztensval_b[i-1]
           zztensval_b.insert(i-1,itens)

         if im.value.find("dir") >-1 :
           iposaa = im.value.find("dir")
           iposkk = im.value.find(",")
           itenss = int(im.value[iposaa+3:iposkk])
           del zzdir[i-1]
           zzdir.insert(i-1,"dir")
           del zzdirval_b[i-1]
           zzdirval_b.insert(i-1,itenss)           

         if im.value.find("super_ql") >-1 :
           iposaaaa = im.value.find("super_ql")
           iposkkkk = im.value.find(",")
           itenssss = int(im.value[iposaaaa+8:iposkkkk])
           del zzsuper_ql[i-1]
           zzsuper_ql.insert(i-1,"super_ql")
           del zzsuper_qlval_b[i-1]
           zzsuper_qlval_b.insert(i-1,itenssss)
           
         if im.value.find("super_qr") >-1 :
           iposaaa = im.value.find("super_qr")
           iposkkk = im.value.find(",")
           itensss = int(im.value[iposaaa+8:iposkkk])
           del zzsuper_qr[i-1]
           zzsuper_qr.insert(i-1,"super_qr")
           del zzsuper_qrval_b[i-1]
           zzsuper_qrval_b.insert(i-1,itensss)

 

           
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
zzstart = []

zzline = []

zztens = []
zztensval = []

zzsuper_qr = []
zzsuper_qrval = []

zzsuper_ql = []
zzsuper_qlval = []

zzdir = []
zzdirval = []

zzleft = []
zzright = []
zzup = []
zzdown = []

zzcycle = []

for i in range (1,100):
  zzstart.append("")
  
  zzline.append("")

  zztens.append("")
  zztensval.append(0)
  
  zzsuper_qr.append("")
  zzsuper_qrval.append(0)
  

  zzsuper_ql.append("")
  zzsuper_qlval.append(0)
  
  zzdir.append("")
  zzdirval.append(0)
  
  zzleft.append("")
  zzright.append("")
  zzup.append("")
  zzdown.append("")
  
  zzcycle.append("")

  
for item in itemlist :
  for i in range (1,100):
     znamel = 'z'+str(i)+'l'
     znamer = 'z'+str(i)+'r'
     

     ipn=0
     try :
       x = item.attributes['x'].value
       y = item.attributes['y'].value
       im =item.attributes['name'] 
       ipn = 1   
     except : 
       inattr=inattr+1 


     if ipn == 1 :
       if im.value.find(znamel) > -1 :
          zzn.append (i)
       if im.value.find(znamel) > -1 or im.value.find(znamer) > -1:
         if im.value.find("start") >-1 :
           del zzstart[i-1]
           zzstart.insert(i-1,"penstroke ")
           
         if im.value.find("line") >-1 :
           del zzline [i-1]
           zzline.insert(i-1," -- ")            
           
      
         if im.value.find("left") >-1 :
           del zzleft[i-1]
           zzup.insert(i-1,"{left}")            
           
         if im.value.find("right") >-1 :
           del zzright[i-1]
           zzup.insert(i-1,"{right}")   
           
         if im.value.find("up") >-1 :
           del zzup[i-1]
           zzup.insert(i-1,"{up}")
           
         if im.value.find("down") >-1 :
           del zzdown[i-1]
           zzdown.insert(i-1,"{down}")

         if im.value.find("cycle") >-1 :
           del zzdown[i-1]
           zzdown.insert(i-1," cycle")
                      
         if im.value.find("tension") >-1 :
           iposa = im.value.find("tension")
           iposk = im.value.find(",")
           itens = int(im.value[iposa+7:iposk])
           del zztens[i-1]
           zztens.insert(i-1,"tension")
           del zztensval[i-1]
           zztensval.insert(i-1,itens)

         if im.value.find("super_qr") >-1 :
           iposaaa = im.value.find("super_qr")
           iposkkk = im.value.find(",")
           itensss = int(im.value[iposaaa+8:iposkkk])
           del zzsuper_qr[i-1]
           zzsuper_qr.insert(i-1,"super_qr")
           del zzsuper_qrval[i-1]
           zzsuper_qrval.insert(i-1,itensss)
           
 
         if im.value.find("super_ql") >-1 :
           iposo = im.value.find("super_ql")
           iposy = im.value.find(",")
           itene = int(im.value[iposo+8:iposy])
           del zzsuper_ql[i-1]
           zzsuper_ql.insert(i-1,"super_ql")
           del zzsuper_qlval[i-1]
           zzsuper_qlval.insert(i-1,itene)

         if im.value.find("dir") >-1 :
           iposaa = im.value.find("dir")
           iposkk = im.value.find(",")
           itenss = int(im.value[iposaa+3:iposkk])
           del zzdir[i-1]
           zzdir.insert(i-1,"dir")
           del zzdirval[i-1]
           zzdirval.insert(i-1,itenss)

nnz = 0
for zitem in zzn :
  nnz = nnz +1 


i = 0
zzn.sort()
zeile =""
semi = ";"
for i in range (0,nnz-1) :
  zitem = zzn[i]
  
  zitemb = zzn[i+1]
  zitemc = zzn[i-1]

  zeile =""
  zeile = str(zzstart[i])+ " z"+str(zitem)+"e"+zzleft[i] +zzright[i] +zzdown[i] +zzcycle[i]  ### confused with s up erness    +zzup[i] 
  zeileb =""
  zeileb = str(zzstart[i])
  if zzstart[i+1]=="" : 
    if zztens[i] <> "" :
      zeile = zeile + strtwo+""+zztens[i]+" ("+str(zztensval[i]/10.0) + '+ (incx * (' + str(zztensval_b[i]/10.0)+ '-' +str(zztensval[i]/10.0) + ')))'   

    if zzsuper_ql[i] <> "" :
      zeile = zeileb + zzsuper_ql[i]+ "("+str(zitem)+"e," +str(zitemb)+"e, ["+str(zzsuper_qlval[i]/1000.0) + '+ (incx * (' + str(zzsuper_qlval_b[i]/1000.0)+ '-' +str(zzsuper_qlval[i]/1000.0) + '))])' 
   
    if zzsuper_qr[i] <> "" :
      zeile = zeileb + zzsuper_qr[i]+ "("+str(zitem)+"e," +str(zitemb)+"e, ["+str(zzsuper_qrval[i]/1000.0) + '+ (incx * (' + str(zzsuper_qrval_b[i]/1000.0)+ '-' +str(zzsuper_qrval[i]/1000.0) + '))])' 


    if zzdir[i] <> "" :
      zeile = zeile +"{"+zzdir[i]+" ("+str(zzdirval[i]) + ' + (incx * (' + str(zzdirval_b[i])+ '-' +str(zzdirval[i]) + ')))}'  
    
    if zzline[i] <> "" :
      zeile = zeile + stline    
    else : 
      if zztens[i] <> "" :
        zeile = zeile + strtwo 
      else :
        zeile = zeile + stre      
        
    if zzcycle[i] <> "" :
      zeile = zeile + stre    
   
  else: 
    zeile = zeile + semi 
  print zeile

zeile = 'z'+str(zzn[nnz-1])+ "e" 
print zeile +semi 
 
print """

% pen labels
penlabels(range 1 thru 99);
endchar;
"""
