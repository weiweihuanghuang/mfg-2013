import web, datetime,mfg
from xml.dom import minidom
import codecs

#db = web.database(dbn='mysql', db='blog', user='root', pw='schnaegg' )
db = web.database(dbn='mysql', db='blog', user='walter', pw='' )

def delFont(fontName,glyphNamel):

  return None

def putFont():
  print mfg.cFont.glyphName
  global glyphsource
  global glyphnameNew
  global glyphName
  glyphName = mfg.cFont.glyphName 
  glyphsource = mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
  glyphnameNew = glyphName+".glif"
  print glyphnameNew
  global xmldoc
  global itemlist
  try :
     xmldoc = minidom.parse(glyphsource)
  except :
     print "not meier"
     return None

  itemlist = xmldoc.getElementsByTagName('point')
  advance = xmldoc.getElementsByTagName('advance')
  db.delete('glyphoutline', where='Glyphname="'+glyphName+'"')  
  db.delete('glyphparam', where='Glyphname="'+glyphName+'"')  

  if not  list(db.select('glyphoutline', where='GlyphName="'+glyphName+'"')) :  # check if list is empty
#  put data into db
     inum=0
     strg=""
     for s in itemlist :
        inum = inum+1
#  find a named point , convention the name begin with the letter z
        try :
            im = s.attributes['name'] 
            iposa = im.value.find("z")
            ipose = im.value.find(",",iposa)
            if ipose > iposa :
               nameval = im.value[iposa:ipose]
            else :
               if ipose == -1 :
                 ipose=len(im.value) 
                 nameval = im.value[iposa:ipose]
#  find the start value
#            print "findstart",inum, im.value.find('start')
            if im.value.find('start') > -1 :
               startp = 1
            else:
               startp = 0
#  find superness , cardinal and all parameter 
#
            db.insert('glyphparam', id=inum,GlyphName=glyphName, PointName=nameval, startp=startp)
            if im.value.find("superness") > 0:
              iposa=im.value.find("superness") 
              ipose= im.value.find(",",iposa)
              if ipose > iposa :
                superness = int(im.value[iposa+9:ipose])
              else :
                ipose = len(im.value)
                superness = int(im.value[iposa+9:ipose])
              db.update('glyphparam', where='id=$inum and GlyphName="'+glyphName+'"', vars=locals(), superness=superness)
    #        cardinal = 0
        except :
           nameval = ""
           startp = 0

        s.attributes['pointNo']= "p" + str(inum)    # adding a new attribute

        try :
          if s.attributes['type'] >-1 :
            mainpoint = 1
          else :
            mainpoint = 1 
        except :
            mainpoint = 0 
	s.toxml()
        strg= "insert into glyphoutline (GlyphName,PointNr,x,y,contrp,id) Values ("+'"'+glyphName+'"'+","+'"'+s.attributes['pointNo'].value+'"' + ","+ str(s.attributes['x'].value)+ "," + str(s.attributes['y'].value)+","+str(mainpoint)+","+str(inum)+")"
        print strg
        db.query(strg)
  return None  

def get_posts():
    glyphName = mfg.cFont.glyphName 
    return db.query("SELECT IFNULL(PointName, '') PointNr,x,y,concat('position:absolute;left:',0+x,'px;top:',0-y,'px; ',IF (PointName > '', 'color:red;', IF (contrp > 0 , 'z-index:-1;color:blue;', 'z-index:-2;color:CCFFFF;')) ) position, id from vglyphoutline where GlyphName="+'"'+glyphName+'"')

def get_post(id):
    glyphName = mfg.cFont.glyphName 
    try:
        return db.select('vglyphoutline', where='id=$id and glyphName='+'"'+glyphName+'"', vars=locals())[0]
    except IndexError:
        return None

def get_glyphparam(id):
    glyphName = mfg.cFont.glyphName 
    try:
        return db.select('glyphparam', where='id=$id and GlyphName='+'"'+glyphName+'"', vars=locals())[0]
    except IndexError:
        return None


def update_post(id, x, y):
    glyphName = mfg.cFont.glyphName 
    db.update('glyphoutline', where='id=$id and GlyphName="'+glyphName+'"', vars=locals(),
        x=x, y=y)

def update_glyphparam(id, a, b, c):
    glyphName = mfg.cFont.glyphName 
    bb = b
    if c != '' :
      cc = c
    else:
      cc = None
    db.update('glyphparam', where='id=$id and GlyphName="'+glyphName+'"', vars=locals(),
        pointName=a, startp=bb, superness=cc)

