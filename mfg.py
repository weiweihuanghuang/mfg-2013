""" Basic metafont point interface using webpy  """
import web
import model
import os
import sys
import glob 
### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/metap/(\d+)', 'Metap',
    '/viewfont/', 'ViewFont',
    '/font1/(\d+)', 'Font1',
    '/font2/(\d+)', 'GlobalParam',
    '/font3/(\d+)', 'localParamA',
    '/font4/(\d+)', 'localParamB',
)


### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)
###  classes



### preset font loading

class cFont:
     fontpath = "fonts/1/"
     fontna = ""
     fontnb = ""
     fontname = ""
     idglobal = 1
     idmaster = 1
     idwork   = '0'
     glyphName =""
     glyphunic = "1"
     superness =1
     metapolation=0.5
     over=0.1
     penwidth=1
     unitwidth=1
     xHeight=1
     fontsize=12
     ht=10
     timestamp=0
     idlocalA = 1
     idlocalB = 2
     loadoption = '0'
 
class Index:

    def GET (self):
        """ Show page """
        posts = model.get_posts()
        master = model.get_masters()
        fontsource = [cFont.fontna,cFont.fontnb,cFont.glyphName]
	webglyph = cFont.glyphName
        return render.metap(posts,master,fontsource,webglyph)


class Metap:

    def GET (self,id):
        """ Show page """
        cFont.idwork=id
        posts = model.get_posts()
        master = model.get_masters()
#        fontsource = [cFont.fontna,cFont.fontnb,cFont.glyphName]

        if id =='0':
#          we are working on font A
#
           fontsource = [cFont.fontna,cFont.glyphName]
        if id =='1':
#          we are working on font B
#          
           fontsource = [cFont.fontnb,cFont.glyphName]

	webglyph = cFont.glyphName
        return render.metap(posts,master,fontsource,webglyph)

class View:
    form = web.form.Form(
        web.form.Textbox('PointNr', web.form.notnull, 
            size=3,
            description="nr"),
        web.form.Textbox('x', web.form.notnull, 
            size=5,
            description="x"), 
        web.form.Textbox('y', web.form.notnull, 
            size=5,
            description="y"),
        web.form.Textbox('PointName',  
            size=5,
            description="name"),
        web.form.Button('save'), 
        )

# add glyphparameters here:

    formParam = web.form.Form(
        web.form.Dropdown('Param',
            [('startp','startp'),('doubledash','doubledash'),('tripledash','tripledash'),('leftp','leftp'),('rightp','rightp'),('downp','downp'),('upp','upp'),('dir','dir'),('leftp2','leftp2'),('rightp2','rightp2'),('downp2','downp2'),('upp2','upp2'),('dir2','dir2'),('superright','superright'),('superleft','superleft'),('tension','tension'),('tensionand','tensionand'),('cycle','cycle'),('penshifted','penshifted'),('pointshifted','pointshifted'),('penwidth','penwidth'),('xHeight','xHeight'),('cardinal','cardinal'),('superness','superness'),('overx','overx'),('overbase','overbase'),('overcap','overcap'),('stemcutter','stemcutter'),('stemshift','stemshift'),('inktrap_l','inktrap_l'),('inktrap_r','inktrap_r')]), 
        web.form.Textbox('parmval',
            size=15, 
            description="parmval"),
        web.form.Button('saveParam'), 
        )

    def GET(self,id):
        """ View single post """
        form=self.form()
        
        if id > '0' : 
           post = model.get_post(int(id))
           glyphparam = model.get_glyphparam(int(id))
           form.fill(post)
        posts = model.get_posts()
        postspa = model.get_postspa()
        formParam = self.formParam()
        if glyphparam != None :
           formParam.fill(glyphparam)
        mastglobal = model.get_globalparam(cFont.idglobal)
        master = model.get_master(cFont.idmaster)
	webglyph = cFont.glyphName
        return render.view(posts,post,form,formParam,master,mastglobal,webglyph,glyphparam,cFont,postspa)

    def POST(self, id):
        form = View.form()
        formParam = View.formParam()
        post = model.get_post(int(id))
        postspa = model.get_postspa()
        formParam = self.formParam()
        if not form.validates() :
            posts = model.get_posts()
            master = model.get_master(cFont.idmaster)
            mastglobal = model.get_globalparam(cFont.idglobal)
	    webglyph = cFont.glyphName
            return render.view(posts, post, form, formParam, master,mastglobal, webglyph,glyphparam,cFont,postspa)
        if form.d.PointName != None :
            if not formParam.validates() :
                return render.view(posts, post, form, formParam, master,mastglobal)
            if model.get_glyphparam(int(id)) != None :
                model.update_glyphparam(int(id),form.d.PointName)

                model.update_glyphparamD(int(id),formParam.d.Param, formParam.d.parmval)
            else :
                model.insert_glyphparam(int(id),form.d.PointName )
                
        model.update_post(int(id), form.d.x, form.d.y)
        posts = model.get_posts()
        master = model.get_master(cFont.idmaster)
        mastglobal = model.get_globalparam(cFont.idglobal)
	webglyph = cFont.glyphName
        glyphparam = model.get_glyphparam(int(id))

        model.writexml()        
        model.ufo2mf() 
        os.environ['MFINPUTS'] = cFont.fontpath
