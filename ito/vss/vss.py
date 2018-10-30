# coding:UTF-8

"""
Pillowのサンプルプログラム
"""

from PIL import Image
from random import random


def nega(image, name):
    """
    画像の色を反転する関数
    """
    rgb_im = image.convert("RGB")  # 画像をRGBに変換
    size = rgb_im.size  # 画像のサイズを変数に保存
    new_im = Image.new("RGB", size)  # 同じサイズの新しい画像を作成
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b = rgb_im.getpixel((x, y))  # 画像のrgbを取得
            #  画像のRGB値を反転する
            r = 255-r
            g = 255-g
            b = 255-b
            new_im.putpixel((x, y), (r, g, b, 0))  # 新しい画像にRGB値を与える
    new_im.save("nega_"+name)
    print("make nega")
    return new_im


def gray(image, name):
    """
    画像をグレースケール化する関数
    """
    rgb_im = image.convert("RGB")
    size = rgb_im.size
    new_im = Image.new("RGB", size)
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b = rgb_im.getpixel((x, y))
            g = (r+g+b)//3
            new_im.putpixel((x, y), (g, g, g, 0))
    new_im.save("gray_"+name)
    print("make gray")
    return new_im


def BW(image, name):
    """
    グレースケール画像を二値化する関数
    """
    c = 255//2
    rgb_im = image.convert("RGB")
    size = rgb_im.size
    new_im = Image.new("RGB", size)
    for x in range(size[0]):
        for y in range(size[1]):
            g, g, g = rgb_im.getpixel((x, y))
            if g > c:
                g = 255
            else:
                g = 0
            new_im.putpixel((x, y), (g, g, g, 0))
    new_im.save("b&w_"+name)
    print("make black and white")
    return new_im


def VSS(image, name):
    """
    二値化した画像をVSSとして分離する関数
    """
    rgb_im = image.convert("RGB")
    size = rgb_im.size
    size_origin = size[:]
    size = list(size)
    size[0] *= 2
    size[1] *= 2
    new_a = Image.new("RGB", size)
    new_b = Image.new("RGB", size)
    for x in range(0, size_origin[0]):
        for y in range(0, size_origin[1]):
            r = random()
            g, g, g = rgb_im.getpixel((x, y))
            if g == 0:
                if r < 0.5:
                    new_a.putpixel((2*x, 2*y), (0, 0, 0, 0))
                    new_a.putpixel((2*x+1, 2*y), (255, 255, 255, 0))
                    new_a.putpixel((2*x, 2*y+1), (255, 255, 255, 0))
                    new_a.putpixel((2*x+1, 2*y+1), (0, 0, 0, 0))
                    new_b.putpixel((2*x, 2*y), (255, 255, 255, 0))
                    new_b.putpixel((2*x+1, 2*y), (0, 0, 0, 0))
                    new_b.putpixel((2*x, 2*y+1), (0, 0, 0, 0))
                    new_b.putpixel((2*x+1, 2*y+1), (255, 255, 255, 0))
                else:
                    new_a.putpixel((2*x, 2*y), (255, 255, 255, 0))
                    new_a.putpixel((2*x+1, 2*y), (0, 0, 0, 0))
                    new_a.putpixel((2*x, 2*y+1), (0, 0, 0, 0))
                    new_a.putpixel((2*x+1, 2*y+1), (255, 255, 255, 0))
                    new_b.putpixel((2*x, 2*y), (0, 0, 0, 0))
                    new_b.putpixel((2*x+1, 2*y), (255, 255, 255, 0))
                    new_b.putpixel((2*x, 2*y+1), (255, 255, 255, 0))
                    new_b.putpixel((2*x+1, 2*y+1), (0, 0, 0, 0))

            if g == 255:
                if r < 0.5:
                    new_a.putpixel((2*x, 2*y), (0, 0, 0, 0))
                    new_a.putpixel((2*x+1, 2*y), (255, 255, 255, 0))
                    new_a.putpixel((2*x, 2*y+1), (255, 255, 255, 0))
                    new_a.putpixel((2*x+1, 2*y+1), (0, 0, 0, 0))
                    new_b.putpixel((2*x, 2*y), (0, 0, 0, 0))
                    new_b.putpixel((2*x+1, 2*y), (255, 255, 255, 0))
                    new_b.putpixel((2*x, 2*y+1), (255, 255, 255, 0))
                    new_b.putpixel((2*x+1, 2*y+1), (0, 0, 0, 0))
                else:
                    new_a.putpixel((2*x, 2*y), (255, 255, 255, 0))
                    new_a.putpixel((2*x+1, 2*y), (0, 0, 0, 0))
                    new_a.putpixel((2*x, 2*y+1), (0, 0, 0, 0))
                    new_a.putpixel((2*x+1, 2*y+1), (255, 255, 255, 0))
                    new_b.putpixel((2*x, 2*y), (255, 255, 255, 0))
                    new_b.putpixel((2*x+1, 2*y), (0, 0, 0, 0))
                    new_b.putpixel((2*x, 2*y+1), (0, 0, 0, 0))
                    new_b.putpixel((2*x+1, 2*y+1), (255, 255, 255, 0))
    new_a.save("key_a_"+name)
    new_b.save("key_b_"+name)
    new = [new_a, new_b]
    print("make keys")
    return new


def decode(key_a, key_b, name):
    """
    VSSを復号する関数
    """
    image_a = key_a
    image_b = key_b
    rgb_a = image_a.convert("RGB")
    rgb_b = image_b.convert("RGB")
    size = rgb_a.size
    new_size = list(size[:])
    new_size[0] = new_size[0]//2
    new_size[1] = new_size[1]//2
    new_im = Image.new("RGB", new_size)
    for x in range(new_size[0]):
        for y in range(new_size[1]):
            ga_0, ga_0, ga_0 = rgb_a.getpixel((2*x, 2*y))
            ga_1, ga_1, ga_1 = rgb_a.getpixel((2*x+1, 2*y))
            ga_2, ga_2, ga_2 = rgb_a.getpixel((2*x, 2*y+1))
            ga_3, ga_3, ga_3 = rgb_a.getpixel((2*x+1, 2*y+1))
            gb_0, gb_0, gb_0 = rgb_b.getpixel((2*x, 2*y))
            gb_1, gb_1, gb_1 = rgb_b.getpixel((2*x+1, 2*y))
            gb_2, gb_2, gb_2 = rgb_b.getpixel((2*x, 2*y+1))
            gb_3, gb_3, gb_3 = rgb_b.getpixel((2*x+1, 2*y+1))
            g_0 = (ga_0+gb_0) % 256
            g_1 = (ga_1+gb_1) % 256
            g_2 = (ga_2+gb_2) % 256
            g_3 = (ga_3+gb_3) % 256
            g = (g_0+g_1+g_2+g_3)//4
            g = g//255
            if g == 0:
                new_im.putpixel((x, y), (255, 255, 255, 0))
            else:
                new_im.putpixel((x, y), (0, 0, 0, 0))
    new_im.save(name)
    print("decode")
    return new_im


if __name__ == "__main__":
    iname = input("input_file_name->")
    oname = input("output_file_name->")
    im = Image.open(iname)  # 画像を読み込む
    print(im.format, im.size, im.mode)  # 画像の情報を出力
    nega(im, oname)
    new = gray(im, oname)
    new = BW(new, oname)
    keys = VSS(new, oname)
    result = decode(keys[0], keys[1], oname)
    result.show()
