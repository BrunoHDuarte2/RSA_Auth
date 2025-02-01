# Projeto de Segurança Computacional

O projeto tem como objetivo implementar um sistema de assinaturas digitais e sua validação por meio RSA-OAEP.

## Dependencias e o .exe
Caso queira executar o arquivo [main.py](main.py) você pode executar o arquivo ou seu executável. Caso use o arquivo, ele depende das seguintes bibliotecas:

1. random
2. math
3. sympy
4. hashlib
5. base64
6. os

Sendo necessário instalar somente o sympy, por meio de:
```
pip install sympy
```

Caso use o executável basta usar no terminal:
```
.\dist\main\main.exe
```
Esse arquivo é somente um exemplo de uso da assinatura, para entender o processo em cada pasta há arquivos '.md' com explicações sobre os algoritmos utilizados. Logo, visite:

1. [MillerRabin](Parte_1/MillerRabin.md)
2. [RSA](Parte_1/RSA.md)
3. [Assinatura](Parte_2/Assinatura.md)