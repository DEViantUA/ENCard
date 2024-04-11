from PIL import ImageFont,Image,ImageDraw
from pathlib import Path
from io import BytesIO
from collections import namedtuple
from math import sqrt

import PIL
import aiohttp,re,random


assets = Path(__file__).parent.parent / 'assets'
font_ttf = str(assets / 'font' / 'Genshin_Impact.ttf')

async def get_font(size):
    return ImageFont.truetype(font_ttf, size)


async def get_dowload_img(link,size = None, thumbnail_size = None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                image = await response.read()
    except:
        raise
    
    try:
        image = Image.open(BytesIO(image)).convert("RGBA")
    except PIL.UnidentifiedImageError:
        print(f"Error: UnidentifiedImageError, {link}")
        raise
    
    if size:
        return image.resize(size)
    elif thumbnail_size:
        image.thumbnail(thumbnail_size)
        return image
    else:
        return image



async def create_image_with_text(text, font_size, max_width = 336, color = (255,255,255,255)):
    # Определяем шрифт изображения
    font = await get_font(font_size)
    # Получаем ширину и высоту изображения на основе размеров текста
    lines = []
    line = []
    for word in text.split():
        if line:
            temp_line = line + [word]
            temp_text = ' '.join(temp_line)
            temp_width = font.getmask(temp_text).getbbox()[2]
            if temp_width <= max_width:
                line = temp_line
            else:
                lines.append(line)
                line = [word]
        else:
            line = [word]
    if line:
        lines.append(line)

    width = 0
    height = 0
    for line in lines:
        line_width = font.getmask(' '.join(line)).getbbox()[2]
        width = max(width, line_width)
        height += font.getmask(' '.join(line)).getbbox()[3]

    # Создаем изображение с белым фоном и размерами, подходящими для текста
    img = Image.new('RGBA', (min(width, max_width), height+(font_size-4)), color= (255,255,255,0))

    # Накладываем текст на изображение
    draw = ImageDraw.Draw(img)
    y_text = 0
    for line in lines:
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        draw.text((0, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height+5
    
    return img


async def get_user_image(img):
    if type(img) != str:
        img = img
    elif type(img) == str:
        linkImg = re.search("(?P<url>https?://[^\s]+)", img)
        if linkImg:
            img = await get_dowload_img(linkImg.group())
        else:
            img = Image.open(img)
    else:
        return None
    return img.convert("RGBA")


async def get_resize_image(userImages,baseheight,basewidth):
    x,y = userImages.size
    if max(x, y) / min(x, y) < 1.1:
        hpercent = (baseheight / float (y)) 
        wsize = int ((float (x) * float (hpercent)))
        userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
        return {"img": userImages, "type": 0}
    elif x > y:
        hpercent = (baseheight / float (y)) 
        wsize = int ((float (x) * float (hpercent)))
        userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
        return {"img": userImages, "type": 1}
    else:
        wpercent = (basewidth / float(userImages.size[0]))
        hsize = int((float(userImages.size[1]) * float(wpercent)))
        userImages = userImages.resize((basewidth, hsize), Image.LANCZOS)
        if hsize < baseheight:
            hpercent = (baseheight / float (y)) 
            wsize = int ((float (x) * float (hpercent)))
            userImages = userImages.resize ((wsize, baseheight), Image.LANCZOS)
            return {"img": userImages, "type": 2}
        return {"img": userImages, "type": 2}
    

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(img, n=3):
    img = img.copy()
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break
    
    return clusters


async def get_color(img):
    a = colorz(img, n = 2)
    a = list(a)[0].lstrip('#')
    color_palette = list(int(a[i:i+2], 16) for i in (0, 2, 4))
    if color_palette[0]> 209:
        color_palette[0] = 209
    if color_palette[1]> 209:
        color_palette[1] = 209
    if color_palette[1]> 209:
        color_palette[1] = 209
    return tuple(color_palette)