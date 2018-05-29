from struct import pack, unpack_from

RUN_LIMIT = 0xff

def encode_RLE(data):
    encode_data = b''
    processPtr = 0

    while processPtr < len(data) - 1:   #-1する意味がよくわかってないけどこれでうまくいく
        code = data[processPtr]
        run,processPtr = getRunLength(data, processPtr, code )
        encode_data += pack('B', run) + pack('B',code)

    return encode_data

def encode_PackBits(data):
    encode_data = b''
    processPtr = 0
    while processPtr < len(data) - 1:
        codePtr = processPtr
        run, processPtr, mode = getPacBits(data, processPtr)
        if mode:
            encode_data += pack('b', -run) + pack('>'+str(run)+'s',data[codePtr:processPtr])
        else:
            encode_data += pack('b', run) + pack('B', data[codePtr])

    return encode_data

def encode_srle(data):
    encode_data = b''
    processPtr = 0
    mode = 0
    while processPtr < len(data) - 1:
        basePtr = processPtr
        run, processPtr, en_mode = getPacBits(data,processPtr)
        if mode == 0:
            mode = 1
            if en_mode == 1:
                encode_data += pack('B', 0)
                processPtr = basePtr
                continue
            encode_data += pack('B', run) + pack('B', data[basePtr])
        else:
            mode = 0
            if en_mode == 0:
                encode_data += pack('B', 0)
                processPtr = basePtr
                continue
            encode_data += pack('B', run) + pack('>'+str(run)+'s',data[basePtr:processPtr])

    return encode_data

def decode_RLE(data):
    decode_data = b''
    it = iter(data)

    for code, run in zip(it, it):
        decode_data += pack('B',code) * run

    return decode_data

def decode_PackBits(data):
    decode_data = b''
    processPtr = 0

    while processPtr < len(data) - 1:
        run = unpack_from('b', data, processPtr)[0]
        processPtr += 1
        if run < 0:
            run = abs(run)
            decode_data += pack('>' + str(run) + 's', data[processPtr:processPtr+run])
            processPtr += run
        else:
            decode_data += pack('B', data[processPtr]) * run
            processPtr += 1

    return decode_data

def decode_srle(data):
    decode_data = b''
    processPtr = 0
    mode = 0

    while processPtr < len(data) - 1:
        run = unpack_from('B', data, processPtr)[0]
        processPtr += 1
        if run == 0:
            mode ^= 1
            continue
        if mode == 1:
            decode_data += pack('>' + str(run) + 's', data[processPtr:processPtr+run])
            processPtr += run
            mode = 0
        else:
            decode_data += pack('B', data[processPtr]) * run
            processPtr += 1
            mode = 1

    return decode_data

def getRunLength(data, processPtr, code):
    run = 0

    while processPtr < len(data) and code == data[processPtr] and run < 0xff :
        processPtr += 1
        run += 1

    return (run,processPtr)

def getPacBits(data, processPtr):
    run = 0
    code = data[processPtr]
    processPtr += 1
    run += 1

    if code == data[processPtr]:
        en_mode = 0
        while processPtr < len(data) and code == data[processPtr] and run < RUN_LIMIT:
            code = data[processPtr]
            processPtr += 1
            run += 1
    else:
        en_mode = 1
        while processPtr < len(data) and code != data[processPtr] and run < RUN_LIMIT:
            code = data[processPtr]
            processPtr += 1
            run += 1

        if processPtr != len(data):
            processPtr -= 1
            run -= 1
    return (run, processPtr, en_mode)

if __name__ == '__main__':
    filename = '/Users/akyo/compress/testfile'
    fp = open(filename,'rb')
    data = fp.read()
    encode_data = encode_srle(data)
    fp.close()
    print(data)
    print(encode_data)
    decode_data = decode_srle(encode_data)
    print(decode_data)
    #wfp = open('/Users/akyo/compress/out','wb')
    #wfp.write(decode_data)

