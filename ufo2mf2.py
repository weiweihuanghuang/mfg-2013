import os 
import sys

def buildfname ( filename ):
    try :
      basename,extension = filename.split('.')
    except :
           extension="garbage"
           basename=""
    return [basename,extension]

dirnamef1 = sys.argv[1]
dirnamef2 = sys.argv[2]
dirnamep1 = sys.argv[3]
if len(dirnamef1)>2 and len(dirnamef2)>2 and len(dirnamep1)>2 :
  
  charlist1 = [f for f in os.listdir(dirnamef1)  ]
  charlist2 = [f for f in os.listdir(dirnamef2) ]
  
#  commd1="mkdir "+dirnamep1
#  os.system(commd1)

  for ch1 in charlist1:
     fnb,ext=buildfname (ch1)
     if ext in ["glif"] :
       print "file",ch1
       try :
         filech1 = open(dirnamef1+"/"+ch1,'r')
         filech2 = open(dirnamef2+"/"+ch1,'r')
         print " "
         print dirnamef1,  " ch ", ch1 
         print " "
         commd1 = "ls "+dirnamef1+"/"+ch1
         os.system(commd1)
         newfile,extension = ch1.split('.')
         newfilename=newfile+".mf"
         commd2 = "python parser.py " +ch1 +" " +dirnamef1 +" " +dirnamef2 +" > " +dirnamep1 +"/" +newfilename
         os.system(commd2)
       except : 
         print "error",dirnamef2+"/"+ch1
       continue

else :
        print "error in argument directory names"
