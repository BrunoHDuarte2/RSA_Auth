from GeradorDePrimos import geracaoDePrimos
import random
import math
import sympy
def geraChaves():
    # Para gerar chaves RSA primeiro se escolhe randomicamente p e q
    p = geracaoDePrimos(1024)
    q = geracaoDePrimos(1024)
    # Dessa forma pode-se obter n
    n = p*q
    # Phi(n) pode ser quebrado como Phi(p)*Phi(q) já que n pode ser fatorado como p*q
    # Além disso, Phi de um número primo é somente o número menos 1.
    # Logo: Phi(n) =  (p-1)*(q-1)
    phi_n = (p-1)*(q-1)
    # Para gerar e, tal que 1<e<Phi(n) e mdc(e, Phi(n)) = 1:
    while True:
        e = random.randint(2, phi_n-1) # Os limites estão como 2 e Phi(n)-1 pois o randint inclui os limites
        if math.gcd(e, phi_n) == 1:
            break
    # Agora para achar d, tal que d*e é congruente a 1 (mod Phi(n))
    d = sympy.mod_inverse(e, phi_n)
    # Retorna a chave pública e a chave privada.
    return (n, e), (n, d)
c1, c2 = geraChaves()
print(c1)
print(c2)