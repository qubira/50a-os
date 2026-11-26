import re,base64,sys,os
s=open(sys.argv[1],encoding='utf-8').read()
uris=re.findall(r'data:(image/[a-z+]+);base64,([A-Za-z0-9+/=]+)',s)
print(len(uris))
for i,(t,b) in enumerate(uris):
    ext=t.split('/')[1].replace('jpeg','jpg')
    open(os.path.join(sys.argv[2],f'f{i:03d}.{ext}'),'wb').write(base64.b64decode(b))
