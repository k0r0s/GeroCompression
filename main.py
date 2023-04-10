import codecs 
import rulehound as rh 
import str2bin as sb

def main_with_iconfig():
    msg = []
    #my_string = "var s = ' !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~';"
    my_string = "Hello World"
    #my_string = "A"
    print("Original string: {}\n".format(my_string))
    encoding  = "utf-16"
    charwidth = sb.get_encoding_width(encoding) 
    oct_arr = sb.str_to_bin(my_string, encoding)
    print("Encoded UTF-16 :")
    for char in oct_arr:
        print(char,hex(sb.binarr_to_int([char])))
    print("\n")

    for byte in oct_arr:
        (iconfig, rule, steps) = rh.seek_rule(byte, 50, default_config = False, fix_steps = True)
        istr = sb.binarr_to_int(iconfig)
        print("rule: {} [{}],\t steps: {},\t iconfig: {}[{}], \t total bits [{}]".format(rule,rule.bit_length(), steps,iconfig, istr.bit_length(), istr.bit_length() + rule.bit_length()))
        char = rh.expand_rule(rule, charwidth, encoding, steps, iconfig)
        msg.append(char)

    msg = b''.join(msg)
    bom = codecs.BOM_UTF16_LE
    assert msg.startswith(bom)
    msg = msg[len(bom):]
    print("\nDecoded UTF-16 message: {}".format(msg.decode("utf-16")))

if __name__ == "__main__":
    main_with_iconfig()
