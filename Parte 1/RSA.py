from GeradorDePrimos import geracaoDePrimos
import random
import math
import sympy
import hashlib
import os
class RSA:
    def _init_(self):
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
    """
        Entrada:
            Mensagem a ser criptografada
            Chave pública
            Funções de Hash
        Saída:
            Mensagem Codificada em OAEP
    """
    def OAEPEncode(self, message:str):
        sha1=hashlib.sha1
        # Preencher a mensagem com zeros
        messageEmBytes = message.encode(encoding='utf-8')
        tamanhoModulo, _ = self.public
        tamanhoDoModuloEmBits = tamanhoModulo.bit_length() // 8
        # Padding da mensagem incluí: 0x00 na primeira posição, 0x01 na segunda posição
        padding = b"\x00\x01"
        tamanhoDoPadding = tamanhoDoModuloEmBits-len(padding)-len(message)
        if tamanhoDoPadding < 0:
            print("Tamanho excedente!")
            return
        padding += os.urandom(tamanhoDoPadding) # Aleatoriedade pro padding 
        dados = padding+messageEmBytes # Concatenação do padding e a mensagem em claro
        # Geração do vetor de salto ou seed
        tamanhoDoHash = 20 # Utilizando SHA-1
        seedAleatoria = os.urandom(20)
        dadosHash = sha1(dados).digest()
        seedHash = sha1(seedAleatoria).digest()
        # 1° Aplicação do XOR: Dados x HashSeed
        dadosXORhashSeed = [a^b for a, b in zip(dados, seedHash)]
        # 2° Aplicação do XOR: seed x DadosHash
        dadosXORhashDados = [a^b for a, b in zip(seedAleatoria, dadosHash)]
        return bytes(dadosXORhashSeed+ dadosXORhashDados)


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
        print(plaintextCodificadoOAEPBytes)
        return self.OAEPDecode(plaintextCodificadoOAEPBytes)

    """
        Entrada:
            Mensagem que acabou de passar por descriptografia RSA.
            As funções de hash.
            Chave pública do RSA.
    """
    def OAEPDecode(self,):
        pass

        
        


rsa = RSA()    
print(rsa.OAEPEncode("Bruno"))