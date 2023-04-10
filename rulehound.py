import cellpylib as cpl 
import numpy as np
import str2bin as sb

def bin_repr_arr(decimal_num,bit_width):
    uint_num = np.uint32(decimal_num)
    uint_bits = np.uint32(bit_width)

    bit_string = np.binary_repr(uint_num, width=uint_bits)
    bit_array = np.array([[int(bit) for bit in bit_string]],dtype = np.int32)
    return bit_array

def seek_rule(final_config, steps, default_config = True, fix_steps = False):
    # opt 0: DEF_CONFIG_TRUE, FIXED_STEPS_FALSE
    # opt 1: DEF_CONFIG_TRUE, FIXED_STEPS_TRUE
    # opt 2: DEF_CONFIG_FALSE, FIXED_STEPS_FALSE
    # opt 3: DEF_CONFIG_FALSE, FIXED_STEPS_TRUE

    if (default_config == True):
        if (fix_steps == False):
            opt = 0
        else: 
            opt = 1
    else: 
        if (fix_steps == False):
            opt = 2
        else:
            opt = 3
    
    bitsize = len(final_config)
    match opt:
        case 0:
            iconfig = cpl.init_simple(bitsize,1)
            for j in range(256):
                ca = cpl.evolve(iconfig, timesteps = steps if steps != 0 else cpl.until_fixed_point,\
                                memoize = True, apply_rule = lambda n, c, t: cpl.nks_rule(n,j))
                for k in range(steps):
                    if (ca[k] == final_config).all():
                        return (iconfig,j,k + 1) #rule and step where matched
            print("No configuration found for byte: {}.\n".format(final_config))
            return (iconfig, 0, steps) # no match found within given range

        case 1: 
            iconfig = cpl.init_simple(bitsize, 1)
            for j in range(256):
                ca = cpl.evolve(iconfig, timesteps = steps, memoize = True, apply_rule = lambda n, c, t: cpl.nks_rule(n,j))
                if (ca[-1] == final_config).all():
                    return (iconfig,j,steps) # rule and number of steps fixed
                else:
                    print("No configuration found.\n")
                    return (iconfig, 0, steps) #no match found within given range
        case 2: 
            for i in range(2**bitsize):
                iconfig = bin_repr_arr(i,bitsize) 
                for j in range(256):
                    ca = cpl.evolve(iconfig, timesteps = steps, memoize=True, apply_rule=lambda n, c, t: cpl.nks_rule(n,j))
                    for k in range(steps):
                        if (ca[k] == final_config).all():
                            return (iconfig, j, k+1) 
            return (iconfig, 0, 0)
        case 3: 
            for i in range(2**bitsize):
                iconfig = bin_repr_arr(i,bitsize) 
                for j in range(256):
                    ca = cpl.evolve(iconfig, timesteps = steps, memoize=True, apply_rule=lambda n, c, t: cpl.nks_rule(n,j))
                    if (ca[-1] == final_config).all():
                        return (iconfig, j, steps)
            print("No configuration found.\n")
            return (iconfig,0, steps)
            

def expand_rule(rule, bitsize, encoding, steps, seed=None):
    if seed is None:
        seed = cpl.init_simple(bitsize, 1)

    ca = cpl.evolve(seed, timesteps = steps, memoize = True, apply_rule = lambda n, c, t: cpl.nks_rule(n, rule))
    int_char = sb.binarr_to_int(ca) 
    encoded_char = sb.decimal_to_encoding(int_char, encoding)
    # encoded_char = carr.to_bytes((carr.bit_length()+7)//8, 'big').decode(encoding)
    # TO CHANGE create a function to support utf-16/32
    return encoded_char

 

def main():
    fconfig = np.array([0,0,0,0,1,0,0,1],dtype=np.int32)
    (iconfig,rule) = seek_rule_seed(fconfig, 100)
    print("final configuration was: {}".format(fconfig))
    print("initial config: {}, rule: {}".format(iconfig,rule))
    print("-------- testing ----------")
    ca = iconfig
    ca = cpl.evolve(ca, timesteps = 100, memoize = True, apply_rule = lambda n, c, t: cpl.nks_rule(n,rule))
    print(ca)
    expand_rule(rule,len(fconfig),100)


if __name__ == "__main__":
    main()
