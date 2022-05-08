from operator import le
from .utils import *
from copy import copy
from .keygen import KeyGen

class Injector:
    @staticmethod
    def extract_message_into_image(image, message):
        SEED = '5d41402abc4b2a76b9719d911017c592'
        key = KeyGen.generate_key(SEED)

        result_image = copy(image)
        current_w = 0
        current_h = key[0]
        current_step_i = 0
        current_step = key[current_step_i]
        
        for message_iterator in range(0, len(message)):
            current_pixel = image[current_w][current_h]
            current_bit = current_pixel[2] % 2

            bit_to_insert = message[message_iterator]

            if current_bit != bit_to_insert:
                diff = 1 if current_bit == 0 else -1
                final_value = current_pixel[2] + diff

                buf_lst = list(current_pixel)
                buf_lst[2] = final_value

                current_pixel = tuple(buf_lst)
                result_image[current_w][current_h] = current_pixel
            
            current_step_i += 1
            current_step = key[current_step_i % len(key)]

            current_h += current_step
            if current_h >= len(image):
                current_h %= len(image)
                current_w += 1
        
        return result_image

    @staticmethod
    def pull_out_message_from_image(image) -> list:
        SEED = '5d41402abc4b2a76b9719d911017c592'
        key = KeyGen.generate_key(SEED)

        current_w = 0
        current_h = key[0]
        current_step_i = 0
        current_step = key[current_step_i]

        message = []
        length_buf = []
        
        bits_decrypted = 0
        message_length = 0
        allow_to_read = False
        
        while True:
            current_pixel = image[current_w][current_h]
            current_bit = current_pixel[2] % 2

            if allow_to_read == True:
                message.append(current_bit)
                bits_decrypted += 1
            else:
                length_buf.append(current_bit)
                length_str = bits_to_string(length_buf)
                if length_str.find('<|') != -1 and length_str.find('|>') != -1:
                    length_str = length_str.replace('<|', '').replace('|>', '')
                    if length_str == '0':
                        return "NO MESSAGE"
                    message_length = int(length_str) * 8
                    allow_to_read = True
            
            current_step_i += 1
            current_step = key[current_step_i % len(key)]

            current_h += current_step
            if current_h >= len(image):
                current_h %= len(image)
                current_w += 1

            if bits_decrypted == message_length and allow_to_read:
                break

        return bits_to_string(message)
    

    
   