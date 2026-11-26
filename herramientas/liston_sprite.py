from PIL import Image
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/liston')
orig=Image.open('frames/f000.png').convert('RGBA')
comp=Image.new('RGBA',(1536,1300),(0,0,0,0)); comp.paste(orig,(0,100),orig)
comp.resize((960,812),Image.LANCZOS).save('lazo-quieto.webp',quality=88,method=6)
def ritmo(u):
    s=u*u*(3-2*u); return s+.33*s*(1-s)
N,C,R=56,8,7; W,H=480,406
sheet=Image.new('RGBA',(W*C,H*R),(0,0,0,0))
for k in range(N):
    p=ritmo(k/(N-1))
    im=comp if k==0 else Image.open(f'frames/f{1+round(p*216):03d}.webp').convert('RGBA')
    sheet.paste(im.resize((W,H),Image.LANCZOS),((k%C)*W,(k//C)*H))
sheet.save('lazo-desata.webp',quality=80,method=6)
print(os.path.getsize('lazo-quieto.webp'),os.path.getsize('lazo-desata.webp'),sheet.size)
