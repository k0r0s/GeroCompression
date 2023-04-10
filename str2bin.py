import numpy as np
import rulehound as rh


def get_encoding_width(encoding):
    """Returns the width in bits of a given encoding"""
    if encoding.lower() == 'utf-8':
        return 8
    elif encoding.lower() == 'utf-16':
        return 16
    elif encoding.lower() == 'utf-32':
        return 32
    else:
        # Assume single-byte encoding with 8 bits per character
        return 8
def binarr_to_int(cell_arr):
    return int("".join([str(x) for x in cell_arr[-1]]), 2)

def str_to_bin(strp, encoding):
    byte_array = bytearray(strp, encoding)
    uint8_array = np.array(byte_array, dtype=np.uint8)
    bit_string = []
    for byte in uint8_array:
        char = np.binary_repr(byte, width=get_encoding_width(encoding))
        char = [int(bit) for bit in char]
        bit_string.append(char)
    return bit_string

def decimal_to_encoding(decimal_value, encoding):
    """Converts a decimal integer to its encoding"""
    if decimal_value < 0 or decimal_value > 0x10FFFF:
        raise ValueError('Decimal value out of range for encoding')
    if encoding.lower() == 'utf-8':
        if decimal_value <= 0x7F:
            return bytes([decimal_value])
        elif decimal_value <= 0x7FF:
            return bytes([0xC0 | (decimal_value >> 6), 0x80 | (decimal_value & 0x3F)])
        elif decimal_value <= 0xFFFF:
            return bytes([0xE0 | (decimal_value >> 12), 0x80 | ((decimal_value >> 6) & 0x3F), 0x80 | (decimal_value & 0x3F)])
        else:
            return bytes([0xF0 | (decimal_value >> 18), 0x80 | ((decimal_value >> 12) & 0x3F), 0x80 | ((decimal_value >> 6) & 0x3F), 0x80 | (decimal_value & 0x3F)])
    elif encoding.lower() == 'utf-16':
        if decimal_value <= 0xFFFF:
            return decimal_value.to_bytes(2, byteorder='big')
        else:
            code_point = decimal_value - 0x10000
            high_surrogate = 0xD800 + (code_point >> 10)
            low_surrogate = 0xDC00 + (code_point & 0x3FF)
            return high_surrogate.to_bytes(2, byteorder='big') + low_surrogate.to_bytes(2, byteorder='big')
    elif encoding.lower() == 'utf-32':
        return decimal_value.to_bytes(4, byteorder='big')
    else:
        raise ValueError('Unsupported encoding')

if __name__ == "__main__":
    a = get_encoding_width("utf-16")
    print(a)