#        os.environ['MPINPUTS'] = cFont.fontpath
        model.writeGlyphlist()
        strms = "sh makefont.sh font.mf"
        print strms
        os.system(strms)
        return render.view(posts, post, form, formParam, master, mastglobal,webglyph,glyphparam,cFont,postspa)

class ViewFont:
    def GET(self):
        """ View single post """
        param=cFont.glyphName
        return render.viewfont(param)

class Font1:
    form = web.form.Form(
        web.form.Textbox('Name', web.form.notnull, 
            size=30,
            description="name", value=cFont.fontna),
        web.form.Textbox('UFO_A', web.form.notnull, 
            size=20,
            description="fontnameA", value=cFont.fontna),
        web.form.Textbox('UFO_B', web.form.notnull, 
            size=20,
            description="fontnameB", value=cFont.fontnb),
        web.form.Textbox('GLYPH', web.form.notnull, 
            size=5,
            description="glyph", value="c"),
        web.form.Textbox('loadoption', web.form.notnull, 
            size=1,
            description="loadoption", value="0"),

        web.form.Button('savefont'),
        )
    def GET(self,id):
        mmaster= list(model.get_masters())
        if id > '0' and id <'1000': 
           master= list(model.get_master(id))
        if id > "1000" :
              cFont.glyphName = chr(int(id)-1001+32)
              cFont.glyphunic = str(int(id)-1001)
        fontname =cFont.fontname 
        fontna = cFont.fontna
        fontnb = cFont.fontnb
        loadoption = cFont.loadoption
        fontlist = [f for f in glob.glob("fonts/*/*.ufo")]
        fontlist.sort()
        form=self.form()
        form=Font1.form()
        form.fill({'Name':fontname,'UFO_A':fontna,'UFO_B':fontnb,'GLYPH':cFont.glyphName,'loadoption':cFont.loadoption})
        return render.font1(fontlist,form,mmaster,cFont)

    def POST (self,id):
        print "post",id
        mmaster= list(model.get_masters())
        form = Font1.form()
        form.fill()
        cFont.fontname = form.d.Name
        cFont.fontna = form.d.UFO_A
        cFont.fontnb = form.d.UFO_B
        if id >'1000' :
           form.d.GLYPH=chr(int(id)-1001+32)
           cFont.glyphunic = str(int(id)-1001)
           form.fill()
        cFont.glyphName  = form.d.GLYPH
        cFont.loadoption = form.d.loadoption
        if id > '0' and id <'1000':
           model.update_master(id)
           master= list(model.get_master(id))
        model.putFont()
        fontlist = [f for f in glob.glob("fonts/*/*.ufo")]
        fontlist.sort()
        return render.font1(fontlist,form,mmaster,cFont)

