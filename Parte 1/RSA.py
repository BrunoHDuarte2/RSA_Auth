from GeradorDePrimos import geracaoDePrimos
import random
import math
import sympy
import hashlib
import base64
import os
class RSA:
    def __init__(self):
        self.public, self.private = self.geraChaves()
        """
            Formato padrão do OpenSSL em base64.
                -----BEGIN RSA PRIVATE KEY-----
                (Dados em base 64)
                -----END RSA PRIVATE KEY-----
            E o mesmo para chave pública. 
        """
    def encodeLength(self, n):
        if n < 128:
            return bytes([n])
        else:
            length_bytes = n.to_bytes((n.bit_length() + 7) // 8, 'big')
            return bytes([0x80 | len(length_bytes)]) + length_bytes
    def decodeLength(self, data, offset):
        length = data[offset]
        if length & 0x80:  
            num_bytes = length & 0x7F
            length = int.from_bytes(data[offset+1:offset+1+num_bytes], 'big')
            return length, offset + 1 + num_bytes
        return length, offset + 1
    
    def encode(self, valor):
        b =  valor.to_bytes((valor.bit_length() + 7)//8, 'big')
        if b[0] >= 0x80:
            b = b'\x00' + b
        return b'\x02' + self.encodeLength(len(b)) + b
    def decode(self, data, offset):
        length, offset = self.decodeLength(data, offset + 1)
        value = int.from_bytes(data[offset:offset+length], 'big')
        return value, offset + length
    def toPem(self, der, header, footer):
        b64 = base64.encodebytes(der).decode('ascii')
        b64_lines = ''.join(b64.splitlines(keepends=False))  
        formatted_b64 = '\n'.join([b64_lines[i:i+64] for i in range(0, len(b64_lines), 64)])
        return f"{header}\n{formatted_b64}\n{footer}"
    def escritaPEM(self, moduloN, expoentePublico, expoentePrivado):
        der = b'\x02\x01\x00' + self.encode(moduloN) + self.encode(expoentePublico) + self.encode(expoentePrivado)
        Pr = b'\x30' + self.encodeLength(len(der)) + der
        der = b'\x02\x01\x00' + self.encode(moduloN) + self.encode(expoentePublico) 
        Pb = b'\x30' + self.encodeLength(len(der)) + der
        with open('./Parte 1/keys/privateKey.pem', 'w') as file:
            file.write(self.toPem(Pr, "-----BEGIN RSA PRIVATE KEY-----", "-----END RSA PRIVATE KEY-----"))
        with open('./Parte 1/keys/publicKey.pem', 'w') as file:
            file.write(self.toPem(Pb, "-----BEGIN RSA PUBLIC KEY-----", "-----END RSA PUBLIC KEY-----"))
    @staticmethod
    def getPublicKey(self):
        with open('./Parte 1/keys/publicKey.pem', 'r') as file:
            leitura = file.readlines()
        leitura = leitura[1:-1] # Fatiamento para tirar o primeiro e o ultimo elemento, que no caso são as linhas, logo remove o header e o footer
        publicData = "".join(linha.strip() for linha in leitura)
        publicDataDecoded = base64.b64decode(publicData)
        _, offset = self.decodeLength(publicDataDecoded, 1)  
        _, offset = self.decode(publicDataDecoded, offset)  
        n, offset = self.decode(publicDataDecoded, offset)  
        e, offset = self.decode(publicDataDecoded, offset)  
        return n, e
    @staticmethod
    def getPrivateKey(self):
        with open('./Parte 1/keys/privateKey.pem', 'r') as file:
            leitura = file.readlines()
        leitura = leitura[1:-1] # Fatiamento para tirar o primeiro e o ultimo elemento, que no caso são as linhas, logo remove o header e o footer
        privateData = "".join(linha.strip() for linha in leitura)
        privateDataDecoded = base64.b64decode(privateData)
        _, offset = self.decodeLength(privateDataDecoded, 1)  
        _, offset = self.decode(privateDataDecoded, offset)  
        n, offset = self.decode(privateDataDecoded, offset) 
        e, offset = self.decode(privateDataDecoded, offset) 
        d, offset = self.decode(privateDataDecoded, offset) 
        return n, e, d
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
        # Escrita em arquivos de formato pem.
        self.escritaPEM(n, e, d)
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
n, e =rsa.getPublicKey()
print("Módulo: ", (n.bit_length()))
print("e: ", (e.bit_length()))
n, e, d =rsa.getPrivateKey()
print("Módulo: ", (n.bit_length()))
print("e: ", (e.bit_length()))
print("d: ", (d.bit_length()))