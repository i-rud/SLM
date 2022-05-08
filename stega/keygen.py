import random

class KeyGen:
    @staticmethod
    def generate_key(seed):
        random.seed(seed)
        key_length = random.randint(1, 5)
        key = []

        for _ in range(key_length):
            key.append(random.randint(1, 10))
        
        return key