# Pasta de Chaves

Esta pasta contém as chaves necessárias para o funcionamento seguro do sistema. As chaves são utilizadas para criptografia e assinatura de dados, garantindo a integridade e a confidencialidade das informações.

## Estrutura da Pasta

- **privateKey.pem**: Contém a chave privada RSA. Esta chave deve ser mantida em segredo e utilizada para a descriptografia de mensagens e assinatura de dados.
- **publicKey.pem**: Contém a chave pública RSA. Esta chave pode ser compartilhada livremente e é usada para a criptografia de mensagens e verificação de assinaturas.


### Geração das Chaves

As chaves são geradas automaticamente quando a aplicação é iniciada, caso as chaves não existam. O processo de geração inclui:

1. Geração de um par de chaves RSA (pública e privada).
2. Armazenamento das chaves em arquivos PEM na pasta `keys`.


