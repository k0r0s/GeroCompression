import numpy as np
import rulehound as rh


def str_to_bin(strp, encoding):
    byte_array = bytearray(strp, encoding)
    uint8_array = np.array(byte_array, dtype=np.uint8)
    bit_string = []
    for byte in uint8_array:
        char = np.binary_repr(byte, width=8)
        char = [int(bit) for bit in char]
        bit_string.append(char)
    return bit_string

#def str_to_bin(strp, encoding):
#    byte_arr = bytearray(strp, encoding)
#    res = [] 
#    for byte in byte_arr: 
#        bits = []
#        for bit in range(8):
#            bits.append((byte >> bit) & 1)
#        res.append(bits)


