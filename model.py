import web, datetime,mfg
from xml.dom import minidom
import codecs
import os.path, time

db = web.database(dbn='mysql', db='blog', user='root', pw='' )
#db = web.database(dbn='mysql', db='blog', user='walter', pw='' )

def xxmlat(s, dbob, sattr, val):

   print "dbob",dbob,"atttt",sattr," vvvv",val
   if str(dbob) != 'None' :
      if not s.hasAttribute(sattr) :
          s.setAttribute(sattr,"")

      if val == '' :
          s.attributes[sattr] = str(dbob)
      else : 
          s.attributes[sattr] = val
         
   else :
      if s.hasAttribute(sattr) :
          s.removeAttribute(sattr)

def xxmrlat( inum, s, db, sattr ):
             
   if s.hasAttribute(sattr) :
       val = s.getAttribute(sattr)
       update_glyphparamD( inum, sattr, val)

def delFont(fontName,glyphNamel):

  return None

def putFont():
#
#  put font A and font B into table
#
  mfg.cFont.fontpath="fonts/"+str(mfg.cFont.idmaster)+"/"
  
  print mfg.cFont.glyphName
  global glyphsource
  global glyphnameNew
  global glyphName
  glyphName = mfg.cFont.glyphName 
  glyphsourceA = mfg.cFont.fontpath+mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
  glyphsourceB = mfg.cFont.fontpath+mfg.cFont.fontnb + "/glyphs/"+glyphName+".glif"
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
         if dbqpB[0].vdate == None :
            vdatedbp = 0
         else:
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
        if s.hasAttribute('name'): 
            im = s.attributes['name'] 
            iposa = im.value.find("z")
            ipose = im.value.find(",",iposa)
            if ipose > iposa :
               nameval = im.value[iposa:ipose]
            else :
               if ipose == -1 :
                 ipose=len(im.value) 
                 nameval = im.value[iposa:ipose]
            db.insert('glyphparam', id=inum,GlyphName=glyphName, idmaster=idmaster, PointName=nameval)

#  find  all parameter and save it in db

            xxmrlat(inum,s,db, 'startp' )
            xxmrlat(inum,s,db, 'superness' )
            xxmrlat(inum,s,db, 'startp')
            xxmrlat(inum,s,db, 'leftp')
            xxmrlat(inum,s,db, 'superness')
            xxmrlat(inum,s,db, 'rightp')
            xxmrlat(inum,s,db, 'downp')
            xxmrlat(inum,s,db, 'upp')
            xxmrlat(inum,s,db, 'superqr')
            xxmrlat(inum,s,db, 'superleft')
            xxmrlat(inum,s,db, 'tension')
            xxmrlat(inum,s,db, 'tensionend')
            xxmrlat(inum,s,db, 'cycle')
            xxmrlat(inum,s,db, 'penshiftedx')
            xxmrlat(inum,s,db, 'penshiftedy')
            xxmrlat(inum,s,db, 'pointshiftx')
            xxmrlat(inum,s,db, 'pointshifty')
            xxmrlat(inum,s,db, 'penwidth')
            xxmrlat(inum,s,db, 'xHeight')
            xxmrlat(inum,s,db, 'cardinal')

        else :
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
    return list(db.query(q1+ids ))

def get_postspa():
    idmaster = gidmast(mfg.cFont.idwork)
    glyphName = mfg.cFont.glyphName 
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    dbstr=db.select('vglyphoutlines', where='glyphName='+'"'+glyphName+'"' +ids, vars=locals())     
    return list(dbstr)


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
      bb = 'NULL' 
    strg="update glyphparam set "+aa+"="+str(bb)+" where id="+str(id)+" and GlyphName='"+glyphName+"'"+ids 
    print strg
    db.query(strg)
  
def update_glyphparam(id, a):
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    ids= " and idmaster="+'"'+str(idmaster)+'"'
    if a != '' :
      aa = a
    else:
      aa = 'NULL'
    db.update('glyphparam', where='id=$id and GlyphName="'+glyphName+'"'+ids, vars=locals(),
        pointName=aa)

