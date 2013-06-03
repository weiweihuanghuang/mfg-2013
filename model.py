import web, datetime,mfg
from xml.dom import minidom
import codecs

glyphsource = "test.ufo/glyphs/n.glif"
xmldoc = minidom.parse(glyphsource)
itemlist = xmldoc.getElementsByTagName('point')
advance = xmldoc.getElementsByTagName('advance')
db = web.database(dbn='mysql', db='blog', user='root', pw='schnaegg' )

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
            superness = 0
            print im.value.find("superness"),im,len(im.value)
            if im.value.find("superness") > 0:
              iposa=im.value.find("superness") 
              ipose= im.value.find(",")
              if ipose > iposa :
                superness = int(im.value[iposa+10:ipose])
              else :
                ipose = len(im.value)
                superness = int(im.value[iposa+10:ipose])
            print "superness", superness
            cardinal = 0
            db.insert('glyphparam', id=inum,GlyphName=glyphName, PointName=nameval, startp=startp, superness=superness, cardinal=cardinal)
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
    try:
        return db.select('vglyphoutline', where='id=$id and glyphName='+'"'+glyphName+'"', vars=locals())[0]
    except IndexError:
        return None

def get_glyphparam(id):
    try:
        return db.select('glyphparam', where='id=$id and GlyphName='+'"'+glyphName+'"', vars=locals())[0]
    except IndexError:
        return None


def update_post(id, x, y):
    db.update('glyphoutline', where='id=$id and GlyphName="'+glyphName+'"', vars=locals(),
        x=x, y=y)

def update_glyphparam(id, a, b, c, d):
    db.update('glyphparam', where='id=$id and GlyphName="'+glyphName+'"', vars=locals(),
        PointName=a, startp=b, superness=c, cardinal=d)

def insert_glyphparam(id, a, b, c, d):
    
    db.insert('glyphparam', id=id,GlyphName=glyphName, PointName=a, startp=b, superness=c, cardinal=d)

def get_master():
    return db.query("SELECT FontName,Interpolation,superness,penwidht,unitwidht,xHeight from master where idmaster=1 ")

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

def writexml():
     inum = 0
     global glyphnameNew
#     db_rows=list(db.query("SELECT PointName,x,y from glyphoutline"))
#    we assume the number of rows from the db >= the number of the itemlist 
     print "newglyphname",glyphnameNew
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
                   qstrp = "SELECT startp from glyphparam where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'
                   db_rowparam = list(db.query(qstrp))
		   if str(db_rowparam[0].startp) > '0':
		      s.attributes['name'] = sname + ', start '
                   else :
		      s.attributes['name'] = sname

               

                 s.toxml()
             except :
                 print " db and script not consisten"
#     with codecs.open("glyphs/e.glif", "w", "utf-8") as out:
     with codecs.open("oswald.ufo/glyphs/"+glyphnameNew, "w", "utf-8") as out:
          xmldoc.writexml(out) 
