import web, datetime,mfg
from xml.dom import minidom
import codecs
import os.path, time

#db = web.database(dbn='mysql', db='blog', user='root', pw='schnaegg' )
db = web.database(dbn='mysql', db='blog', user='walter', pw='' )

def delFont(fontName,glyphNamel):

  return None

def putFont():
#
#  put font A and font B into table
#
  print mfg.cFont.glyphName
  global glyphsource
  global glyphnameNew
  global glyphName
  glyphName = mfg.cFont.glyphName 
  glyphsourceA = mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
  glyphsourceB = mfg.cFont.fontnb + "/glyphs/"+glyphName+".glif"
  glyphnameNew = glyphName+".glif"
  print glyphnameNew
  print "lastmodifiedA: %s" % time.ctime(os.path.getmtime(glyphsourceA))
  print "lastmodifiedB: %s" % time.ctime(os.path.getmtime(glyphsourceB))

  global xmldocA
  global xmldocB
  global itemlistA
  global itemlistB
  try :
     xmldocA = minidom.parse(glyphsourceA)
     xmldocB = minidom.parse(glyphsourceB)
  except :
     print "not meier"
     return None

  advanceA = xmldocA.getElementsByTagName('advance')
  advanceB = xmldocB.getElementsByTagName('advance')
  
  idmasterA = int(mfg.cFont.idmaster)
  idmasterB = -idmasterA

  idsA= " and idmaster="+'"'+str(idmasterA)+'"'
  idsB= " and idmaster="+'"'+str(idmasterB)+'"'
#
#  decide when to load new entries from xml file   
#
  dbqA= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphoutline where glyphname=glyphName" +idsA))
  dbqB= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphoutline where glyphname=glyphName" +idsB))
  dbqpA= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphparam where glyphname=glyphName"+idsA))
  dbqpB= list(db.query("SELECT unix_timestamp(max(vdate)) vdate from glyphparam where glyphname=glyphName"+idsB))
# check if glyphoutline exists
  for idmaster in [idmasterA,idmasterB] :
    if idmaster == idmasterA:
      glyphsource = glyphsourceA
      dbq = dbqA
      if  dbqA[0].vdate == None :
         vdatedb = 0
         vdatedbp = 0
      else:
         vdatedb=int(dbqA[0].vdate)
         vdatedbp=int(dbqpA[0].vdate)
      ids = idsA
      itemlist = xmldocA.getElementsByTagName('point')

    if idmaster == idmasterB:
      glyphsource = glyphsourceB
      dbq = dbqB
      if  dbqB[0].vdate == None :
         vdatedb = 0
         vdatedbp = 0
      else:
         vdatedb=int(dbqB[0].vdate)
         vdatedbp=int(dbqpB[0].vdate)
      ids = idsB
      itemlist = xmldocB.getElementsByTagName('point')

    if dbq:
      print  dbq[0].vdate,vdatedb,vdatedbp, os.path.getmtime(glyphsource) 
      vdateos=int(os.path.getmtime(glyphsource))
      if ( max(vdatedb,vdatedbp) < vdateos) :
        db.delete('glyphoutline', where='Glyphname="'+glyphName+'"'+ids )  
        db.delete('glyphparam', where='Glyphname="'+glyphName+'"'+ids )  

    if not  list(db.select('glyphoutline', where='GlyphName="'+glyphName+'"'+ids )) :  # check if list is empty
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
            db.insert('glyphparam', id=inum,GlyphName=glyphName, idmaster=idmaster, PointName=nameval, startp=startp)
            if im.value.find("superness") > 0:
              iposa=im.value.find("superness") 
              ipose= im.value.find(",",iposa)
              if ipose > iposa :
                superness = int(im.value[iposa+9:ipose])
              else :
                ipose = len(im.value)
                superness = int(im.value[iposa+9:ipose])
              db.update('glyphparam', where='id=$inum and GlyphName="'+glyphName+'"' + ids, vars=locals(), superness=superness)
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
        strg= "insert into glyphoutline (GlyphName,PointNr,x,y,contrp,id,idmaster) Values ("+'"'+glyphName+'"'+","+'"'+s.attributes['pointNo'].value+'"' + ","+ str(s.attributes['x'].value)+ "," + str(s.attributes['y'].value)+","+str(mainpoint)+","+str(inum)+","+str(idmaster)+")"
        db.query(strg)

  return None  

