""" Basic metfont point interface using webpy  """
import web
import model
import os
import sys
import glob 
### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/edit/(\d+)', 'Edit',
    '/viewfont/', 'ViewFont',
    '/font1/', 'Font1',
)


### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)
###  classes

class cFont:
     fontna = "oswald.ufo"
     fontnb = "oswald.ufo"
     glyphName = "c"

class Index:

    def GET (self):
        """ Show page """
        posts = model.get_posts()
        master = model.get_master()
        fontsource = [cFont.fontna,cFont.fontnb,cFont.glyphName]
        return render.index(posts,master,fontsource)


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

    formParam = web.form.Form(
        web.form.Textbox('startp',
	    size=1,
            description="start"),
        web.form.Textbox('superness',
            size=4, 
            description="superness"),
        web.form.Dropdown(name='Cardinal',
            args=['Up', 'Left', 'Down', 'Right'],
	    value='Up'),
        web.form.Dropdown(name='+ Parameter',
            args=['Tension', 'Direction', 'Line', 'Pen1', 'Pen2', 'Stem', 'Baseline', 'X-Height', 'Cap', 'Ascender', 'Descender']), web.form.Checkbox('delete'), 

#            if Tension in args :
#               formParam = web.form.Form(
#               web.form.Textbox('Tension',
#               size=5, 
#               description="Tension"))

        web.form.Button('saveParam'), 
        )

   


    def GET(self,id):
        """ View single post """
        post = model.get_post(int(id))
        posts = model.get_posts()
        form=self.form()
        glyphparam = model.get_glyphparam(int(id))
        form.fill(post)
        formParam = self.formParam()
        if glyphparam != None :
           formParam.fill(glyphparam)
        master = model.get_master()
        return render.view(posts,post,form,formParam,master)

    def POST(self, id):
        form = View.form()
        formParam = View.formParam()
        post = model.get_post(int(id))
        if not form.validates() :
            posts = model.get_posts()
            master = model.get_master()
            return render.view(posts, post, form, formParam, master)
        if form.d.PointName != None :
            if not formParam.validates() :
                return render.view(posts, post, form, formParam, master)
            if model.get_glyphparam(int(id)) != None :
                model.update_glyphparam(int(id),form.d.PointName, formParam.d.startp, formParam.d.superness, formParam.d.Cardinal)
            else :
                model.insert_glyphparam(int(id),form.d.PointName, formParam.d.startp, formParam.d.superness, formParam.d.Cardinal)
                
        model.update_post(int(id), form.d.x, form.d.y)
        posts = model.get_posts()
        master = model.get_master()
        model.writexml()        
        commstr = "python ufo2mf.py " + cFont.fontna+"/glyphs " + cFont.fontnb+"/glyphs glyphs"
        os.system(commstr)
        os.system("sh makefont.sh")
        return render.view(posts, post, form, formParam, master)

class ViewFont:
    def GET(self):
        """ View single post """
        param=Index.form.d.UFO_A
        return render.viewfont(param)

class Font1:
    form = web.form.Form(
        web.form.Textbox('UFO_A', web.form.notnull, 
            size=20,
#            description="namea", value="oswald.ufo"),
            description="namea", value=cFont.fontna),
        web.form.Textbox('UFO_B', web.form.notnull, 
            size=20,
            description="nameb", value=cFont.fontnb),
        web.form.Textbox('GLYPH', web.form.notnull, 
            size=5,
            description="glyph", value="c"),
        web.form.Button('savefont'),
        )
    def GET(self):
        fontna = cFont.fontna
        fontnb = cFont.fontnb
#        fontlist= ["oswald","meier"] 
        fontlist = [f for f in glob.glob("*.ufo")]
        form=self.form()
        form=Font1.form()
        form.fill({'UFO_A':fontna,'UFO_B':fontnb,'GLYPH':cFont.glyphName})
        return render.font1(fontlist,form)

    def POST (self):
        form = Font1.form()
        form.fill()
        print "form.d.UFO_A",form.d.UFO_A
        cFont.fontna = form.d.UFO_A
        cFont.fontnb = form.d.UFO_B
        cFont.glyphName  = form.d.GLYPH
        print "glyph",form.d.GLYPH
        model.putFont()
        fontlist = [f for f in glob.glob("*.ufo")]
        return render.font1(fontlist,form)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()