class GlobalParam:

    formg = web.form.Form( 
        web.form.Textbox('superness', web.form.notnull, 
            size=3,
            description="superness", value="1"),
        web.form.Textbox('metapolation', web.form.notnull, 
            size=3,
            description="metapolation", value="0.5"),
        web.form.Textbox('penwidth', web.form.notnull, 
            size=3,
            description="penwidth", value="1.0"),
        web.form.Textbox('unitwidth', web.form.notnull, 
            size=3,
            description="unitwidth", value="1.0"),
        web.form.Textbox('xHeight', web.form.notnull, 
            size=3,
            description="xHeight", value="1.0"),
        web.form.Textbox('ht', web.form.notnull, 
            size=3,
            description="ht", value="10"),
        web.form.Textbox('fontsize', web.form.notnull, 
            size=3,
            description="fontsize", value="10"),
        web.form.Textbox('maxstemcut', web.form.notnull, 
            size=3,
            description="maxstemcut", value="10"),
        web.form.Textbox('over', web.form.notnull, 
            size=3,
            description="over", value="0.1"),

        web.form.Button('saveg'),
        )

    def GET(self,id):
        
        print "getparam",id
        gml = list(model.get_globalparams())
        formg = self.formg()
        if id > '0' :
          gm = list(model.get_globalparam(id))
        else:
          gm = None

        if gm != None:
             formg.fill({'superness':gm[0].superness,'metapolation':gm[0].metapolation,'penwidth':gm[0].penwidth,'unitwidth':gm[0].unitwidth,'xHeight':gm[0].xHeight,'ht':gm[0].ht,'fontsize':gm[0].fontsize,'maxstemcut':gm[0].maxstemcut,'over':gm[0].over})
        return render.font2(formg,gml,cFont)

    def POST (self,id):
        print "postparam",id
        gml = list(model.get_globalparams())
        gm = list(model.get_globalparam(id))
        formg = self.formg()
        formg.fill()
        if formg.validates  :
               model.update_globalparam(id, formg.d.superness, formg.d.metapolation, formg.d.penwidth, formg.d.unitwidth, formg.d.xHeight, formg.d.ht, formg.d.fontsize, formg.d.maxstemcut, formg.d.over)
        if not formg.validates() :
               return render.font2(formg,gml,cFont)

        model.writeGlobalParam()

        return render.font2(formg,gml,cFont)