def insert_glyphparam(id, a):
    
    glyphName = mfg.cFont.glyphName 
    idmaster = gidmast(mfg.cFont.idwork)
    db.insert('glyphparam', id=id,GlyphName=glyphName, PointName=a, idmaster=idmaster)

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

def update_master(id):

    fontNameA=mfg.cFont.fontna
    fontNameB=mfg.cFont.fontnb
    fontName=mfg.cFont.fontname 
    db.update('master', where='idmaster=$id', vars=locals(),
       fontNameA=fontNameA,fontNameB=fontNameB,FontName=fontName)
    return None

def get_globalparams():
    return db.select('globalparam', vars=locals())


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

def get_localparams():
    return db.select('localparam', vars=locals())

def get_localparam(id):
    print "idididget local",id
    return db.select('localparam', where='idlocal=$id',vars=locals())

def put_globalparam(id):

    superness=mfg.cFont.superness
    metapolation=mfg.cFont.metapolation
    penwidth=mfg.cFont.penwidth
    unitwidth=mfg.cFont.unitwidth
    xHeight=mfg.cFont.xHeight
    ht = mfg.cFont.ht
    fontsize = mfg.cFont.fontsize
    db.insert('globalparam', where='idglobal = $id',vars=locals(), 
        superness=superness, metapolation=metapolation, penwidth=penwidth, unitwidth=unitwidth, xHeigth=xHeigth , ht=ht, fontsize=fontsize)
    return None

def updatemaster(id, a, b, c, d):
    db.update('master', where='idmaster = $id', vars=locals(), 
      FontName = a, FontNameA = b, FontNameB = c, idglobal = d)
    return None

def update_globalparam(id, a, b, c, d, e, f, g, h):
    db.update('globalparam', where='idglobal = $id', vars=locals(), 
      superness = a, metapolation = b, penwidth = c, unitwidth = d, xHeight = e, ht = f, fontsize = g, maxstemcut = h)
    return None

def update_localparam(id, a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14 ):
    print "idididget local update",id
    db.update('localparam', where='idlocal = $id', vars=locals(), 
      px = a1, mean = a2, des=a3, ascl=a4, cap=a5, width=a6, xheight=a7, capital=a8, ascender=a9, descender=a10, inktrap=a11, stemcut=a12, skeleton=a13, superness=a14)
    return None


def writexml():

     glyphName = mfg.cFont.glyphName 
     print "*** 000",glyphName
     if mfg.cFont.idwork =='0' :
        print "*** 0",glyphName
        glyphsource  = mfg.cFont.fontpath+mfg.cFont.fontna + "/glyphs/"+glyphName+".glif"
        print "*** gylyphsource A*",glyphsource
        xmldoc = xmldocA
     if mfg.cFont.idwork =='1' :
        print "*** 1",glyphName
        xmldoc = xmldocB
        glyphsource = mfg.cFont.fontpath+mfg.cFont.fontnb + "/glyphs/"+glyphName+".glif"
        print "*** gylyphsource B*",glyphsource
     itemlist = xmldoc.getElementsByTagName('point')
     idmaster = gidmast(mfg.cFont.idwork)
     ids= " and idmaster="+'"'+str(idmaster)+'"'
     inum = 0
#     db_rows=list(db.query("SELECT PointName,x,y from glyphoutline"))
#    we assume the number of rows from the db >= the number of the itemlist 
     for  s in itemlist:
             inum = inum + 1
             qstr = "SELECT PointNr,x,y,PointName from vglyphoutline where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'+ids
            
             db_rows=list(db.query(qstr))
             s.attributes['pointNo'] = str(db_rows[0].PointNr)
             s.attributes['x'] = str(db_rows[0].x)
             s.attributes['y'] = str(db_rows[0].y)
             sname = str(db_rows[0].PointName)
             if sname <> "None" : 
                   qstrp = "SELECT * from glyphparam where id="+str(inum) +" and Glyphname="+'"'+glyphName+'"'+ids
                   db_rowparam = list(db.query(qstrp))
                   nameattr = sname
                   print "namename",nameattr
                   if s.hasAttribute('name') :
                      s.attributes['name']=nameattr
                   else :
                      s.setAttribute('name',nameattr)
