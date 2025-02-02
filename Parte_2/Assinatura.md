# PARTE 2 | Assinatura
### PARTE II | Funções de Hash

Uma função de hash recebe uma mensagem de tamanho variável como entrada e gera um valor de hash de tamanho fixo, H(M). O principal objetivo dessa função é garantir a integridade dos dados, ou seja, verificar se a mensagem não foi alterada, além de assegurar segurança e autenticidade.

Para que uma função de hash seja confiável, ela deve possuir as seguintes propriedades:

- **Propriedade de mão única:** Não é possível descobrir a entrada a partir do hash.
- **Determinística:** A mesma entrada sempre gera o mesmo hash.
- **Eficiência:** O cálculo do hash deve ser rápido.
- **Resistência à colisão:** Entradas diferentes não devem gerar o mesmo hash.
- **Efeito avalanche:** Pequenas alterações na entrada resultam em mudanças drásticas no hash.

No algoritmo RSA, a função de hash desempenha um papel fundamental no processo de assinatura digital:

Conforme ilustrado na imagem acima, é necessária uma função para gerar o hash da mensagem em texto claro antes de assiná-la. Dessa forma, a função de hash será criada para que possa ser utilizada posteriormente na função de assinatura.

> A biblioteca `hashlib` no Python cria marcas únicas (chamadas de hashes) a partir de dados, como textos ou arquivos. Ela aplica algoritmos matemáticos (como SHA-256 ou MD5) para gerar uma sequência única de caracteres que representa os dados de entrada.
>
> **Observação:** Esta biblioteca assegura as cinco propriedades necessárias para um hash seguro citadas acima.

Nesse projeto, para a assinatura, é utilizada a família SHA-3, que emprega a **construção esponja**. Esse método funciona de maneira semelhante a uma esponja: primeiro, ele "absorve" os dados e, depois, os "extrai". Segue abaixo a implementação do código.

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
    
   

