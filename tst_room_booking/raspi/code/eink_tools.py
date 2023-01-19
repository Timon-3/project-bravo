# Here are all the functions, to simplify the eInk Design process
import qrcode # pip install qrcode[pil]
from PIL import Image,ImageDraw,ImageFont

# 
def add_icon(icon_img,size=36):
    ic_im = Image.open(icon_img)
    ic_im = ic_im.resize((size,size))
    return ic_im



# Create and add QR Code
def add_qrcode(qr_code_text,size=90):
    qr_img=qrcode.make(qr_code_text)
    qr_img = qr_img.resize((size,size))
    return qr_img

def centre_image():
    return 2
def centre_text(text=""):
    return text


def create_image(size, message, font, fontColor):
    W, H = size
    image = Image.new('RGB', size)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    draw.text(((W-w)/2, (H-h)/2), message, font=font, fill=fontColor)
    return image

W, H = (300,200)
msg = "hello"

im = Image.new("RGBA",(W,H),"yellow")
draw = ImageDraw.Draw(im)
w, h = draw.textsize(msg)
draw.text(((W-w)/2,(H-h)/2), msg, fill="black")

im.save("hello.png", "PNG")