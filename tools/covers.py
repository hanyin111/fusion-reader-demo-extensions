from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
if len(sys.argv) != 2:
    raise SystemExit('Usage: python tools/covers.py <local-font-file>')
font_path = Path(sys.argv[1])
if not font_path.is_file(): raise SystemExit('The supplied local font does not exist.')
out = root / 'public/covers'
out.mkdir(parents=True, exist_ok=True)
for index, (key, title) in enumerate([('letter', '山间来信'), ('paper', '纸上旅行'), ('morning', '晨光札记')]):
    background = [(229, 221, 239), (222, 232, 229), (240, 228, 211)][index]
    color = [(98, 69, 128), (57, 98, 83), (135, 94, 54)][index]
    image = Image.new('RGB', (480, 680), background)
    draw = ImageDraw.Draw(image)
    draw.rectangle((32, 32, 448, 648), outline=color, width=2)
    draw.text((60, 80), title[:2], font=ImageFont.truetype(str(font_path), 72), fill=color)
    draw.text((60, 166), title[2:], font=ImageFont.truetype(str(font_path), 72), fill=color)
    draw.line((64, 292, 170, 292), fill=color, width=3)
    draw.text((64, 322), '原创阅读演示', font=ImageFont.truetype(str(font_path), 23), fill=color)
    for step in range(3):
        y = 460 + step * 32
        draw.arc((64 - step * 15, y, 420 + step * 20, y + 130), 190, 350, fill=color, width=3)
    draw.text((64, 587), '聚阅 · 三章短篇', font=ImageFont.truetype(str(font_path), 18), fill=color)
    image.save(out / f'{key}.png', optimize=True)
print('Created three original cover illustrations.')
