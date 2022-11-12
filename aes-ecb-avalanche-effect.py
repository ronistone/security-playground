import random
from math import floor
from os import system


def generate_random_bytes(num_bits):
    payload =  random.randbytes(num_bits)
    return payload



def generate_plain_text(num=10):
    print("Generating plain texts:")
    for i in range(1, num+1):
        filename = f"M{i}.txt"
        data = generate_random_bytes(16)
        write_file(filename, data)

def generate_plain_text_line(num=10):
    print("Generating plain texts with one bit flipped:")
    for i in range(1, num+1):
        filename = f"M{i}.txt"
        newFilename = f"M{i}'.txt"
        data = read_file(filename)

        flippedBit, dataProcessed = flipBit(data)

        print(f"Flipped the bit {flippedBit+1}")

        diff = compareBits(data, dataProcessed)
        print(f"{filename}, {newFilename} Files diff in {diff} bits")

        write_file(newFilename, bytes(dataProcessed))

def byte_xor(ba1, ba2):
    """ XOR two byte strings """
    return bytearray([_a ^ _b for _a, _b in zip(ba1, ba2)])

def compareBits(a,b):
    if len(a) != len(b):
        print("Size differ")
    count = 0
    compared = byte_xor(a,b)
    for i in range(len(compared)):
        for j in range(8):
            if compared[i] & (1 << j):
                count += 1
    return count

def flipBit(data):
    flippedBit = random.randrange(len(data)*8)
    flippedByte = floor(flippedBit / 8)
    flippedByteBit = flippedBit % 8
        
    dataProcessed = bytearray(data)
    dataProcessed[flippedByte] = dataProcessed[flippedByte] ^ (1 << flippedByteBit)
    return flippedBit, bytes(dataProcessed)

def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def write_file(filename, data, mode="wb"):
    with open(filename, mode) as file:
        print(f"Writing {filename} with {len(data)} bytes ({len(data)*8} bits)")
        file.write(data)

def generate_key(size=16):
    print("Generating Key")
    filename = "key"
    data = generate_random_bytes(size).hex()
    write_file(filename, data, 'w')

def cipher_with_openssl(filename, filenameOutput):
    system(f"openssl enc -in {filename} -aes-128-ecb -K $(cat key) -out {filenameOutput}")

def cipher_all_files(num=10):
    for i in range(1,num+1):
        print(f"encrypting M{i}.txt and M{i}'.txt...")
        cipher_with_openssl(f"M{i}.txt", f"C{i}.txt")
        cipher_with_openssl(f"M{i}\\'.txt", f"C{i}\\'.txt")

def compare_all_encrypted_file(num=10):
    for i in range(1, num+1):
        cData = read_file(f"C{i}.txt")
        cLineData = read_file(f"C{i}'.txt")
        diff = compareBits(cData, cLineData)
        print(f"C{i}.txt and C{i}'.txt differ in {diff} bits ({((diff/128)*100):.2f}%)!")

if __name__ == "__main__":
    # A)
    print("\n\nA)\n===========================")
    generate_plain_text()
    print("===========================\n\n")

    # B)
    print("\n\nB)\n===========================")
    generate_key()
    print("===========================\n\n")

    # C)
    print("\n\nC)\n===========================")
    generate_plain_text_line()
    print("===========================\n\n")

    # D) e E)
    print("\n\nD) e E)\n===========================")
    cipher_all_files()
    print("===========================\n\n")

    # F)
    print("\n\nF)\n===========================")
    compare_all_encrypted_file()
    print("===========================\n\n")



"""
Crie um arquivo texto com o seu nome completo e número de matrícula. Coloque o print do arquivo texto.Crie um breve relatório (PDF) sobre o experimento para avaliar o efeito avalanche do AES. A ideia do efeito avalanche é mensurar a taxa de bits diferentes entre os textos cifrado e claro. Siga os passos abaixo.

a) Crie dez textos claros (M1, M2, M3.., M10), cada um deles contendo EXATAMENTE 16 bytes ou 128 bits. No Linux, por exemplo, você pode usar o seguinte comando: "echo "abcdefghijhkde1" > teste1.txt" (note que foram adicionador 15 bytes - o último byte representa o encerramento do arquivo).
b) Crie uma chave de 128 bits.
c) Mude 1 byte em cada um dos dez textos claros criados na letra a). Agora nós teremos M1', M2', M3', ..., M10'.
d) Use o OpenSSL para cifrar cada um dos dez textos claros usando o AES-ECB e a chave da letra b). Agora nós teremos C1, C2, C3, ..., C10.
e) Use o OpenSSL para cifrar cada um dos dez textos claros modificados usando o AES-ECB e a chave da letra b). Agora nós teremos C1', C2', ..., C10'.
f) Compare C1 e C1' e conte quantos BITS são diferentes. Qual a taxa de bits diferentes (# de bits diferentes/128)?

"""