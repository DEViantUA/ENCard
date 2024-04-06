from PIL import ImageFont,Image,ImageDraw
from pathlib import Path
from io import BytesIO
from collections import namedtuple
from math import sqrt

import aiohttp,re,random


assets = Path(__file__).parent.parent / 'assets'
font_ttf = str(assets / 'font' / 'Genshin_Impact.ttf')

async def get_font(size):
    return ImageFont.truetype(font_ttf, size)



async def create_image_with_text(text, font_size, max_width=336, color=(255, 255, 255, 255), alg="Left"):    
    font = await get_font(font_size)

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

    img = Image.new('RGBA', (min(width, max_width), height + (font_size)), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(img)
    
    y_text = 0
    for line_num, line in enumerate(lines):
        text_width, text_height = font.getmask(' '.join(line)).getbbox()[2:]
        if alg == "center" and line_num > 0:
            x_text = (max_width - text_width) // 2
        else:
            x_text = 0
        draw.text((x_text, y_text), ' '.join(line), font=font, fill=color)
        y_text += text_height + 5
            
    return img


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





# Copyright 2024 DEViantUa <t.me/deviant_ua>
# All rights reserved.
from PIL import Image,ImageFilter, ImageDraw
from more_itertools import chunked
import numpy as np
import colorsys
import json
from cachetools import TTLCache

def get_element_color(element):
    if element == "Fire":
        return (255,45,37,255) 
    elif element== "Grass":
        return (0,255,93,255) 
    elif element == "Electric":
        return (156,38,255,255) 
    elif element == "Water":
        return (0,184,255,255) 
    elif element == "Wind":
        return (0,255,196,255) 
    elif element== "Rock":
        return (255,139,23,255) 
    else:
        return (0,255,251,255) 
    
cache = TTLCache(maxsize=1000, ttl=300)  

async def recolor_image(image, target_color, light = False):
    if light:
        ll = await light_level(target_color)
        if ll < 45:
            target_color = await _get_light_pixel_color(target_color,up = True)
            
    result = Image.new('RGBA', image.size, target_color)
    
    if image.mode == 'RGBA':
        result.putalpha(image.split()[-1])
    
    return result


async def get_dowload_img(link,size = None, thumbnail_size = None):
    cache_key = json.dumps((link, size, thumbnail_size), sort_keys=True)
        
    if cache_key in cache:
        return cache[cache_key]
    headers_p = {}
    try:
        if "pximg" in link:
            headers_p = {
                "referer": "https://www.pixiv.net/",
            }
        async with aiohttp.ClientSession(headers=headers_p) as session, session.get(link) as r:
            try:
                image = await r.read()
            finally:
                await session.close()
    except:
        raise
    
    image = Image.open(BytesIO(image)).convert("RGBA")
    
    if size:
        image = image.resize(size)
        cache[cache_key] = image
        return image
    elif thumbnail_size:
        image.thumbnail(thumbnail_size)
        cache[cache_key] = image
        return image
    else:
        cache[cache_key] = image
        return image

async def apply_opacity(image, opacity=0.2):
    result_image = image.copy()
    alpha = result_image.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    result_image.putalpha(alpha)

    return result_image

async def light_level(pixel_color):   
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3])) 
    return l

def color_distance(color1, color2):
    return sum((a - b) ** 2 for a, b in zip(color1, color2)) ** 0.5

async def replace_color(image, old_color, new_color, radius=100):
    image = image.convert("RGBA")
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            current_color = pixels[x, y][:3]
            if color_distance(current_color, old_color) <= radius:
                pixels[x, y] = (*new_color, pixels[x, y][3])
    
    return image


async def _get_light_pixel_color(pixel_color, up = False):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    if up:
        l = min(max(0.6, l), 0.9)
    else:
        l = min(max(0.3, l), 0.8)
    return tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
  
async def _get_dark_pixel_color(pixel_color):
    h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in pixel_color[:3]))
    l = min(max(0.8, l), 0.2)
    a = tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s))
    
    return  a