#
#      read param value and write into xml
#
                   xxmlat(s,db_rowparam[0].startp,'startp','1')
                   xxmlat(s,db_rowparam[0].leftp,'leftp','1')
                   xxmlat(s,db_rowparam[0].superness,'superness','')
                   xxmlat(s,db_rowparam[0].rightp,'rightp','1')
                   xxmlat(s,db_rowparam[0].downp,'downp','1')
                   xxmlat(s,db_rowparam[0].upp,'upp','1')
                   xxmlat(s,db_rowparam[0].superqr,'superqr','')
                   xxmlat(s,db_rowparam[0].superleft,'superleft','')
                   xxmlat(s,db_rowparam[0].tension,'tension','')
                   xxmlat(s,db_rowparam[0].tensionend,'tensionend','')
                   xxmlat(s,db_rowparam[0].cycle,'cycle','')
                   xxmlat(s,db_rowparam[0].penshiftedx,'penshiftedx','')
                   xxmlat(s,db_rowparam[0].penshiftedy,'penshiftedy','')
                   xxmlat(s,db_rowparam[0].pointshiftx,'pointshiftx','')
                   xxmlat(s,db_rowparam[0].pointshifty,'pointshifty','')
                   xxmlat(s,db_rowparam[0].penwidth,'penwidth','')
                   xxmlat(s,db_rowparam[0].xHeight,'xHeight','')
                   xxmlat(s,db_rowparam[0].cardinal,'cardinal','')

             s.toxml()
     print "glyphsource", glyphsource
     with codecs.open(glyphsource, "w", "utf-8") as out:
          xmldoc.writexml(out) 

def writeGlyphlist():
  ifile=open(mfg.cFont.fontpath+"glyphlist.mf","w")
  


  return None

def writeGlobalParam():
#
# prepare font.mf parameter file
# write the file into the directory mfg.cFont.fontpath
#  
  master = list(get_master(mfg.cFont.idmaster)) 
  imgl = list(get_globalparam(mfg.cFont.idglobal))

  des=2.45
  asc=0.8
  cap=0.8

  superness = imgl[0].superness
  metapolation = imgl[0].metapolation
  px = imgl[0].penwidth
  u = imgl[0].unitwidth
  mean   = imgl[0].xHeight
  fontsize   = imgl[0].fontsize
  ht    = imgl[0].ht
  maxstemcut = imgl[0].maxstemcut
#
# global parameters
  ifile=open(mfg.cFont.fontpath+"font.mf","w")
  ifile.write("% parameter file \n")
  ifile.write("metapolation:=%.1f;\n"%metapolation)
  ifile.write("font_size:=%.0fpt#;\n"%fontsize)
  ifile.write("ht#:=%.0fpt#;\n"%ht)
  ifile.write("u#:=%.0fpt#;\n"%u)
  ifile.write("max_stemcut:=%.0fpt;\n"%maxstemcut)
  ifile.write("superness:=%.2f;\n"%superness)

# local parameters A  
  imlo = list(get_localparam(mfg.cFont.idlocalA))

  ifile.write("A_px#:=%.1fpt#;\n"%imlo[0].px)
  ifile.write("A_mean#:=%.2fpt#;\n"%imlo[0].mean)
  ifile.write("A_des#:=%.2fpt#;\n"%imlo[0].des)
  ifile.write("A_asc#:=%.1fht#;\n"%imlo[0].ascl)
  ifile.write("A_cap#:=%.1fht#;\n"%imlo[0].cap)
  ifile.write("A_width:=%.2f;\n"%imlo[0].width)
  ifile.write("A_xheight:=%.0f;\n"%imlo[0].xheight)
  ifile.write("A_capital:=%.0f;\n"%imlo[0].capital)
  ifile.write("A_ascender:=%.0f;\n"%imlo[0].ascender)
  ifile.write("A_descender:=%.0f;\n"%imlo[0].descender)
  ifile.write("A_inktrap:=%.0f;\n"%imlo[0].inktrap)
  ifile.write("A_stemcut:=%.0f;\n"%imlo[0].stemcut)
  ifile.write("A_skeleton#:=%.2fpt#;\n"%imlo[0].skeleton)
  ifile.write("A_superness:=%.2f;\n"%imlo[0].superness)
  
