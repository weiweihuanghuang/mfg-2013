rm font.mf
rm font.2602gf
rm missfont.log
rm font.log
rm font.dvi
rm font.otf
rm font.ttf
rm font.tfm
rm font.pfb
rm font.afm
rm font.svg
rm font.woff
rm font.eot
rm font.pdf
rm font-webfont.eot
rm font-webfont.woff
rm font-webfont.ttf

python param_script.py  > font.mf

# mf font.mf

perl mf2pt1.pl --encoding=t1 --comment="Copyright (c) 2013" --family="font" --nofixedpitch --fullname="font" --name="font-regular" --weight="regular" font.mf

sfnt2woff font.otf && ~/Sites/mfg6/ttf2eot font.ttf > font.eot
sfnt2woff font.otf > font.woff

mv font.eot ~/Sites/mfg6/static/font-webfont.eot
mv font.woff ~/Sites/mfg6/static/font-webfont.woff
mv font.ttf ~/Sites/mfg6/static/font-webfont.ttf
mv font.otf ~/Sites/mfg6/static/font.otf
