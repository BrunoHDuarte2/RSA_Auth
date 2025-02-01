# Documentação da Implementação RSA

## Visão Geral
Este documento descreve a implementação de um sistema de criptografia RSA em Python, que inclui a geração de chaves, criptografia e descriptografia de mensagens utilizando o esquema de padding OAEP (Optimal Asymmetric Encryption Padding). A implementação também suporta a escrita e leitura de chaves em formato PEM.

## Dependências
O código utiliza as seguintes bibliotecas:
- `random`: Gera números aleatórios.
- `math`: Funções matemáticas.
- `sympy`: Cálculo do inverso modular.
- `hashlib`: Funções hash.
- `base64`: Codifica e decodifica chaves em base64.
- `os`: Gera bytes aleatórios para o padding OAEP.
- `GeradorDePrimos`: Módulo externo para geração de números primos de 1024 bits.

## Estrutura da Classe `RSA`
A classe `RSA` implementa um sistema completo de criptografia RSA com as seguintes funcionalidades:

### Inicialização
```python
 def __init__(self):
     self.public, self.private = self.geraChaves()
```
Gera um par de chaves RSA ao inicializar uma instância da classe.

### Geração de Chaves
```python
 def geraChaves(self):
```
1. Gera dois números primos `p` e `q` com 1024 bits.
2. Calcula $n = p q$ e $\varphi(n) = (p-1)(q-1)$.
3. Escolhe `e` tal que $mdc(e, \varphi(n)) = 1$.
4. Calcula $ed = 1 (\mod \varphi(n))$.
5. Escreve as chaves em formato PEM.

### Formato PEM
As chaves pública e privada são salvas no formato OpenSSL PEM, contendo dados codificados em base64:
```plaintext
-----BEGIN RSA PRIVATE KEY-----
(Base64)
-----END RSA PRIVATE KEY-----
```

### Codificação e Decodificação OAEP
A implementação segue o paper de Yutong Zhong, usando `SHA-256` para as funções `G` e `H`.

**Codificação:**
```python
 def OAEPEncode(self, message: str):
```
1. Adiciona padding para garantir tamanho fixo.
2. Gera um valor aleatório `r`.
3. Aplica `G(r)` e `H(X)`.
4. Aplica `XOR` para obter `X` e `Y`.

**Decodificação:**
```python
 def OAEPDecode(self, encoded_message: bytes):
```
1. Separa `X` e `Y`.
2. Calcula `r` e `m_padded`.
3. Remove padding e retorna a mensagem original.

### Criptografia e Descriptografia
**Criptografia:**
```python
 def RSACriptografa(self, plaintext:str):
```
1. Codifica a mensagem com OAEP.
2. Converte para inteiro.
3. Calcula $ciphertext = mensagem^e (\mod n )$.
4. Retorna o texto cifrado em bytes.

**Descriptografia:**
```python
 def RSADescriptografa(self, ciphertext):
```
1. Converte `ciphertext` para inteiro.
2. Calcula $plaintext = ciphertext^d (\mod n)$.
3. Decodifica com OAEP e retorna a mensagem original.

## Exemplo de Uso
```python
 rsa = RSA()
 mensagem_original = "TESTE DE FUNCIONALIDADE"
 mensagem_cifrada = rsa.RSACriptografa(mensagem_original)
 mensagem_decifrada = rsa.RSADescriptografa(mensagem_cifrada)
 print(mensagem_decifrada)  # Deve imprimir "TESTE DE FUNCIONALIDADE"
```

