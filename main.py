from Parte_1.RSA import RSA
from Parte_2_3.Parte_2_3 import Hash
import base64
import sys
rsa = RSA()
hash = Hash(rsa)
mensagemEntrada = "Mensagem de teste para entrada da assinatura!"
print("-----------------------------")
print("Mensagem de entrada: "+mensagemEntrada)
mLinha, m =(hash.assinar_msg(mensagemEntrada))
print("-----------------------------")
print("Assinatura: ", mLinha)
print("-----------------------------")
print("Utilizando essa assinatura e a mensagem original, pode-se validar se a assinatura realmente se refere a aquela mensagem")
hash.verificar_ass(mLinha, m)
print("-----------------------------")
print("Ao tentar utilizar algo diferente da assinatura correta:")
hash.verificar_ass(base64.b64encode(bytes("ASSINATURAERRADA", 'utf-8')), m)


