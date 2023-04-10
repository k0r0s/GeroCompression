import rulehound as rh 
import str2bin as sb

def main_with_iconfig():
    msg = []
    #my_string = "var s = ' !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~';"
    #my_string = "Hello World"
    my_string = "AEIO"
    print("Original string: {}\n".format(my_string))
    encoding  = "utf-8"
    charwidth = sb.get_encoding_width(encoding) 
    oct_arr = sb.str_to_bin(my_string, encoding)
    print("Encoded UTF-8 : {}\n".format(oct_arr))
    for byte in oct_arr:
        (iconfig, rule, steps) = rh.seek_rule(byte, 100, default_config = False, fix_steps = False)
        istr = sb.binarr_to_int(iconfig)
        print("rule: {} [{}],\t steps: {},\t iconfig: {}[{}], \t total bits [{}]".format(rule,rule.bit_length(), steps,iconfig, istr.bit_length(), istr.bit_length() + rule.bit_length()))
        char = rh.expand_rule(rule, charwidth, encoding, steps, iconfig)
        msg.append(char)
    print("\nDecoded UTF-8 message: {}".format(msg))

if __name__ == "__main__":
    main_with_iconfig()
