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
            ipose = im.value.find(",")
            if ipose > -1:
               nameval = im.value[iposa:ipose]
            else :
               nameval = im.value
            print "inum nameval",inum,nameval          
#  find the start value
#            print "findstart",inum, im.value.find('start')
            if im.value.find('start') > 0 :
               startp = 1
            else:
               startp = 0
#  find superness , cardinal and all parameter 
#
            db.insert('glyphparam', id=inum,GlyphName=glyphName, PointName=nameval, startp=startp)
            if im.value.find("superness") > 0:
              iposa=im.value.find("superness") 
              ipose= im.value.find(",")
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

def get_master():
    return db.query("SELECT FontName,superness,Interpolation,penwidth,unitwidth,xHeight from master where idmaster=1 ")

def put_master():
    t=db.transaction()
    print "put_master",fontName
    try:
       db.insert('master', FontName="'"+fontName+"'")
#,Interpolation='fff',superness='fff',penwidth='a',unitwidth='b',xHeight='c')
    except:
       t.rollback()
       raise
    else:
       t.commit()

    return None    

def update_master(id, a, b, c, d, e):
#    print 'update_master',id,a,b,c,d,e    
    db.update('master', where='idmaster = $id', vars=locals(), 
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
