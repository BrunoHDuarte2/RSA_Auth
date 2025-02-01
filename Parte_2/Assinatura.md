# PARTE 2 | Assinatura

A assinatura digital RSA é um método criptográfico que utiliza o algoritmo RSA para garantir a autenticidade e integridade de uma mensagem ou documento. Nesse processo, o remetente utiliza sua chave privada para gerar uma assinatura única baseada no conteúdo da mensagem. O destinatário, por sua vez, pode verificar essa assinatura utilizando a chave pública correspondente, assegurando que a mensagem não foi alterada e que realmente provém do remetente alegado.

Como representado na figura a seguir:

![Diagrama da Assinatura RSA](../Diagrama_assinatura.png)

## Etapas da Implementação

1. **M (Mensagem Original):**
    - No código, a mensagem original é passada como argumento para as funções `gerar_hash`, `assinar_msg` e `verificar_ass`.

2. **H(M) (Hash da Mensagem):**
    - No código, o hash da mensagem é gerado na função `gerar_hash`.
    - `hash_mensagem = self.gerar_hash(mensagem)`
    - O hash é uma representação única e compacta da mensagem, gerada por uma função criptográfica (como SHA-3-256).

3. **PRa*Ra* (Chave Privada para Criptografar o Hash):**
    - No código, a chave privada é usada na função `RSACriptografa` para criptografar o hash da mensagem.
    - `assinatura_msg = self.rsa.RSACriptografa(hash_mensagem)`
    - **Matematicamente**, a criptografia com a chave privada no RSA é feita usando a fórmula:

        ```math
        assinatura: S = H(M)^d \mod n
        ```

        Onde:

        - \( H(M) \): Hash da mensagem.
        - \( d \): Expoente da chave privada.
        - \( n \): Módulo RSA (produto de dois números primos grandes).

4. **E(PRa*Ra*, H(M)) (Assinatura Digital):**
    - No código, a assinatura digital é gerada ao criptografar o hash da mensagem com a chave privada.
    -  `assinatura_msg = self.rsa.RSACriptografa(hash_mensagem)`
    - A assinatura é então codificada em Base64 para facilitar o armazenamento e transmissão: `assinatura_msg_base64 = base64.b64encode(assinatura_msg)`.
    - **Matematicamente**, a assinatura é o resultado da operação de criptografia com a chave privada, como descrito acima.

5. **PU_a (Chave Pública para Verificar a Assinatura):**
    - No código, a chave pública é usada na função `RSADescriptografa` para descriptografar a assinatura e recuperar o hash original.
    - `hash_recuperado = self.rsa.RSADescriptografa(assinaturaEmBytes)`
    - **Matematicamente**, a descriptografia com a chave pública no RSA é feita usando a fórmula:

        ```math
        \text{hash\_recuperado} = \text{assinatura}^e \mod n
        ```

        Onde:

        - \( \text{assinatura} \): Assinatura digital.
        - \( e \): Expoente da chave pública.
        - \( n \): Módulo RSA (o mesmo usado na criptografia).

6. **D (Verificação da Assinatura):**
    - No código, a verificação da assinatura é feita na função `verificar_ass`.
    - O hash da mensagem recebida é comparado com o hash recuperado da assinatura descriptografada.
    - `if hash_msg == hash_recuperado: print('Assinatura válida!')`.
    - **Matematicamente**, a verificação é bem-sucedida se:

        ```math
        H(M) = \text{hash\_recuperado}
        ```

        Isso confirma que a assinatura foi gerada com a chave privada correspondente à chave pública usada para descriptografar.

## Bibliotecas Utilizadas

Para implementar as funcionalidades descritas, foram utilizadas as seguintes bibliotecas:

1. **`hashlib`:** Esta biblioteca fornece uma interface comum para diversos algoritmos de hash seguros e funções de resumo de mensagem. Inclui algoritmos como SHA-1, SHA-224, SHA-256, SHA-384, SHA-512 e SHA-3, além do MD5. No contexto do código apresentado, o `hashlib` é utilizado para gerar o hash SHA-3-256 da mensagem, que serve como uma "impressão digital" única do conteúdo.

2. **`base64`:** Esta biblioteca oferece funções para codificar e decodificar dados binários em representações ASCII, como Base64. No código, é utilizada para codificar a assinatura gerada em Base64, facilitando sua transmissão e armazenamento, já que a codificação Base64 converte dados binários em uma string de caracteres ASCII.

## Implementação em Python

```python
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
    hash_mensagem = self.gerar_hash(mensagem)
    
    # Criptografa o hash da mensagem utilizando a chave privada do RSA
    assinatura_msg = self.rsa.RSACriptografa(hash_mensagem)  # Retorna a assinatura em formato de bytes
    
    # Codifica a assinatura em Base64 para facilitar o armazenamento e transmissão
    assinatura_msg_base64 = base64.b64encode(assinatura_msg)
    
    # Retorna a assinatura codificada em Base64 e a mensagem original
    return assinatura_msg_base64, mensagem

# Função para verificar a assinatura de uma mensagem
def verificar_ass(self, assinatura_base64, mensangem):
    # Gera o hash da mensagem recebida utilizando a função gerar_hash
    hash_msg = self.gerar_hash(mensangem)
    
    # Decodifica a assinatura de Base64 para bytes
    assinaturaEmBytes = base64.b64decode(assinatura_base64)
    
    # Descriptografa a assinatura utilizando a chave pública do RSA para recuperar o hash original
    hash_recuperado = self.rsa.RSADescriptografa(assinaturaEmBytes)  # Retorna o hash recuperado em formato de bytes
    
    # Compara o hash da mensagem recebida com o hash recuperado da assinatura
    if hash_msg == hash_recuperado:
        print('Assinatura válida!')  # Se os hashes forem iguais, a assinatura é válida
    else:
        print("Assinatura inválida!")  # Se os hashes forem diferentes, a assinatura é inválida