def insert_glyphparam(id, a, b, c):
    
    glyphName = mfg.cFont.glyphName 
    db.insert('glyphparam', id=id,GlyphName=glyphName, PointName=a, startp=b, superness=c)

def get_masters():
    return db.select('master',  vars=locals())

def get_master():

    id=mfg.cFont.idmaster
    return db.select('master',  where='idmaster=$id', vars=locals())

def put_master():

    fontName=mfg.cFont.fontname
    fontNameA=mfg.cFont.fontna
    fontNameB=mfg.cFont.fontnb
    idglobal =mfg.cFont.idglobal
    t=db.transaction()
    
    try:
       db.insert('master', FontName="'"+fontName+"'", FontNameA="'"+fontNameA+"'", FontNameB="'"+fontNameB+"'", idglobal="'"+idglobal+"'")
    except:
       t.rollback()
       raise
    else:
       t.commit()

    return None    

def get_globalparams():
    return db.select('globalparam', vars=locals())

def get_globalparam():

    id=mfg.cFont.idglobal
    return db.select('globalparam', where='idglobal=$id',vars=locals())

def put_globalparam(id):

    superness=mfg.cFont.superness
    Interpolation=mfg.cFont.Interpolation
    penwidth=mfg.cFont.penwidth
    unitwidth=mfg.cFont.unitwidth
    xHeight=mfg.cFont.xHeight
    db.insert('globalparam', where='idglobal = $id',vars=locals(), 
        superness=superness, Interpolation=Interpolation, penwidth=penwidth, unitwidth=unitwidth, xHeigth=xHeigth)
    return None

def update_master(id, a, b, c, d):
    db.update('master', where='idmaster = $id', vars=locals(), 
      FontName = a, FontNameA = b, FontNameB = c, idglobal = d)
    return None

def update_globalparam(id, a, b, c, d, e):
    db.update('globalparam', where='idglobal = $id', vars=locals(), 
      superness = a, Interpolation = b, penwidth = c, unitwidth = d, xHeight = e)
    return None

def writexml():
     glyphName = mfg.cFont.glyphName 
     glyphsource = mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
     inum = 0
#     db_rows=list(db.query("SELECT PointName,x,y from glyphoutline"))
#    we assume the number of rows from the db >= the number of the itemlist 
     for  s in itemlist:
             inum = inum + 1
             qstr = "SELECT PointNr,x,y,PointName from vglyphoutline where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'
            
             try :
                 db_rows=list(db.query(qstr))
                 s.attributes['pointNo'] = str(db_rows[0].PointNr)
                 s.attributes['x'] = str(db_rows[0].x)
                 s.attributes['y'] = str(db_rows[0].y)
                 sname = str(db_rows[0].PointName)
                 if sname <> "None" : 
                   qstrp = "SELECT * from glyphparam where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'
                   db_rowparam = list(db.query(qstrp))
                   nameattr = sname

		   if str(db_rowparam[0].startp) > '0':
		     nameattr = nameattr + ', start '
                   
                   print " superness ",db_rowparam[0].superness 
		   if str(db_rowparam[0].superness) != 'None':
		     nameattr = nameattr + ',superness'+str(db_rowparam[0].superness)
                    
                   s.attributes['name'] = nameattr 

                 s.toxml()
             except :
                 print " db and script not consisten"
     print "glyphsource", glyphsource
     with codecs.open(glyphsource, "w", "utf-8") as out:
          xmldoc.writexml(out) 

def writeGlobalParam():
# prepare font.mf parameter file
#
  master = list(get_master()) 
  fontsize=12
  incx=0
  u = 1
  superness = master[0].superness 
  print "superness ",superness
  px=0.1
  mean=6.12
  des=2.45
  asc=0.8
  cap=0.8
  ifile=open("font.mf","w")
  ifile.write("% parameter file \n")
  ifile.write("incx:=%.0f;\n"%incx)
  ifile.write("font_size:=%.0fpt#;\n"%fontsize)
  ifile.write("ht#:=10pt#;\n")
  ifile.write("u#:=%.0fpt#;\n"%u)
  ifile.write("px#:=%.1fpt#;\n"%px)
  ifile.write("superness:=%.1f;\n"%superness)
  ifile.write("mean#:=%.2fpt#;\n"%mean)
  ifile.write("des#:=%.2fht#;\n"%des)
  ifile.write("asc#:=%.2fht#;\n"%asc)
  ifile.write("cap#:=%.2fht#;\n"%cap)
  ifile.write("\n") 
  ifile.write("input glyphs\n") 
  ifile.write("bye\n") 
  ifile.close()
  return None 