async def get_average_color(image):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    channels = image.split()
    
    return (
        round(np.average(channels[0], weights=channels[-1])),
        round(np.average(channels[1], weights=channels[-1])),
        round(np.average(channels[2], weights=channels[-1])),
    )


async def get_dominant_colors(
    image,
    number,
    *,
    dither=Image.Quantize.FASTOCTREE,
    common=True,
):
    if image.mode != 'RGB':
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        if not common:
            width = image.width
            height = image.height
            
            image = Image.fromarray(np.array([np.repeat(
                np.reshape(image.convert('RGB'), (width * height, 3)),
                np.reshape(image.split()[-1], width * height),
                0,
            )]), 'RGB')
    
    if image.mode == 'RGBA':
        if dither == Image.Quantize.FASTOCTREE:
            simple_image = image.copy()
            simple_image.putalpha(255)
        else:
            simple_image = image.convert('RGB')
    else:
        simple_image = image
    
    reduced = simple_image.quantize(dither=dither, colors=number)
    
    palette = [*chunked(reduced.getpalette(), 3)]
    
    if common and image.mode == 'RGBA':
        alpha = np.array(image.split()[-1])
        
        colors = sorted((
            (
                np.sum(alpha * reduced.point([0] * i + [1] + [0] * (255 - i))),
                tuple(palette[i]),
            )
            for _, i in reduced.getcolors()
        ), reverse=True)
    else:
        colors = [
            (n, tuple(palette[i]))
            for n, i in sorted(reduced.getcolors(), reverse=True)
        ]
    
    return tuple(colors)


async def get_distance_alpha(image, converter=(lambda x: x)):
    width = image.width
    height = image.height
    
    radius = np.hypot(1, 1)
    
    return Image.fromarray(np.fromfunction(
        lambda y, x: np.uint8(255 * converter(np.hypot(
            2 * x / (width - 1) - 1,
            2 * y / (height - 1) - 1,
        ) / radius)),
        (height, width),
    ), 'L')


async def get_background_alpha(image):
    return await get_distance_alpha(
        image,
        lambda x: x * np.sin(x * np.pi / 2),
    )


async def get_foreground_alpha(image):
    return await get_distance_alpha(
        image,
        lambda x: 1 - x * np.sin(x * np.pi / 2),
    )

async def get_colors(image,number,*,common=False,radius=1,quality=None):
    if quality is not None:
        image = image.copy()
        image.thumbnail((quality, quality), 0)
    
    if radius > 1:
        image = image.filter(ImageFilter.BoxBlur(radius))
    
    filtered_image = image.convert('RGB')
    
    if image.mode != 'RGBA':
        filtered_image.putalpha(await get_background_alpha(image))
    else:
        filtered_image.putalpha(Image.fromarray(np.uint8(
            np.uint16(await get_background_alpha(image))
            * image.split()[-1]
            / 255
        ), 'L'))
    
    color_palette = await get_dominant_colors(filtered_image, number, common=common)
    color_palette = color_palette[0][1]
    ll = await light_level(color_palette)
    if ll < 0.15:
        color_palette = await _get_light_pixel_color(color_palette)
    elif ll > 0.80:
        color_palette = await _get_dark_pixel_color(color_palette)
        
        
    return color_palette


async def get_centr_size(size, file_name): #get_centr_honkai_art
    background_image = Image.new('RGBA', size, color=(0, 0, 0, 0))
    foreground_image = file_name.convert("RGBA")

    scale = max(size[0] / foreground_image.size[0], size[1] / foreground_image.size[1])
    foreground_image = foreground_image.resize((int(foreground_image.size[0] * scale), int(foreground_image.size[1] * scale)))

    background_size = background_image.size
    foreground_size = foreground_image.size

    x = background_size[0] // 2 - foreground_size[0] // 2

    if foreground_size[1] > background_size[1]:
        y_offset = max(int(0.3 * (foreground_size[1] - background_size[1])), int(0.5 * (-foreground_size[1])))
        y = -y_offset
    else:
        y = background_size[1] // 2 - foreground_size[1] // 2

    background_image.alpha_composite(foreground_image, (x, y))

    return background_image