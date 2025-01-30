import hashlib 
import base64

 #Transformando a mensagem em bytes e gerando o hash
def g_hash (mensagem):
    mensagem_bytes = mensagem.encode(encoding="utf-8") # transformando em bytes
    gh = hashlib.sha3_256() # criando o objeto hash lib
    gh.update(mensagem_bytes) # recebndo a entrada
    m_hash = gh.hexdigest() # gerando o hash da mensagem no formato hexdecimal
    return m_hash

# Assinatura da mensagem
def ass_msg (m, d, n):
    m_hash = g_hash(m) # Gerando o hash da mensagem H(M)
    m_int = int(m_hash, 16) # transformando hexdecimal em inteiro
    m_ass = pow(m_int, d, n) # gerando a assinatura (M^d mod n)
    return m_ass, m #retorna a mensagem em claro + a mensagem criptografada E(PRa,H(M))

# Formatação da mensagem
def formatacao_base64(m_ass):
    m_ass_bytes = m_ass.to_bytes((m_ass.bit_length() + 7) // 8, byteorder='big') # int p bytes 
    m_ass_base64 = base64.b64encode(m_ass_bytes) # bytes p base64
    print(f'Formatação base64: {m_ass_base64.decode("utf-8")}')
    return m_ass_base64.decode("utf-8")



def verificacao(e, n, m_ass_base64, m):
    hash_mensagem = int(g_hash(m), 16) #gerando o hash da mensagem em claro e transformando em inteiro
    assinatura_bytes = base64.b64decode(m_ass_base64) # transformanto a str base64 em bytes de novo
    assinatura_int = int.from_bytes(assinatura_bytes, byteorder='big')
    hash_recuperado = pow(assinatura_int, e, n)
    if hash_recuperado == hash_mensagem: return True
    else: return False
    

assinatura, mensagem = ass_msg(m, d, n)
m_ass_base64 =  formatacao_base64(assinatura)
print(f'Mensagem em Claro: {mensagem} \nAssinatura: {assinatura}')
print(f'Formato base64: {m_ass_base64}')
if verificacao(e,n,m_ass_base64,m) == True: print('Assinatura validada!')
else: print('Assinatura inválida')


