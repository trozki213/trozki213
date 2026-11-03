"""Profile header: a Hodgkin–Huxley neuron at three input currents, drawn on graph paper.
Run from anywhere: python tools/banner.py"""
import numpy as np
from hh import sim
from textpath import text_d

W,H=1280,470
M=56
THEMES={
 'light':dict(edge='#cbdcd7',bg='#ffffff',minor='#e3ece9',major='#c9dcd6',ink='#13233f',ink2='#46566f',muted='#6f7d93',cursor='rgba(19,35,63,0.35)'),
 'dark': dict(edge='rgba(255,255,255,0.10)',bg='#0c2a4a',minor='rgba(255,255,255,0.05)',major='rgba(255,255,255,0.115)',ink='#f2f6fc',ink2='#bccbe0',muted='#91a6c4',cursor='rgba(242,246,252,0.45)'),
}
T=150.0
GX0=176                      # traces start (left gutter holds channel labels)
GX1=W-M
currents=[5.5,6.2,6.3]
base=[282,357,432]
SCALE=0.62                   # px per mV
DUR=3.4; BEGIN=0.3

def trace(I,yb):
    t,v=sim(I,T=T,dt=0.01)
    t=t[::4]; v=v[::4]
    xs=GX0+(t/T)*(GX1-GX0); ys=yb-(v+65.0)*SCALE
    keep=[0]
    for i in range(1,len(xs)-1):
        if abs(ys[i]-ys[keep[-1]])>0.12 or xs[i]-xs[keep[-1]]>5 or abs(ys[i+1]-ys[i])>0.12:
            keep.append(i)
    keep.append(len(xs)-1)
    return 'M'+'L'.join(f"{xs[i]:.1f} {ys[i]:.1f}" for i in keep)

def build(theme):
    c=THEMES[theme]; o=[]
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">')
    o.append('<title id="t">Antonio Troiano</title>')
    o.append('<desc id="d">Mathematical and Computing Sciences for AI, Bocconi University. The traces are the membrane potential of a simulated Hodgkin–Huxley neuron driven by constant currents of 5.5, 6.2 and 6.3 µA/cm²: only the last one fires repetitively.</desc>')
    o.append(f'''<defs>
<pattern id="mm" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M8 0H0V8" fill="none" stroke="{c['minor']}" stroke-width="0.8"/></pattern>
<pattern id="cm" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="translate({M%40} {M%40})"><rect width="40" height="40" fill="url(#mm)"/><path d="M40 0H0V40" fill="none" stroke="{c['major']}" stroke-width="1.2"/></pattern>
<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<clipPath id="pen"><rect x="0" y="0" width="{GX0-3}" height="{H}"><animate attributeName="width" from="{GX0-3}" to="{GX1+6}" begin="{BEGIN}s" dur="{DUR}s" fill="freeze"/></rect></clipPath>
</defs>''')
    o.append(f'''<style>
.tr{{fill:none;stroke:{c['ink']};stroke-width:2.2;stroke-linejoin:round;stroke-linecap:round}}
.static{{display:none}}
@media (prefers-reduced-motion: reduce){{.anim,.cursor{{display:none}}.static{{display:inline}}}}
</style>''')
    o.append('<g clip-path="url(#card)">')
    o.append(f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/><rect width="{W}" height="{H}" fill="url(#cm)"/>')
    o.append('<g class="anim" clip-path="url(#pen)"><g id="traces">'+''.join(f'<path class="tr" d="{trace(I,yb)}"/>' for I,yb in zip(currents,base))+'</g></g>')
    o.append('<use class="static" href="#traces" xlink:href="#traces"/>')
    # recorder cursor
    o.append(f'<line class="cursor" x1="{GX0-3}" x2="{GX0-3}" y1="{base[0]-80}" y2="{base[-1]+18}" stroke="{c["cursor"]}" stroke-width="1.5" opacity="0">'
             f'<animate attributeName="x1" from="{GX0-3}" to="{GX1+6}" begin="{BEGIN}s" dur="{DUR}s" fill="freeze"/>'
             f'<animate attributeName="x2" from="{GX0-3}" to="{GX1+6}" begin="{BEGIN}s" dur="{DUR}s" fill="freeze"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.04;0.9;1" begin="{BEGIN}s" dur="{DUR+0.3}s" fill="freeze"/></line>')
    # name + subtitle
    d,_=text_d('Antonio Troiano','lm17',78,M-2,128); o.append(f'<path d="{d}" fill="{c["ink"]}"/>')
    d,_=text_d('Mathematical and Computing Sciences for AI, Bocconi University','lm12i',27,M,172); o.append(f'<path d="{d}" fill="{c["ink2"]}"/>')
    # channel labels in the left gutter, right-aligned
    for I,yb in zip(currents,base):
        d,_=text_d(f'{I}','lm10',24,GX0-58,yb+1,anchor='end'); o.append(f'<path d="{d}" fill="{c["muted"]}"/>')
    d,_=text_d('µA/cm²','lm10i',18,GX0-58,base[0]-50,anchor='end'); o.append(f'<path d="{d}" fill="{c["muted"]}"/>')
    # scale bar: 20 ms, 50 mV (top right, above the quiet stretch of the first channel)
    sx1=GX1; sx0=sx1-20/T*(GX1-GX0); sy=base[0]-46; sv=50*SCALE
    o.append(f'<path d="M{sx0:.1f} {sy-sv:.1f}V{sy:.1f}H{sx1:.1f}" fill="none" stroke="{c["muted"]}" stroke-width="2"/>')
    d,_=text_d('20 ms','lm10',18,(sx0+sx1)/2,sy+22,anchor='middle'); o.append(f'<path d="{d}" fill="{c["muted"]}"/>')
    d,_=text_d('50 mV','lm10',18,sx0-10,sy-sv/2+6,anchor='end'); o.append(f'<path d="{d}" fill="{c["muted"]}"/>')
    o.append('</g>')
    o.append(f'<rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="17.5" fill="none" stroke="{c["edge"]}" stroke-width="1.5"/>')
    o.append('</svg>')
    return ''.join(o)

if __name__=='__main__':
    # writes assets/banner-light.svg and assets/banner-dark.svg (needs the Latin Modern fonts from TeX Live)
    import os
    out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets')
    for th in THEMES:
        s=build(th); open(os.path.join(out,f'banner-{th}.svg'),'w').write(s); print(th,len(s)//1024,'KB')
