#Bibliotecas de criptografia
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

def obterMensagem():
    return input("Digite a mensagem: ")

def criptografiaAES(chave, texto):
    cifra = AES.new(chave, AES.MODE_ECB)
    cifra = cifra.encrypt(pad(texto, AES.block_size))
    return b64encode(texto).decode('latin1')

def converterBinario(texto):
    #Converte cada caractere de texto para seu valor ASCII e formata para uma representação binária de 8 bits.
    #Depois concatena tudo em uma string só
    binario = ''.join(format(ord(char), '08b') for char in texto)
    return binario

mensagem = obterMensagem()
msg_bytes = mensagem.encode('utf-8')  # Converte para bytes usando UTF-8 (encrypt não aceita string)

chave = get_random_bytes(16) #16 bytes para serem a chave do AES-128

mensagemCripto = criptografiaAES(chave, msg_bytes) 
print("Mensagem criptografada:", mensagemCripto)

mensagemBin = converterBinario(mensagemCripto)
print("Mensagem em binário:", mensagemBin)

def desconverterBinario(binario):
    # Divide a sequência binária em grupos de 8 bits
    bytes = [binario[i:i+8] for i in range(0, len(binario), 8)]
    
    # Converte cada grupo de 8 bits de volta para um caractere ASCII
    texto = ''.join(chr(int(byte, 2)) for byte in bytes)
    
    return texto

msg_desconv = desconverterBinario(mensagemBin)
print("Mensagem desconvertida de binário:", msg_desconv)

#msg_desconv_bytes = msg_desconv.encode('utf-8')  # Converte para bytes usando UTF-8 (decrypt não aceita string)

def descriptografiaAES(chave, texto):
    cifra = AES.new(chave, AES.MODE_ECB)
    textoDescriptografado = cifra.decrypt(pad(b64decode(texto), AES.block_size))
    return textoDescriptografado.decode('latin1').rstrip('\0')

msg_descripto = descriptografiaAES(chave, msg_desconv)
print("Mensagem inicial:", msg_descripto)