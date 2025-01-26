import hashlib 
import base64

 #Transformando a mensagem em bytes e gerando o hash
def g_hash (mensagem):
    mensagem_bytes = mensagem.encode(encoding="utf-8")
    gh = hashlib.sha3_512() 
    gh.update(mensagem_bytes) 
    m_hash = gh.hexdigest()
    return m_hash

# Assinatura da mensagem
def ass_msg (m, d, n):
    m_hash = g_hash(m)
    m_int = int(m_hash, 16)
    m_ass = pow(m_int, d, n)
    return m_ass

def formatacao_base64(m_ass):
    m_ass_bytes = m_ass.to_bytes((m_ass.bit_length() + 7) // 8, byteorder='big')
    m_ass_base64 = base64.b64encode(m_ass_bytes)
    m_ass_base64_str = m_ass_base64.decode('utf-8')
    return m_ass_base64_str   

d = 123456789
n = 987654321
m = "GeeksForGeeks"

print(ass_msg(m, d, n))
print(formatacao_base64(ass_msg(m, d, n)))