# local parameters B  
  imlo = list(get_localparam(mfg.cFont.idlocalB))

  ifile.write("B_px#:=%.1fpt#;\n"%imlo[0].px)
  ifile.write("B_mean#:=%.2fpt#;\n"%imlo[0].mean)
  ifile.write("B_des#:=%.2fpt#;\n"%imlo[0].des)
  ifile.write("B_asc#:=%.1fht#;\n"%imlo[0].ascl)
  ifile.write("B_cap#:=%.1fht#;\n"%imlo[0].cap)
  ifile.write("B_width:=%.2f;\n"%imlo[0].width)
  ifile.write("B_xheight:=%.0f;\n"%imlo[0].xheight)
  ifile.write("B_capital:=%.0f;\n"%imlo[0].capital)
  ifile.write("B_ascender:=%.0f;\n"%imlo[0].ascender)
  ifile.write("B_descender:=%.0f;\n"%imlo[0].descender)
  ifile.write("B_inktrap:=%.0f;\n"%imlo[0].inktrap)
  ifile.write("B_stemcut:=%.0f;\n"%imlo[0].stemcut)
  ifile.write("B_skeleton#:=%.2fpt#;\n"%imlo[0].skeleton)
  ifile.write("B_superness:=%.2f;\n"%imlo[0].superness)

  ifile.write("\n") 
  ifile.write("input glyphs\n") 
  ifile.write("bye\n") 
  ifile.close()
  return None 


def buildfname ( filename ):
    try :
      basename,extension = filename.split('.')
    except :
           extension="garbage"
           basename=""
    return [basename,extension]

def ufo2mf():
  print "************",mfg.cFont.fontpath
  dirnamef1 = mfg.cFont.fontpath+mfg.cFont.fontna+"/glyphs"
  dirnamef2 = mfg.cFont.fontpath+mfg.cFont.fontnb+"/glyphs"
  dirnamep1 = mfg.cFont.fontpath+"glyphs"
 
  charlist1 = [f for f in os.listdir(dirnamef1) ]
  charlist2 = [f for f in os.listdir(dirnamef2) ]

  for ch1 in charlist1: 
    fnb,ext=buildfname (ch1)
    if ext in ["glif"] and ( fnb == mfg.cFont.glyphName or mfg.cFont.timestamp == 0 ) :

      print "file",ch1
    
      try :
        filech1 = open(dirnamef1+"/"+ch1,'r')
        filech2 = open(dirnamef2+"/"+ch1,'r')
        commd1 = "ls "+dirnamef1+"/"+ch1
        os.system(commd1)
        newfile,extension = ch1.split('.')
        newfilename=newfile+".mf"
        commd2 = "python parser_pino_mono.py " +ch1 +" " +dirnamef1 +" " +dirnamef2 +" > " +dirnamep1 +"/" +newfilename
        os.system(commd2)
      except :
        print "error",dirnamef1+"/"+ch1
        print "error",dirnamef2+"/"+ch1
      continue
  
  mfg.cFont.timestamp=1
  return None

def writeGlyphlist():

  print "*** write glyphlist ***"
  ifile=open(mfg.cFont.fontpath+"glyphlist.mf","w")
 

  dirnamep1 = mfg.cFont.fontpath+"glyphs"
 
  charlist1 = [f for f in os.listdir(dirnamep1) ]

  for ch1 in charlist1: 
    fnb,ext=buildfname (ch1)
    if ext in ["mf"]  :

      ifile.write("input glyphs/"+ch1+"\n")
    
  ifile.close()
  return None


