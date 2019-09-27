from PIL import Image

"""
CHANGELOG

1.02:
Size ratio for RGB is 1:root(8)
Size ratio for RGBA is 1:root(6)

When the base image is RGB, it can only hold 3 bits of injection per pixel.
When converted to RGBA, it can now hold 4 bits of injection per pixel.
This makes injection pixel to output pixels ratio 1:6 as opposed to
1:8 if base image was RGB

Because RGBA uses alpha (transparency) to store 1 extra bit, information
can be lost if the output is handled incorrectly ie. saving it in mspaint

tl;dr I can now store the same amount of information as before in a smaller image

1.03:
Pixel ratio for RGB is 1:8
Pixel ratio for RGBA is 1:6

Pictures don't need to be square or exactly 1:root(whatever) anymore. Wew.
As long as the base image can fit all the injection bits, either pictures can be any shape
"""


base = Image.open("base.png").convert("RGBA")
injection = Image.open("injection.png").convert("RGB")
baseimg = base.load()
injimg = injection.load()

injbits = injection.size[0] * injection.size[1] * 24
basebits = base.size[0] * base.size[1] * 4
injdata = []

if (injbits > basebits):
    print("The injection image is too large large (", injbits, '/', basebits)
    input()
    exit()

print("Bits to inject:", injbits)
print("Free space in base image:", basebits)

#Converts the injection image's pixels into binary
for y in range(injection.size[1]):
    for x in range(injection.size[0]):
        for i in range(len(injimg[x, y])):
            #Formats to binary to 8bit
            injdata += list('{0:08b}'.format(injimg[x, y][i]))
            
#Flips data to make poping easier.
injdata = injdata[::-1]

#Dumps the binary equivalent of the injection image to a text file 
index = open("(Delete me) injection_bin.txt", 'w')
index.write(''.join(injdata))
index.close()

print("Injecting")

#Injects binary into base image
index = open("(Delete me) edited_base_pixel_dump.txt", 'w')
for y in range(base.size[1]):
    for x in range(base.size[0]):
        if (len(injdata) > 0):
            temp = []
            for i in range(len(baseimg[0, 0])):
                #Offsets color value by 1 or 0 (whatever is popped off the stack)
                #Special exception for 255 since we can't use 256
                if (baseimg[x, y][i] == 255):
                    temp.append(baseimg[x, y][i] - int(injdata.pop()))
                else:
                    temp.append(baseimg[x, y][i] + int(injdata.pop()))
            baseimg[x, y] = tuple(temp)
            #Dumps the edited color values of the base image to a text file
            index.write(str(baseimg[x, y]) + '\n')
#Break out of both loops when injdata empties            
        else:
            break
    else:
        continue
    break
index.close()
print("All bits injected")

base.save("output.png")

"""
Everything below does exactlty what the extractor does. Just here for ease of testing
"""

print("Testing")

editimg = baseimg
base = Image.open("base.png").convert("RGBA")
baseimg = base.load()

width = injection.size[0]
height = injection.size[1]

output = Image.new("RGB", (width, height))
outimg = output.load()

extdata = []

for y in range(base.size[1]):
    for x in range(base.size[0]):
        if (len(extdata) < injbits):
            for i in range(len(baseimg[0, 0])):
                #Compares color data from the original to the edited image
                #If they are different, that bit is a 1, otherwise it's a 0
                extdata.append(str(int(baseimg[x, y][i] != editimg[x, y][i])))
        else:
            break
    else:
        continue
    break
   
#Stupidly complicated way of splitting a list of numbers into chunks of 8 and converting them to decimal
convdata = [int(''.join(extdata[x:x+8]), 2) for x in range(0, len(extdata), 8)]

#Formats converted values into the color value tuple form (R, G, B)
#Cuts off extra data and flips
newdata = [tuple(convdata[x:x+len(outimg[0, 0])]) for x in range(0, len(convdata), len(outimg[0, 0]))][::-1]
                 
#Dumps the color values of the extracted image to a text file
index = open("(Delete me) output_pixel_dump.txt", 'w')
for x in newdata:
    index.write(" " + str(x) + "\n")
index.close()

for y in range(height):
    for x in range(width):
        outimg[x, y] = newdata.pop()

output.save("(Delete me) If This Looks Like The Injection It Worked.png")

print("Done")
input()
