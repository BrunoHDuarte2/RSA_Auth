from GeradorDePrimos import geracaoDePrimos
import random
import math
import sympy
import hashlib
import os
class RSA:
    def __init__(self):
        self.public, self.private = self.geraChaves()
    def geraChaves(self):
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
    def OAEPEncode(self, message):
        (n, _) = self.public
        hashSHA256 = hashlib.sha256
        tamanhoHash = hashSHA256().digest_size # Aqui pode ser substituido diretamente por 32, dado que 256 bits / 8 = 32
        tamanhoMessage = (n.bit_length() + 7) // 8 # # Tamanho que uma mensagem ocupa em bytes
        # Se o tamanho da mensagem for maior que o espaço disponível - os dois hashs necessários no OAEP (Mascara da mensagem e Mascara do valor aleatório) - o byte de serapação (\x01)
        if len(message) > tamanhoMessage - 2*tamanhoHash-2:
            return None
        maskAleatoria = random.getrandbits(tamanhoHash*8) # Aqui dá pra substituir por 256 pelo mesmo motivo de cima
        # Pega a mensagem, tranforma em bytes, hasheia e pega o valor de hash
        messageHash = hashSHA256(message.encode()).digest()
        hashMaskAleatoria = hashSHA256(maskAleatoria.to_bytes(tamanhoHash,byteorder='big')).digest()
        # tuplaDeBytes agora contém tuplas (messageHash[i], hashMaskAleatoria[i]) 
        tuplaDeBytes = zip(messageHash, hashMaskAleatoria)
        # Usando list comprehension para fazer (messageHash[i] XOR hashMaskAleatoria[i])
        messageMask = bytes([mhash ^ ahash for (mhash, ahash) in tuplaDeBytes])
        # Resultado Final:
        # (hash do valor aleatório XOR hash da mensagem) ++ mensagem original ++ padding
        messageCodificada = messageMask + message.encode() + bytes([0] * (tamanhoMessage - len(message) - len(messageMask) - 1))
        return messageCodificada
    def RSACriptografa(self, plaintext:str):
        (n, e) = self.public
        messageCodificada = self.OAEPEncode(plaintext)
        if messageCodificada == None:
            return "ERRO NO TAMANHO DA MENSAGEM"
        # Pega a mensagem, que está em bytes, segundo o retorno do OAEP, e transforma em int
        mensagemEmInteiros = int.from_bytes(messageCodificada, byteorder='big')
        ciphertext = pow(mensagemEmInteiros, e, n) # ciphertext = mensagemEmInteiros^e (mod n)
        return ciphertext.to_bytes((ciphertext.bit_length()+7)//8, byteorder='big') 
    def RSADescriptografa(self, ciphertext:str):
        (n, d) = self.private
        chipertextEmInteiros = int.from_bytes(ciphertext, byteorder='big')
        plaintextCodificadoOAEP = pow(chipertextEmInteiros, d, n) # plaintext = ciphertextEmInteiros^d (mod n)
        plaintextCodificadoOAEPBytes = plaintextCodificadoOAEP.to_bytes((plaintextCodificadoOAEP.bit_length()+7)//8, byteorder='big')
        return self.OAEPDecode(plaintextCodificadoOAEPBytes)

    def OAEPDecode(self, ciphertext):
        pass
        
