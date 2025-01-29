import base64


def formatacao_base64(m_ass):
    m_ass_bytes = m_ass.to_bytes((m_ass.bit_length() + 7) // 8, byteorder='big') # int p bytes 
    m_ass_base64 = base64.b64encode(m_ass_bytes) # bytes p base64
    m_ass_base64_str = m_ass_base64.decode('utf-8') # transforma de base64 em string para ficar mais legível
    return m_ass_base64_str 

def desformatacao_base64(m_ass_base64_str):

    m_ass_bytes = base64.b64decode(m_ass_base64_str)  # Decodifica de Base64 para bytes
    m_ass = int.from_bytes(m_ass_bytes, byteorder='big')  # Converte de bytes para inteiro
    return m_ass

teste = 14021998

print(formatacao_base64(teste))
print(desformatacao_base64(formatacao_base64(teste)))