from aes import aes_encrypt,aes_decrypt
from PIL import Image
import random
from compare import compare

def lsb_change(x,y):
    x=str(bin(x))
    str1=x[:-1]+y
    str1 = int(str1, base=2)
    return str1

def get_lsb(x):
    x=str(bin(x))
    return x[-1]

def generate_positions(seed,size,w,h):
    random.seed(seed)
    pos=[]
    for _ in range(size):
        x=random.randint(0,w)
        y=random.randint(0,h)
        pos.append((x,y))
    return pos


def embed_sequentially(path,ct):
    image=Image.open(path)
    width,height=image.size
    x=0
    for i in range(width):
        for j in range(height):
            pixel_value = image.getpixel((i, j))
            image.putpixel((i,j),(lsb_change(pixel_value[0],ct[x]),pixel_value[1],pixel_value[2]))
            x+=1
            if(x==len(ct)):
                print(x)
                return image
            
def embed_randomly(path,ct,seed):
    image=Image.open(path)
    width,height=image.size
    x=0
    pos=generate_positions(seed,len(ct),width,height)

    for i in range(len(pos)):

        pixel_value = image.getpixel(pos[i])
        image.putpixel(pos[i],(lsb_change(pixel_value[0],ct[x]),pixel_value[1],pixel_value[2]))
        x+=1
        if(x==len(ct)):
            print(x)
            return image
    
def extract_sequentially(image,size):
    width,height=image.size
    text=""
    x=0
    for i in range(width):
        for j in range(height):
            pixel_value = image.getpixel((i, j))
            text+=get_lsb(pixel_value[0])
            x+=1
            if(x==size):
                return text
            
def extract_randomly(image,size,seed):
    width,height=image.size
    pos=generate_positions(seed,size,width,height)
    text=""
    x=0
    for i in range(len(pos)):
        pixel_value = image.getpixel(pos[i])
        text+=get_lsb(pixel_value[0])
        x+=1
        if(x==size):
            return text


def binary_to_bytes(binary_string):
    decimal_value = int(binary_string, 2)
    num_bytes = (len(binary_string) + 7) // 8    
    byte_data = decimal_value.to_bytes(num_bytes, byteorder='big')
    return byte_data

def main():
    plaintext = input("Enter your message : ")
    key = b"0123456789abcdef"
    image=Image.open("image1.png")
    ciphertext = aes_encrypt(plaintext, key)
    ciphertext_bin=''.join(format(byte,'08b') for byte in ciphertext)
    image=embed_randomly("image1.png",ciphertext_bin,10)
    image.save("embedded_image1.png")
    extracted=extract_randomly(image,len(ciphertext_bin),10)
    extracted_bytes=binary_to_bytes(extracted)
    decrypted=aes_decrypt(extracted_bytes,key)
    print("PlainText:", plaintext)
    print("Ciphertext:", ciphertext_bin)
    print("extracted:",extracted)
    print("decrypted: ",decrypted)

    compare("image1.png","embedded_image1.png")

    



if __name__=="__main__":
    main()
   
    
    
