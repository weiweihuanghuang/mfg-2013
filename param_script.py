import sys
# Python script

# %if sys.argv[1]<>0 :
#   incx = sys.argv[1]
# else :
#   incx = 1.1


#fl = open("parammeta.txt",r)
#incx = fl.read()

string = "% parameter file \n"

string = string + "incx:=0;\n"

# string = string + "incx:="+incx + ";\n"
string = string + "font_size:=12pt#;\n"  
string = string + "ht#:=10pt#; \n"      
string = string + "u#:=1pt#; \n"      			 
string = string + "px#:=.1pt#; \n"      					
string = string + "superness:=1.0; \n"  
string = string + "mean#:=6.12pt#; \n"
string = string + "des#:=2.45pt#; \n"
string = string + "asc#:=0.8ht#; \n"
string = string + "cap#:=0.8ht#; \n"
string = string + "  \n"
string = string + "input glyphs \n"
string = string + "bye \n"
string = string + " \n"

print string
