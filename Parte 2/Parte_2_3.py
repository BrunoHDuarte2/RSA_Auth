import hashlib
import base64

# Função para gerar o hash (SHA-3-256) de uma mensagem ou arquivo
def g_hash(mensagem):
    if isinstance(mensagem, str) and mensagem.endswith('.txt'):  # 
        with open(mensagem, 'rb') as f:  # 
            mensagem = f.read()  # 
    elif isinstance(mensagem, str):
        mensagem = mensagem.encode(encoding="utf-8")  #
    
    gh = hashlib.sha3_256()
    gh.update(m)
    hash_mensagem = gh.hexdigest()  
    return hash_mensagem

# Função para assinar a mensagem ou arquivo (usando RSA)
def assinar_msg(mensagem, d, n):
    hash_mensagem = g_hash(mensagem)  # Gerando o hash da mensagem ou conteúdo do arquivo H(M)
    int_msg = int(hash_mensagem, 16)  # Convertendo o hash hexadecimal em inteiro
    assinatura_msg = pow(int_msg, d, n)  # Gerando a assinatura (M^d mod n)
    return assinatura_msg, mensagem  # Retorna a assinatura(int) e a mensagem original

def formatar_base64(assinatura_msg):
    num_bytes = (assinatura_msg.bit_length() + 7) // 8  # Tamanho do módulo n em bytes
    assinatura_bytes = assinatura_msg.to_bytes(num_bytes, byteorder='big')  # int para bytes com o tamanho correto
    assinatura_base64 = base64.b64encode(assinatura_bytes)
    return assinatura_base64

