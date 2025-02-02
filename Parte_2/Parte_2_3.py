import hashlib
import base64
from Parte_1.RSA import RSA

# Função para gerar o hash (SHA-3-256) de uma mensagem ou arquivo
class Hash:
    def __init__(self, rsa:RSA):
        self.rsa = rsa
    
    # Função para gerar o hash de uma mensagem
def gerar_hash(self, mensagem):
    # Verifica se a mensagem é um arquivo de texto
    if isinstance(mensagem, str) and mensagem.endswith('.txt'):  
        # Abre o arquivo em modo binário ('rb') e lê todo o conteúdo
        with open(mensagem, 'rb') as f:
            mensagem = f.read()  # Armazena o conteúdo completo do arquivo
    elif isinstance(mensagem, str):  # Verifica se a mensagem é uma string
        mensagem = mensagem.encode(encoding="utf-8")  # Converte a string para bytes usando a codificação UTF-8

    # Cria um objeto de hash utilizando o algoritmo SHA3-256
    gh = hashlib.sha3_256()  
    # Atualiza o objeto de hash com o conteúdo da mensagem
    gh.update(mensagem)  
    # Retorna o hash gerado em formato binário (bytes)
    return gh.digest()
    
    # Função para assinar uma mensagem
def assinar_msg(self, mensagem):
    # Gera o hash da mensagem utilizando a função gerar_hash
    hash_mensagem = self.gerar_hash(mensagem) # H(M)
    
    # Criptografa o hash da mensagem utilizando a chave privada do RSA
    assinatura_msg = self.rsa.RSACriptografa(hash_mensagem)  # Retorna a assinatura em formato de bytes
    
    # Codifica a assinatura em Base64 para facilitar o armazenamento e transmissão
    assinatura_msg_base64 = base64.b64encode(assinatura_msg)
    
    # Retorna a assinatura codificada em Base64 e a mensagem original
    return assinatura_msg_base64, mensagem

# Função para verificar a assinatura de uma mensagem
def verificar_ass(self, assinatura_base64, mensangem):
    # Gera o hash da mensagem recebida utilizando a função gerar_hash
    hash_msg = self.gerar_hash(mensangem) #H(M)
    
    # Decodifica a assinatura de Base64 para bytes
    assinaturaEmBytes = base64.b64decode(assinatura_base64)
    
    # Descriptografa a assinatura utilizando a chave pública do RSA para recuperar o hash original
    hash_recuperado = self.rsa.RSADescriptografa(assinaturaEmBytes)  # Retorna o hash recuperado em formato de bytes
    
    # Compara o hash da mensagem recebida com o hash recuperado da assinatura
    if hash_msg == hash_recuperado:
        print('Assinatura válida!')  # Se os hashes forem iguais, a assinatura é válida
    else:
        print("Assinatura inválida!")  # Se os hashes forem diferentes, a assinatura é inválida
