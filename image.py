from PIL import Image
from struct import pack, unpack_from
import RunLength

class Coordinate():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.buffer1 = 0

    def getNextCoordinate(self, width, height):
        if self.buffer1 == 0:
            self.buffer1 = 1
            return 1
        else:
            next_x = self.x
            next_y = self.y
            next_x += 1
            if next_x >= width:
                next_x = 0
                next_y += 1

            if next_y >= height:
                return 0

            self.x = next_x
            self.y = next_y

            return 1

def encodeImage(image):
    width = image.width
    height = image.height
    datasize = width * height
    data = []

    coordinate = Coordinate()

    while coordinate.getNextCoordinate(width, height):
        x = coordinate.x
        y = coordinate.y
        r,g,b = image.getpixel((x,y))
        data.append(r)

    encode_data = RunLength.encode_RLE(data)

    return encode_data

def decodeImage(image_data):
    processPtr = 0
    identifer = image_data[:4]
    width = unpack_from('I', image_data, 4)[0]
    height = unpack_from('I', image_data, 8)[0]

    processPtr += 4 + 4 + 4
    print('{}, {}, {}'.format(identifer, width, height))

    out = Image.new('RGBA', (width, height))
    coordinate = Coordinate()

    while 1:
        if processPtr == len(image_data):
            break
        length = unpack_from('B', image_data, processPtr)[0]
        processPtr += 1
        if length == None:
            break
        code = unpack_from('B', image_data, processPtr)[0]
        processPtr += 1

        r = code
        g = code
        b = code

        for i in range(length):
            if coordinate.getNextCoordinate(width, height) == 0:
                print('ERROR')
                return 0
            x = coordinate.x
            y = coordinate.y
            out.putpixel((x,y),(r,g,b,0))

    out.show()
    return 1

if __name__ == '__main__':
    #img = Image.open('/Users/akyo/compress/color/Lenna.bmp', 'r')

    out_img = open('/Users/akyo/compress/out','rb')

    #data = encodeImage(img.convert('RGB'))

    #identifer = pack('<4s',b'RLE1')
    #width = pack('<I',img.width)
    #height = pack('<I',img.height)

    #out_img.write(identifer + width + height + data)
    data = out_img.read()
    decodeImage(data)

