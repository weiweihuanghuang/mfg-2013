import sys
# Python script

# %if sys.argv[1]<>0 :
#   incx = sys.argv[1]
# else :
#   incx = 1.1


#fl = open("parammeta.txt",r)
#incx = fl.read()

string = "% parameter file \n"

string = string + "incx:=0.5;\n"

# string = string + "incx:="+incx + ";\n"
string = string + "font_size:=12pt#;\n"  
string = string + "ht#:=10pt#; \n"      
string = string + "u#:=1pt#; \n"      			 
string = string + "px#:=.8pt#; \n"  
string = string + "penx:=1; \n"      					    					
string = string + "superness:=1.08; \n"  
string = string + "xheight:=1.0; \n"
string = string + "mean#:=4.10pt# * xheight; \n"
string = string + "des#:=2.45pt#; \n"
string = string + "asc#:=0.72ht#; \n"
string = string + "cap#:=0.65ht#; \n"
string = string + "width:=1; \n"
string = string + "widthcomp:=.1; \n"
string = string + "capital:=1; \n"
string = string + "ascender:=1; \n"
string = string + "descender:=1; \n"
string = string + "over#:=0.1u#; \n"
string = string + "baseline:=0; \n"
string = string + "winkel:=1; \n"
string = string + "rotationA:=0; \n"
string = string + "rotationB:=0; \n"


# extra parameters

string = string + "width_a:=1.1; \n"
string = string + "width_B:=1; \n"
string = string + "width_N:=1; \n"
string = string + "width_n:=1; \n"
string = string + "width_o:=1; \n"
string = string + "width_g:=1; \n"
string = string + "width_b:=1; \n"
string = string + "width_c:=1; \n"
string = string + "width_d:=1; \n"
string = string + "width_e:=1; \n"
string = string + "width_f:=1; \n"
string = string + "width_g:=1; \n"
string = string + "width_h:=1; \n"
string = string + "width_i:=1; \n"
string = string + "width_j:=1; \n"
string = string + "width_k:=1; \n"




string = string + "  \n"
string = string + "input glyphs \n"
string = string + "bye \n"
string = string + " \n"

print string
