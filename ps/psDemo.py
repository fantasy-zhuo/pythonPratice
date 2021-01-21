from removebg import RemoveBg
from PIL import Image
import re

# changebg: 调用PIL添加背景颜色
def changebg(img, color):
    imgName = re.findall(re.compile(r'(.*?)_no_bg.png') , img)[0]
    color_dict = {"A": (255, 0, 0), "B": (67, 142, 219), "C": (255, 255, 255)}  # A:red B:bule C:white D:justremovebg
    im = Image.open(img)
    x, y = im.size
    try:
        p = Image.new('RGBA', im.size, color=color_dict.get(color))
        p.paste(im, (0, 0, x, y), im)
        p.save('{}.png'.format(imgName + '_' + color))
    except:
        print('changebg err')
        pass


rmbg = RemoveBg("UiwiP9dQj53v693md9UyEyZz", "../error.log")

# 获取单个照片的抠图   XKMh1J7geGfnGY9CFu9zXV8f
imgPath = 'Penguins.jpg'
rmbg.remove_background_from_img_file(imgPath)  # 图片地址
option = 'B'  # 蓝色
changebg(imgPath + '_no_bg.png', option)