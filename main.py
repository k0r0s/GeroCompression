import rulehound as rh 
import str2bin as sb

def main_with_iconfig():
    msg = []
    my_string = "Hello World"
    print("Original string: {}\n".format(my_string))
    encoding = "utf-8"
    oct_arr = sb.str_to_bin(my_string, encoding)
    print("Encoded UTF-8 : {}\n".format(oct_arr))
    for byte in oct_arr:
        (iconfig, rule, steps) = rh.seek_rule(byte, 100, default_config = False, fix_steps = True)
        print("rule: {},\t steps: {},\t iconfig: {}".format(rule,steps,iconfig))
        char = rh.expand_rule(rule, 8, steps, iconfig)
        msg.append(char)
    print("\nDecoded UTF-8 message: {}".format(msg))

if __name__ == "__main__":
    main_with_iconfig()
