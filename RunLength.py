from struct import pack, unpack

def encode(data):
    encode_data = b''
    processPtr = 0

    while processPtr < len(data) - 1:
        code = data[processPtr]
        run,processPtr = getRunLength(data, processPtr, code )
        encode_data += pack('B',code)
        encode_data += pack('B',run)

    return encode_data

def decode(data):
    decode_data = b''
    it = iter(data)

    for code, run in zip(it, it):
        print(code)
        decode_data += pack('B',code) * run

    return decode_data

def getRunLength(data, processPtr, code):
    run = 0

    while processPtr < len(data) and code == data[processPtr] :
        processPtr += 1
        run += 1

    return (run,processPtr)

if __name__ == '__main__':
    filename = '/Users/akyo/compress/testfile'
    fp = open(filename,'rb')
    data = fp.read()
    encode_data = encode(data)
    fp.close()
    wfp = open('/Users/akyo/compress/out','wb')
    print(encode_data)
    decode_data = decode(encode_data)
    wfp.write(decode_data)

