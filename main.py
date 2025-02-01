from Parte_1.RSA import RSA
from Parte_2.Parte_2_3 import Hash
import sys
def main():
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:], start=1):
            print(f"Argumento {i}: {arg}")
    else:
        print("Nenhum argumento recebido.")

if __name__ == "__main__":
    main()