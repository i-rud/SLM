def string_to_bits(string):
    bits_arr = []
    for c in string:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        bits_arr.extend([int(b) for b in bits])
    return bits_arr

def bits_to_string(bits_arr):
    chars = []
    for b in range(len(bits_arr) // 8):
        byte = bits_arr[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