def gidmast(idwork):
    if idwork == '0':
       idmaster = int(mfg.cFont.idmaster)
    if idwork == '1':
       idmaster = -int(mfg.cFont.idmaster)
    return(idmaster)

def get_posts():
    idmaster = gidmast(mfg.cFont.idwork)
    glyphName = mfg.cFont.glyphName 
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    q1="SELECT IFNULL(PointName, '') PointNr,x,y,concat('position:absolute;left:',0+x,'px;top:',0-y,'px; ',IF (PointName > '', 'color:red;', IF (contrp > 0 , 'z-index:-1;color:blue;', 'z-index:-2;color:CCFFFF;')) ) position, id from vglyphoutline where GlyphName="+'"'+glyphName+'"'
    return db.query(q1+ids )

def get_post(id):
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    try:
        return db.select('vglyphoutline', where='id=$id and glyphName='+'"'+glyphName+'"' +ids, vars=locals())[0]
    except IndexError:
        return None

def get_glyphparam(id):
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    try:
        return db.select('glyphparam', where='id=$id and GlyphName='+'"'+glyphName+'"'+ids, vars=locals())[0]
    except IndexError:
        return None


def update_post(id, x, y):
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    db.update('glyphoutline', where='id=$id and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        x=x, y=y)

def update_glyphparamD(id, a, b):
# string:syntax update glyphparam set leftp='1' where id=75 and Glyphname='p' and idmaster=1;
    print a,b
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    aa = a 
    if b != '' :
      bb = b 
    else:
      bb = None
    str="update glyphparam set "
  
def update_glyphparam(id, a, b, c ):
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    bb = b
    if c != '' :
      cc = c
    else:
      cc = None
    db.update('glyphparam', where='id=$id and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=a, startp=bb, superness=cc)

def insert_glyphparam(id, a, b, c):
    
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    db.insert('glyphparam', id=id,GlyphName=glyphName, PointName=a, startp=b, idmaster=idmaster, superness=c)

def get_masters():
    return db.select('master',  vars=locals())

def get_master(id):

    mfg.cFont.idmaster=id
    ssmr= db.select('master',  where='idmaster=$id', vars=locals())
    ssm=list(ssmr)
    mfg.cFont.fontname=str(ssm[0].FontName)
    mfg.cFont.fontna=str(ssm[0].FontNameA)
    mfg.cFont.fontnb=str(ssm[0].FontNameB)
 
    return ssmr


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

def get_globalparam(id):
    mfg.cFont.idglobal=id

    return db.select('globalparam', where='idglobal=$id',vars=locals())

def put_globalparam(id):

    superness=mfg.cFont.superness
    metapolation=mfg.cFont.metapolation
    penwidth=mfg.cFont.penwidth
    unitwidth=mfg.cFont.unitwidth
    xHeight=mfg.cFont.xHeight
    db.insert('globalparam', where='idglobal = $id',vars=locals(), 
        superness=superness, metapolation=metapolation, penwidth=penwidth, unitwidth=unitwidth, xHeigth=xHeigth)
    return None

def update_master(id, a, b, c, d):
    db.update('master', where='idmaster = $id', vars=locals(), 
      FontName = a, FontNameA = b, FontNameB = c, idglobal = d)
    return None

def update_globalparam(id, a, b, c, d, e):
    db.update('globalparam', where='idglobal = $id', vars=locals(), 
      superness = a, metapolation = b, penwidth = c, unitwidth = d, xHeight = e)
    return None

def writexml():
     glyphName = mfg.cFont.glyphName 
     if mfg.cFont.idwork =='0' :
        glyphsource = mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
        xmldoc = xmldocA
     if mfg.cFont.idwork =='1' :
        xmldoc = xmldocB
        glyphsource = mfg.cFont.fontnb + "/glyphs/"+glyphName+".glif"
     itemlist = xmldoc.getElementsByTagName('point')
     idmaster = gidmast(mfg.cFont.idwork)
     ids= " and idmaster="+'"'+str(idmaster)+'"'
     inum = 0
#     db_rows=list(db.query("SELECT PointName,x,y from glyphoutline"))
#    we assume the number of rows from the db >= the number of the itemlist 
     for  s in itemlist:
             inum = inum + 1
             qstr = "SELECT PointNr,x,y,PointName from vglyphoutline where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'+ids
            
             try :
                 db_rows=list(db.query(qstr))
                 s.attributes['pointNo'] = str(db_rows[0].PointNr)
                 s.attributes['x'] = str(db_rows[0].x)
                 s.attributes['y'] = str(db_rows[0].y)
                 sname = str(db_rows[0].PointName)
                 if sname <> "None" : 
                   qstrp = "SELECT * from glyphparam where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'+ids
                   db_rowparam = list(db.query(qstrp))
                   nameattr = sname
                   s.attributes['name']=nameattr
#
#      read param value and write into xml
#
		   if str(db_rowparam[0].startp) > '0':
		      s.attributes['start'] = '1'
		   if str(db_rowparam[0].leftp) > '0' :
                      s.attributes['leftp']='1'
                   if str(db_rowparam[0].smooth] > '0':
                      s.attributes['smooth']="yes"
                   if str(db_rowparam[0].superness) ! ='None':
                      s.attributes['superness']=str(db_rowparam[0].superness)  
		   if str(db_rowparam[0].rightp) > '0':
		      s.attributes['rightp'] = '1'
		   if str(db_rowparam[0].downp) > '0' :
                      s.attributes['downp']='1'
                   if str(db_rowparam[0].smooth] > '0':
                      s.attributes['upp']='1'
                   if str(db_rowparam[0].supegr) ! ='None':
                      s.attributes['supergr']=str(db_rowparam[0].supergr)  
                   if str(db_rowparam[0].superleft) ! ='None':
                      s.attributes['superleft']=str(db_rowparam[0].superleft)  
                   if str(db_rowparam[0].tension) ! ='None':
                      s.attributes['tension']=str(db_rowparam[0].tension)  
                   if str(db_rowparam[0].tensionend) ! ='None':
                      s.attributes['tensionend']=str(db_rowparam[0].tensionend)  
                   if str(db_rowparam[0].cycle) ! ='None':
                      s.attributes['cycle']=str(db_rowparam[0].cycle)  
                   if str(db_rowparam[0].penwidth) ! ='None':
                      s.attributes['penwidth']=str(db_rowparam[0].penwidth) 
                   if str(db_rowparam[0].xHeight) ! ='None':
                      s.attributes['xHeight']=str(db_rowparam[0].xHeight)  
                   if str(db_rowparam[0].penshiftedx) ! ='None':
                      s.attributes['penshiftedx']=str(db_rowparam[0].penshiftedx)  
                   if str(db_rowparam[0].penshiftedy) ! ='None':
                      s.attributes['penshiftedy']=str(db_rowparam[0].penshiftedy)  
                   if str(db_rowparam[0].penshiftx) ! ='None':
                      s.attributes['penshiftx']=str(db_rowparam[0].penshiftx)  
                   if str(db_rowparam[0].penshifty) ! ='None':
                      s.attributes['penshifty']=str(db_rowparam[0].penshifty)  
                   if str(db_rowparam[0].cardinal) ! ='None':
                      s.attributes['cardinal']=str(db_rowparam[0].cardinal) 

                 s.toxml()
             except :
                 print " db and script not consisten"
     print "glyphsource", glyphsource
     with codecs.open(glyphsource, "w", "utf-8") as out:
          xmldoc.writexml(out) 

def writeGlobalParam():
# prepare font.mf parameter file
#
  
  master = list(get_master(mfg.cFont.idmaster)) 
  imgl = list(get_globalparam(mfg.cFont.idglobal))
  fontsize=12
  incx=0
  u = 1
  superness = imgl[0].superness
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
