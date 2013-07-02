import sys
# Python script

# %if sys.argv[1]<>0 :
#   incx = sys.argv[1]
# else :
#   incx = 1.1


#fl = open("parammeta.txt",r)
#incx = fl.read()

string = "% parameter file \n"

#global parameter
string = string + "incx:=0;\n"
string = string + "font_size:=12pt#;\n"  
string = string + "ht#:=10pt#; \n"      
string = string + "u#:=1pt#; \n"      			 
string = string + "superness:=1.2; \n"  
string = string + "max_stemcut:=40; \n"

#local parameter A at incx = 0
string = string + "A_px#:=0.1pt#; \n"      					
string = string + "A_mean#:=6.12pt#; \n"
string = string + "A_des#:=2.45pt#; \n"
string = string + "A_asc#:=0.8ht#; \n"
string = string + "A_cap#:=0.8ht#; \n"
string = string + "A_width:=1; \n"
string = string + "A_xheight:=1; \n"
string = string + "A_capital:=1; \n"
string = string + "A_ascender:=1; \n"
string = string + "A_descender:=1; \n"
string = string + "A_inktrap:=10; \n"
string = string + "A_stemcut:=20; \n"
string = string + "A_skeleton#:=0pt#; \n"

#local parameter B at incx = 1
string = string + "B_px#:=0.1pt#; \n"      					
string = string + "B_mean#:=6.12pt#; \n"
string = string + "B_des#:=2.45pt#; \n"
string = string + "B_asc#:=0.8ht#; \n"
string = string + "B_cap#:=0.8ht#; \n"
string = string + "B_width:=1.05; \n"
string = string + "B_xheight:=1; \n"
string = string + "B_capital:=1; \n"
string = string + "B_ascender:=1; \n"
string = string + "B_descender:=1; \n"
string = string + "B_inktrap:=10; \n"
string = string + "B_stemcut:=0; \n"
string = string + "B_skeleton#:=0.02pt#; \n"

#glyph parameter
string = string + "width_n:=1; \n"
string = string + "width_nL:=0; \n"
string = string + "width_nR#:=0pt#; \n"


string = string + "  \n"
string = string + "input glyphs \n"
string = string + "bye \n"
string = string + " \n"

#string = string + "contr:=0; \n"
#progressive contrast increase
#string = string + "contr:=-30incx+35pt#; \n"


print string
