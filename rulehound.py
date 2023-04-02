import cellpylib as cpl 
import numpy as np


def bin_repr_arr(decimal_num,bit_width):
    uint_num = np.uint32(decimal_num)
    uint_bits = np.uint32(bit_width)

    bit_string = np.binary_repr(uint_num, width=uint_bits)
    bit_array = np.array([[int(bit) for bit in bit_string]],dtype = np.int32)
    return bit_array

def seek_rule(final_config,max_steps):
    bitsize = len(final_config)
    for j in range(256): #rules
        iconfig = cpl.init_simple(bitsize,1) #  0 0 0 0 1 0 0 0 0
        ca = cpl.evolve(iconfig, timesteps = max_steps if max_steps != 0 else cpl.until_fixed_point(),\
                        memoize=True, apply_rule=lambda n, c, t: cpl.nks_rule(n,j))
        for k in range(max_steps):
            if (ca[k] == final_config).all():
                print("rule:\t{}[bits: {}],\tstep:\t{}[bits: {}],\tdflt: {}".format(j,j.bit_length(),k,k.bit_length(),iconfig))
                return (j,k)
    print("No rule for this config.")
    return (0,0)




def seek_rule_seed(final_config,max_steps):
    bitsize = len(final_config)
    for i in range(2**bitsize):
        for j in range(256):
            iconfig = bin_repr_arr(i,bitsize) # any config 0 1 0 0 1 1 0 1       
            ca = cpl.evolve(iconfig, timesteps = max_steps, memoize=True, apply_rule=lambda n, c, t: cpl.nks_rule(n,j))
            for k in range(max_steps):
                if (ca[k] == final_config).all():
                    print("rule:\t{}[bits: {}],\tstep:\t{}[bits: {}],\ticonfig:\t{}".format(j,j.bit_length(),k,k.bit_length(),iconfig))
                    return (iconfig, j, k)

def expand_rule(rule, bitsize, ts):
    ca = cpl.init_simple(bitsize,1)
    ca = cpl.evolve(ca, timesteps = 1 + ts, memoize=True, apply_rule = lambda n, c, t: cpl.nks_rule(n, rule))
    carr = int("".join([str(x) for x in ca[-1]]), 2)
    carr = carr.to_bytes((carr.bit_length()+7)//8, 'big').decode()
    return carr

def expand_rule_seed(seed, rule, bitsize, ts):
    ca = seed
    ca = cpl.evolve(seed, timesteps = 1 + ts, memoize=True, apply_rule = lambda n, c, t: cpl.nks_rule(n, rule))
    carr = int("".join([str(x) for x in ca[-1]]), 2)
    carr = carr.to_bytes((carr.bit_length()+7)//8, 'big').decode()
    return carr


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
