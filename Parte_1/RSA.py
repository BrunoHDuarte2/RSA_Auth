from Parte_1.GeradorDePrimos import geracaoDePrimos
import random
import math
import sympy
import hashlib
import base64
import os
class RSA:
    def __init__(self):
        # Tenta ler o arquivo, caso não dê certo gera uma exceção
        try:
            # Se a tentativa de leitura de qualquer um dos dois der errado, isso irá gerar um exceção
            with open('./Parte_1/keys/privateKey.pem', 'r') as file:
                PrK = file.readlines()
            with open('./Parte_1/keys/publicKey.pem', 'r') as file:
                PbK = file.readlines()
            self.public = self.getPublicKey()
            n, e, d = self.getPrivateKey()
            self.private = (n, d)
        except:
            # Caso onde o arquivo não existe
            # O gerachave cria o arquivo se precisar
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
        with open('./Parte_1/keys/privateKey.pem', 'w') as file:
            file.write(self.toPem(Pr, "-----BEGIN RSA PRIVATE KEY-----", "-----END RSA PRIVATE KEY-----"))
        with open('./Parte_1/keys/publicKey.pem', 'w') as file:
            file.write(self.toPem(Pb, "-----BEGIN RSA PUBLIC KEY-----", "-----END RSA PUBLIC KEY-----"))
    
    def getPublicKey(self):
        with open('./Parte_1/keys/publicKey.pem', 'r') as file:
            leitura = file.readlines()
        leitura = leitura[1:-1] # Fatiamento para tirar o primeiro e o ultimo elemento, que no caso são as linhas, logo remove o header e o footer
        publicData = "".join(linha.strip() for linha in leitura)
        publicDataDecoded = base64.b64decode(publicData)
        _, offset = self.decodeLength(publicDataDecoded, 1)  
        _, offset = self.decode(publicDataDecoded, offset)  
        n, offset = self.decode(publicDataDecoded, offset)  
        e, offset = self.decode(publicDataDecoded, offset)  
        return n, e
    
    def getPrivateKey(self):
        with open('./Parte_1/keys/privateKey.pem', 'r') as file:
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
        Seguindo o algoritmo descrito no paper do Yutong Zhong
        Parametros e operações necessárias:
            n: tamanho em bits do modulo RSA
            k0 e k1: numeros definidos pelo protocolo OAEP
            m: plaintext com tamanho n - k0 - k1 bits
            G e H: funções criptograficas de hash
            XOR
            r: string randomica gerada de k0 bits
    """
    def OAEPEncode(self, message):
        n, _ = self.public
        n = (n.bit_length()+7) // 8  # Tamanho de n em bytes
        k0 = 256 // 8  # Tamanho do hash em bytes
        
        padding_length = n - k0 - len(message)
        m_padded = message + b'\x00' * padding_length  
        
        r = os.urandom(k0)  
        G = hashlib.sha256
        H = hashlib.sha256
        G_r = G(r).digest()
        X = bytes([a^b for a, b in zip(m_padded, G_r)])
        
        H_X = H(X).digest()
        
        Y = bytes([a^b for a, b in zip(r, H_X)])
        
        return X + Y
    
    def RSACriptografa(self, plaintext):
        (n, d) = self.private
        messageCodificada = self.OAEPEncode(plaintext)
        if messageCodificada == None:
            return "ERRO NO TAMANHO DA MENSAGEM"
        # Pega a mensagem, que está em bytes, segundo o retorno do OAEP, e transforma em int
        mensagemEmInteiros = int.from_bytes(messageCodificada, byteorder='big')
        ciphertext = pow(mensagemEmInteiros, d, n) # ciphertext = mensagemEmInteiros^e (mod n)
        return ciphertext.to_bytes((ciphertext.bit_length()+7)//8, byteorder='big') 
    def RSADescriptografa(self, ciphertext):
        (n, e) = self.public
        chipertextEmInteiros = int.from_bytes(ciphertext, byteorder='big')
        plaintextCodificadoOAEP = pow(chipertextEmInteiros, e, n) # plaintext = ciphertextEmInteiros^d (mod n)
        plaintextCodificadoOAEPBytes = plaintextCodificadoOAEP.to_bytes((plaintextCodificadoOAEP.bit_length()+7)//8, byteorder='big')
        return self.OAEPDecode(plaintextCodificadoOAEPBytes)

    """
        Entrada:
            Mensagem que acabou de passar por descriptografia RSA.
            As funções de hash.
            Chave pública do RSA.
    """
    def OAEPDecode(self, encoded_message: bytes):
        n, _ = self.public
        n = (n.bit_length()+7) // 8  # Tamanho de n em bytes
        
        
        X = encoded_message[:32]
        Y = encoded_message[32:]
        
        G = hashlib.sha256
        H = hashlib.sha256
        H_X = H(X).digest()
        r = bytes([a^b for a,b in zip(Y, H_X)])
        G_r = G(r).digest()
        
        m_padded = bytes([a^b for a,b in zip(X, G_r)])
        message = m_padded.rstrip(b'\x00')
        return message
    
