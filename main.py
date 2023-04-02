import rulehound as rh 
import str2bin as sb

def main_no_iconfig():
    msg = []
    my_string = "Hello World"
    print("original string: {}\n".format(my_string))
    encoding = "utf-8"
    oct_arr = sb.str_to_bin(my_string, encoding)
    print("encoded utf-8: {}\n".format(oct_arr))
    for byte in oct_arr:
        (rule, steps) = rh.seek_rule(byte, 300)
        char = rh.expand_rule(rule, 8,steps)
        msg.append(char)
    print(msg)

def main_with_iconfig():
    msg = []
    my_string = "Hello World"
    print("original string: {}\n".format(my_string))
    encoding = "utf-8"
    oct_arr = str_to_bin(my_string, encoding)
    print("Encoded UTF-8 : {}\n".format(oct_arr))
    for byte in oct_arr:
       # (rule, steps) = rh.seek_rule(byte, 1000)
        (iconfig, rule, steps) = rh.seek_rule_seed(byte, 100)
        char = rh.expand_rule_seed(iconfig, rule, 8,steps)
        msg.append(char)
    print("\nDecoded UTF-8 message: {}".format(msg))

if __name__ == "__main__":
    main_no_iconfig()
