import random
from MillerRabin import millerRabin
def geraNumeroPrimo(bits):
    num = random.getrandbits(bits) # Gera um número de 1024 bits
    num |= (1 << bits - 1)         # OR com 2^1023 o que garante que o bit mais significativo é 1
    num |= 1                       # OR com 1 para garantir que o número é ímpar
    return num
