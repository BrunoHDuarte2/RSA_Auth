import hashlib
import base64
from Parte_1.RSA import RSA

# Função para gerar o hash (SHA-3-256) de uma mensagem ou arquivo
class Hash:
    def __init__(self, rsa:RSA):
        self.rsa = rsa
    
    def gerar_hash(self, mensagem):
        if isinstance(mensagem, str) and mensagem.endswith('.txt'):  
            with open(mensagem, 'rb') as f:   
                mensagem = f.read()   
        elif isinstance(mensagem, str):
            mensagem = mensagem.encode(encoding="utf-8")  
        gh = hashlib.sha3_256()
        gh.update(mensagem)
        return gh.digest()
    
    def assinar_msg(self, mensagem):
        hash_mensagem = self.gerar_hash(mensagem)
        assinatura_msg = self.rsa.RSACriptografa(hash_mensagem) #bytes
        assinatura_msg_base64 = base64.b64encode(assinatura_msg)
        return assinatura_msg_base64, mensagem
        
    def verificar_ass(self, assinatura_base64, mensangem):
        hash_msg = self.gerar_hash(mensangem)
        assinaturaEmBytes = base64.b64decode(assinatura_base64)
        hash_recuperado = self.rsa.RSADescriptografa(assinaturaEmBytes) # bytes
        if hash_msg == hash_recuperado:
            print('Assinatura válida!')
        else :
            print("INVÁLIDA")
