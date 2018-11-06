from PIL import Image

def embed(img,filename):
    img.convert("RGB")
    eimg = Image.open("sample.png")
    esize = eimg.size
    eimg.convert("LA")
    eimg.point(lambda x: 0 if x < 230 else x)
    wcnt = img.size[0] // 100
    hcnt = img.size[1] // 100
    new_img = Image.new("RGB",img.size,(255,255,255))
    for i in range(wcnt):
        for j in range(hcnt):
            new_img.paste(eimg,(i*esize[0],j*esize[1]))
    new_img2 = Image.new("RGB",(2*img.size[0],2*img.size[1]))
    for i in range(2*img.size[0]):
        for j in range(2*img.size[1]):
            if i%2==1:
                new_img2.putpixel((i,j),img.getpixel((i//2,j//2)))
            else:
                new_img2.putpixel((i,j),new_img.getpixel((i//2,j//2)))
    filename = "new_"+filename
    new_img2.save(filename)

filename = input("ファイル名を入力してください")
img = Image.open(filename)
embed(img,filename)