class localParamA:

    formlocA = web.form.Form(
        web.form.Textbox('px', web.form.notnull, 
            size=3,
            description="px", value="1"),
        web.form.Textbox('mean', web.form.notnull, 
            size=3,
            description="mean", value="5"),
        web.form.Textbox('des', web.form.notnull, 
            size=3,
            description="des", value="2"),
        web.form.Textbox('asc', web.form.notnull, 
            size=3,
            description="asc", value="1.0"),
        web.form.Textbox('cap', web.form.notnull, 
            size=3,
            description="cap", value="1.0"),

  	web.form.Textbox('width', web.form.notnull, 
            size=3,
            description="width", value="1"),

        web.form.Textbox('xheight', web.form.notnull, 
            size=3,
            description="xheight", value="10"),
        web.form.Textbox('capital', web.form.notnull, 
            size=3,
            description="capital", value="10"),
        web.form.Textbox('ascender', web.form.notnull, 
            size=3,
            description="ascender", value="10"),
        web.form.Textbox('descender', web.form.notnull, 
            size=3,
            description="descender", value="10"),
        web.form.Textbox('inktrap', web.form.notnull, 
            size=3,
            description="inktrap", value="10"),
        web.form.Textbox('stemcut', web.form.notnull, 
            size=3,
            description="stemcut", value="10"),
        web.form.Textbox('skeleton', web.form.notnull, 
            size=3,
            description="skeleton", value="10"),
        web.form.Textbox('superness', web.form.notnull, 
            size=3,
            description="superness", value="30"),
        web.form.Button('saveA'),
        )
    def GET(self,id):
        
        print "getparam",id
        gml = list(model.get_globalparams())
        formg = GlobalParam.formg()
        glo = list(model.get_localparams())
        formlA = self.formlocA()
        formlB = localParamB.formlocB()
        gm = list(model.get_globalparam(cFont.idglobal))
        formg.fill({'superness':gm[0].superness,'metapolation':gm[0].metapolation,'penwidth':gm[0].penwidth,'unitwidth':gm[0].unitwidth,'xHeight':gm[0].xHeight,'ht':gm[0].ht,'fontsize':gm[0].fontsize,'maxstemcut':gm[0].maxstemcut,'over':gm[0].over})
        idlA =id 
        
        idlB =cFont.idlocalB
        if idlA > '0' :
          cFont.idlocalA = id
          gloA = list(model.get_localparam(id))
        else:
          gloA = None
        if idlB > '0' :
          gloB = list(model.get_localparam(idlB))
        else:
          gloB = None

        if gloA != None:
           formlA.fill({'px':gloA[0].px,'mean':gloA[0].mean,'des':gloA[0].des,'asc':gloA[0].ascl,'cap':gloA[0].cap,'width':gloA[0].width,'xheight':gloA[0].xheight,'capital':gloA[0].capital,'ascender':gloA[0].ascender,'descender':gloA[0].descender,'inktrap':gloA[0].inktrap,'stemcut':gloA[0].stemcut,'skeleton':gloA[0].skeleton,'superness':gloA[0].superness})
        if gloB != None:
           formlB.fill({'px':gloB[0].px,'mean':gloB[0].mean,'des':gloB[0].des,'asc':gloB[0].ascl,'cap':gloB[0].cap,'width':gloB[0].width,'xheight':gloB[0].xheight,'capital':gloB[0].capital,'ascender':gloB[0].ascender,'descender':gloB[0].descender,'inktrap':gloB[0].inktrap,'stemcut':gloB[0].stemcut,'skeleton':gloB[0].skeleton,'superness':gloB[0].superness})

        return render.font3(formg,gml,cFont,glo,formlA,formlB)

    def POST (self,id):
        gml = list(model.get_globalparams())
        glo = list(model.get_localparams())
        idlB = cFont.idlocalB 
        idlA = id
        cFont.idlocalA=id 
        gloA = list(model.get_localparam(idlA))
        gloB = list(model.get_localparam(idlB))
        formg = GlobalParam.formg()
        formlA = self.formlocA() 
        formlB = localParamB.formlocB() 
        formlA.fill()

        formlB.fill({'px':gloB[0].px,'mean':gloB[0].mean,'des':gloB[0].des,'asc':gloB[0].ascl,'cap':gloB[0].cap,'width':gloA[0].width,'xheight':gloB[0].xheight,'capital':gloB[0].capital,'ascender':gloB[0].ascender,'descender':gloB[0].descender,'inktrap':gloB[0].inktrap,'stemcut':gloB[0].stemcut,'skeleton':gloB[0].skeleton,'superness':gloB[0].superness})

        if formlA.validates() :
               model.update_localparam(idlA,formlA.d.px,formlA.d.mean,formlA.d.des,formlA.d.asc,formlA.d.cap,formlA.d.width,formlA.d.xheight,formlA.d.capital,formlA.d.ascender,formlA.d.descender,formlA.d.inktrap,formlA.d.stemcut,formlA.d.skeleton,formlA.d.superness)

        if not formlA.validates() :
               return render.font3(formg,gml,cFont,glo,formlA,formlB)

        model.writeGlobalParam()
        return render.font3(formg,gml,cFont,glo,formlA,formlB)


