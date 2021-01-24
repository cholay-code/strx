import sys
from PIL import Image

if len(sys.argv) > 2:
    filename = sys.argv[1]
    iconpath = sys.argv[2]
    img = Image.open(filename)
    img.save(iconpath, format='ICO', sizes=[ (64, 64) ])
else:
    print(f'Provide two arguments:\npython3 pngtoico.py <input> <output>')
