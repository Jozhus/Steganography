from PIL import Image

edit = Image.open("G:/Users/Jozhus/Documents/Python/Pictures/output.png").convert("RGBA")
editimg = edit.load()
base = Image.open("G:/Users/Jozhus/Documents/Python/Pictures/base.png").convert("RGBA")
baseimg = base.load()

print("Extracted image size")
width = int(input("Width: "))
height = int(input("Height: "))
outbits = width * height * 24
basebits = base.size[0] * base.size[1] * 4

output = Image.new("RGB", (width, height))
outimg = output.load()

extdata = []

if (outbits > basebits):
    print("That size is too large (", outbits, '/', basebits, ')')
    input()
    exit()

print("Diffing")

for y in range(base.size[1]):
    for x in range(base.size[0]):
        if (len(extdata) < outbits):
            for i in range(len(baseimg[0, 0])):
                #Compares color data from the original to the edited image
                #If they are different, that bit is a 1, otherwise it's a 0
                extdata.append(str(int(baseimg[x, y][i] != editimg[x, y][i])))
        else:
            break
    else:
        continue
    break

print("Converting")
      
convdata = [int(''.join(extdata[x:x+8]), 2) for x in range(0, len(extdata), 8)]

newdata = [tuple(convdata[x:x+len(outimg[0, 0])]) for x in range(0, len(convdata), len(outimg[0, 0]))][::-1]

print("Drawing")

for y in range(height):
    for x in range(width):
         outimg[x, y] = newdata.pop()


output.save("G:/Users/Jozhus/Documents/Python/Pictures/Original.png")

print("Done")
print("If the image has black bars, change the height")
print("If the image is messed up, change the width")
input()