class localParamB:

    formlocB = web.form.Form(
        web.form.Textbox('px', web.form.notnull, 
            size=3,
            description="px", value="1"),
        web.form.Textbox('mean', web.form.notnull, 
            size=3,
            description="mean", value="5"),
        web.form.Textbox('des', web.form.notnull, 
            size=3,
            description="des", value="2"),
        web.form.Textbox('asc', web.form.notnull, 
            size=3,
            description="asc", value="1.0"),
        web.form.Textbox('cap', web.form.notnull, 
            size=3,
            description="cap", value="1.0"),


  	web.form.Textbox('width', web.form.notnull, 
            size=3,
            description="width", value="1"),


        web.form.Textbox('xheight', web.form.notnull, 
            size=3,
            description="xheight", value="10"),
        web.form.Textbox('capital', web.form.notnull, 
            size=3,
            description="capital", value="10"),
        web.form.Textbox('ascender', web.form.notnull, 
            size=3,
            description="ascender", value="10"),
        web.form.Textbox('descender', web.form.notnull, 
            size=3,
            description="descender", value="10"),
        web.form.Textbox('inktrap', web.form.notnull, 
            size=3,
            description="inktrap", value="10"),
        web.form.Textbox('stemcut', web.form.notnull, 
            size=3,
            description="stemcut", value="10"),
        web.form.Textbox('skeleton', web.form.notnull, 
            size=3,
            description="skeleton", value="10"),
        web.form.Textbox('superness', web.form.notnull, 
            size=3,
            description="superness", value="20"),
        web.form.Button('saveB'),
        )
    def GET(self,id):
        
        gml = list(model.get_globalparams())
        formg = GlobalParam.formg()
        glo = list(model.get_localparams())
        formlA = localParamA.formlocA()
        formlB = self.formlocB()
        gm = list(model.get_globalparam(cFont.idglobal))
        formg.fill({'superness':gm[0].superness,'metapolation':gm[0].metapolation,'penwidth':gm[0].penwidth,'unitwidth':gm[0].unitwidth,'xHeight':gm[0].xHeight,'ht':gm[0].ht,'fontsize':gm[0].fontsize,'maxstemcut':gm[0].maxstemcut,'over':gm[0].over})
        idlA = cFont.idlocalA  
        idlB =id 
        if idlA > '0' :
          gloA = list(model.get_localparam(idlA))
        else:
          gloA = None
        if idlB > '0' :
          gloB = list(model.get_localparam(id))
        else:
          gloB = None

        if gloA != None:
           formlA.fill({'px':gloA[0].px,'mean':gloA[0].mean,'des':gloA[0].des,'asc':gloA[0].ascl,'cap':gloA[0].cap,'width':gloA[0].width,'xheight':gloA[0].xheight,'capital':gloA[0].capital,'ascender':gloA[0].ascender,'descender':gloA[0].descender,'inktrap':gloA[0].inktrap,'stemcut':gloA[0].stemcut,'skeleton':gloA[0].skeleton,'superness':gloA[0].superness})
        if gloB != None:
           formlB.fill({'px':gloB[0].px,'mean':gloB[0].mean,'des':gloB[0].des,'asc':gloB[0].ascl,'cap':gloB[0].cap,'width':gloB[0].width,'xheight':gloB[0].xheight,'capital':gloB[0].capital,'ascender':gloB[0].ascender,'descender':gloB[0].descender,'inktrap':gloB[0].inktrap,'stemcut':gloB[0].stemcut,'skeleton':gloB[0].skeleton,'superness':gloB[0].superness})

        return render.font4(formg,gml,cFont,glo,formlA,formlB)

    def POST (self,id):
        gml = list(model.get_globalparams())
        glo = list(model.get_localparams())
        idlA = cFont.idlocalA 
        cFont.idlocalB = id
        idlB =id 
#                id argument via the html
#
        gloB = list(model.get_localparam(id))
        gloA = list(model.get_localparam(idlA))
        formlB = self.formlocB()
        formlA = localParamA.formlocA()
        formg = GlobalParam.formg()
        formlB.fill()

        formlA.fill({'px':gloA[0].px,'mean':gloA[0].mean,'des':gloA[0].des,'asc':gloA[0].ascl,'cap':gloA[0].cap,'width':gloA[0].width,'xheight':gloA[0].xheight,'capital':gloA[0].capital,'ascender':gloA[0].ascender,'descender':gloA[0].descender,'inktrap':gloA[0].inktrap,'stemcut':gloA[0].stemcut,'skeleton':gloA[0].skeleton,'superness':gloA[0].superness})

        if formlB.validates() :
              model.update_localparam(idlB,formlB.d.px,formlB.d.mean,formlB.d.des,formlB.d.asc,formlB.d.cap,formlB.d.width,formlB.d.xheight,formlB.d.capital,formlB.d.ascender,formlB.d.descender,formlB.d.inktrap,formlB.d.stemcut,formlB.d.skeleton,formlB.d.superness)
        if not formlB.validates() :
               return render.font4(formg,gml,cFont,glo,formlA,formlB)

        model.writeGlobalParam()

        return render.font4(formg,gml,cFont,glo,formlA,formlB)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()

