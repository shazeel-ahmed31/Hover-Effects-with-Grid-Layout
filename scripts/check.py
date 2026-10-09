from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
root=Path(__file__).resolve().parents[1]
class Check(HTMLParser):
 def __init__(self):super().__init__();self.cards=0;self.errors=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='article':
   self.cards+=1
   if a.get('tabindex')!='0':self.errors.append('Card is not keyboard focusable')
  if tag=='img' and not a.get('alt'):self.errors.append('Missing image alternative')
  for key in ['src','href']:
   value=a.get(key,'');url=urlsplit(value)
   if value and not url.scheme and url.path and not (root/unquote(url.path)).is_file():self.errors.append('Missing local asset: '+value)
for name in ['index.html','Task9.html']:
 parser=Check();parser.feed((root/name).read_text(encoding='utf-8'));assert parser.cards==6;assert not parser.errors,parser.errors
assert (root/'index.html').read_bytes()==(root/'Task9.html').read_bytes()
print('Both entry pages, six accessible cards and local assets checked.')
