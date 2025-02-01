import random
# Teste de Miller-Rabin
# Dado um número inteiro, verificar se ele é primo.
"""
    Lógica:
        Baseado no Pequeno Teorema de Fermat, no qual diz que
        a congruência: a^(n-1) ≡ 1 (mod n) vale para todo a primo.
        A partir disso é possível se notar que a^(n-1) -1 é divisivel por n

"""
def millerRabin(n:int , k:int):
    # Escrever n-1 como 2^i * m
    nMenos1 =  n-1
    expoente = 0
    while (nMenos1 % 2) == 0:
        # Enquanto a divisão inteira por 2 de n-1 resultar em um valor par...
        nMenos1 = nMenos1 >> 1
        expoente+=1
    m = nMenos1
    e = expoente
    # Dados "m" e o "e": n-1 pode ser escrito como (2^e)*m
    # Sorteando a tq 1<a<n-1
    for i in range(k):
        a = random.randint(2, n-2)
        if not testeDeMiller(a, n, e, m):
            return False
    return True
def testeDeMiller(base, numero, expoente, m):
    x = pow(base, m, numero)
    if x == 1 or x == numero-1:
        return True
    for i in range(expoente-1):
        x = pow(x, 2, numero)
        if x == numero-1:
            return True
    return False