"""Typeset text as SVG outlines with matplotlib, so the header does not depend on installed fonts."""
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path
import numpy as np
FONTS={
 'lm17':'/usr/share/texmf/fonts/opentype/public/lm/lmroman17-regular.otf',
 'lm12i':'/usr/share/texmf/fonts/opentype/public/lm/lmroman12-italic.otf',
 'lm10':'/usr/share/texmf/fonts/opentype/public/lm/lmroman10-regular.otf',
 'lm10i':'/usr/share/texmf/fonts/opentype/public/lm/lmroman10-italic.otf',
 'pagella':'/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-regular.otf',
 'pagellai':'/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-italic.otf',
 'lora':'/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf',
}
def text_d(s,font,size,x=0,y=0,anchor='start'):
    fp=FontProperties(fname=FONTS[font])
    tp=TextPath((0,0),s,size=size,prop=fp)
    v=tp.vertices.copy(); codes=tp.codes
    w=tp.get_extents().x1 if len(v) else 0
    adv=w
    if anchor=='end': x-=adv
    elif anchor=='middle': x-=adv/2
    out=[];i=0
    def P(p): return f"{x+p[0]:.2f} {y-p[1]:.2f}"
    while i<len(v):
        c=codes[i]
        if c==Path.MOVETO: out.append('M'+P(v[i])); i+=1
        elif c==Path.LINETO: out.append('L'+P(v[i])); i+=1
        elif c==Path.CURVE3: out.append('Q'+P(v[i])+' '+P(v[i+1])); i+=2
        elif c==Path.CURVE4: out.append('C'+P(v[i])+' '+P(v[i+1])+' '+P(v[i+2])); i+=3
        elif c==Path.CLOSEPOLY: out.append('Z'); i+=1
        else: i+=1
    return ''.join(out), adv
