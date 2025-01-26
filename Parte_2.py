import hashlib 
import base64

 #Transformando a mensagem em bytes e gerando o hash
def g_hash (mensagem):
    mensagem_bytes = mensagem.encode(encoding="utf-8") # transformando em bytes
    gh = hashlib.sha3_512() # criando o objeto hash lib
    gh.update(mensagem_bytes) # recebndo a entrada
    m_hash = gh.hexdigest() # gerando o hash da mensagem no formato hexdecimal
    return m_hash

# Assinatura da mensagem
def ass_msg (m, d, n):
    m_hash = g_hash(m) # Gerando o hash da mensagem H(M)
    m_int = int(m_hash, 16) # transformando hexdecimal em inteiro
    m_ass = pow(m_int, d, n) # gerando a assinatura (M^d mod n)
    return m_ass

# Formatação da mensagem
def formatacao_base64(m_ass):
    m_ass_bytes = m_ass.to_bytes((m_ass.bit_length() + 7) // 8, byteorder='big') # int p bytes 
    m_ass_base64 = base64.b64encode(m_ass_bytes) # bytes p base64
    m_ass_base64_str = m_ass_base64.decode('utf-8') # transforma de base64 em string para ficar mais legível
    return m_ass_base64_str   

d = 123456789
n = 987654321
m = "GeeksForGeeks"

print(ass_msg(m, d, n))
print(formatacao_base64(ass_msg(m, d, n)))
