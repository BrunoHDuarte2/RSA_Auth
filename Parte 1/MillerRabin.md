# Teste de Primalidade de Miller-Rabin

## Visão Geral
O teste de Miller-Rabin é um algoritmo probabilístico para verificar se um número é primo. Ele se baseia no Pequeno Teorema de Fermat, que afirma que, para um número primo `n`, a congruência `a^(n-1) ≡ 1 (mod n)` é sempre válida.

O método reescreve `n-1` como `2^e * m`, onde `m` é um número ímpar, e então realiza testes probabilísticos escolhendo bases aleatórias `a` e verificando propriedades de potência modular.

## Implementação 
```python
def millerRabin(n:int , k:int):
    # Escrever n-1 como 2^i * m
    nMenos1 =  n-1
    expoente = 0
    while (nMenos1 % 2) == 0:
        # Enquanto a divisão inteira por 2 de n-1 resultar em um valor par...
        nMenos1 = nMenos1 >> 1
        expoente+=1
    m = nMenos1
    e = expoente
    # Dados "m" e o "e": n-1 pode ser escrito como (2^e)*m
    # Sorteando a tq 1<a<n-1
    for i in range(k):
        a = random.randint(2, n-2)
        if not testeDeMiller(a, n, e, m):
            return False
    return True
def testeDeMiller(base, numero, expoente, m):
    x = pow(base, m, numero)
    if x == 1 or x == numero-1:
        return True
    for i in range(expoente-1):
        x = pow(x, 2, numero)
        if x == numero-1:
            return True
    return False
```

## Explicação do Código
1. **Fatoração de `n-1`**: A função `millerRabin` decompõe `n-1` na forma `2^e * m`, determinando os valores de `m` e `e`.
2. **Testes Aleatórios**: Para `k` iterações, escolhe-se um número `a` aleatório e verifica-se a condição `a^m mod n`.
3. **Verificação de Primalidade**: Se `a^m mod n` for `1` ou `n-1`, o número pode ser primo. Caso contrário, quadramos o resultado iterativamente para verificar se `n-1` aparece como resíduo modular.
4. **Retorno do Resultado**: Se algum teste falhar, o número é composto; caso contrário, é provavelmente primo.

## Uso
Tendo um verificador de números primos, torna-se possível gerar os primos necessários para o algoritmo RSA. Conforme especificado no trabalho, no RSA, os valores de \( p \) e \( q \) devem ter 1024 bits. No arquivo [GeradorDePrimos.py](GeradorDePrimos.py), é definida a função responsável por gerar um número primo com o tamanho especificado:  

```python
def geracaoDePrimos(bits):
    while True:
        num = random.getrandbits(bits)  
        num |= (1 << (bits - 1))  # Garante que o bit mais significativo seja 1
        num |= 1  # Garante que o número seja ímpar
        if millerRabin(num, 10):
            return num
```

Nessa função, primeiro é gerado um número aleatório de 1024 bits. Em seguida, garante-se que o bit correspondente a \( 2^{1023} \) seja 1 e que o bit menos significativo \( 2^0 \) também seja 1. Isso assegura que o número tenha exatamente 1024 bits e seja ímpar, visto que o único número primo par é o 2, que não possui 1024 bits.  

Após essa etapa, o número gerado é submetido ao teste de primalidade de Miller-Rabin. Se não for primo, o processo continua até encontrar um número válido.





