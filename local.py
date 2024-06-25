#Bibliotecas de criptografia
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

#Bibliotecas de interface
from PySimpleGUI import PySimpleGUI as sg

#Bibliotecas de grafico
import numpy as np
import matplotlib.pylab as plt

#Funcoes 
def obterMensagem():
    return input("Digite a mensagem: ")

def criptografiaAES(chave, texto):
    cifra = AES.new(chave, AES.MODE_CBC)
    iv = cifra.iv
    msg_cripto = cifra.encrypt(pad(texto.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + msg_cripto).decode('utf-8')

def converterBinario(texto):
    #Converte cada caractere de texto para seu valor ASCII e formata para uma representação binária de 8 bits.
    #Depois concatena tudo em uma string só
    binario = ''.join(format(ord(char), '08b') for char in texto)
    return binario

def desconverterBinario(binario):
    # Divide a sequência binária em grupos de 8 bits
    bytes = [binario[i:i+8] for i in range(0, len(binario), 8)]

    # Converte cada grupo de 8 bits de volta para um caractere ASCII
    texto = ''.join(chr(int(byte, 2)) for byte in bytes)

    return texto

def descriptografiaAES(chave, texto):
    texto = base64.b64decode(texto)
    iv = texto[:AES.block_size]
    texto = texto[AES.block_size:]
    cifra = AES.new(chave, AES.MODE_CBC, iv)
    textoDescriptografado = unpad(cifra.decrypt(texto), AES.block_size)
    return textoDescriptografado.decode('utf-8')

def aplicarCodigoDeLinha(mensagemGraf):
    # Define your data (e.g., binary stream)
    data = list(map(int, mensagemGraf))
    
    # Map data to 4D-PAM5 symbols (you'll need a lookup table)
    # For simplicity, assume each symbol lasts for T seconds

    # Create time vector
    T = 1.0  # Symbol duration (adjust as needed)
    time = np.arange(0, len(data) * T, T)

    # Generate PAM5 waveform (replace with your mapping logic)
    pam5_waveform = []  # List of voltage levels
    
    for i in range(0, len(data), 2):
        # Extract two bits
        bits = data[i:i + 2]

        # Map to PAM5 voltage level
        if bits == [0, 0]:
            pam5_waveform.append(-2)  # -2V
        elif bits == [1, 0]:
            pam5_waveform.append(-1)  # -1V
        elif bits == [0, 1]:
            pam5_waveform.append(1)   # +1V
        elif bits == [1, 1]:
            pam5_waveform.append(2)   # +2V
        else:
            pam5_waveform.append(0)   # probably useless
 
    return pam5_waveform, T

def fazerGrafico(sinal, T):
    # Create time axis
    time = np.arange(len(sinal))

    # Upsample PAM5 levels to create a square waveform
    square_waveform = np.repeat(sinal, int(1 / T))
    
    # Plot the waveform
    plt.clf()
    plt.plot(time, square_waveform, drawstyle="steps-pre", marker="o", linestyle="-", color="b", label="PAM5 Signal")
    plt.axhline(y=0, color='red', linestyle='--', label='Zero Voltage')
    plt.xlabel("Time")
    plt.ylabel("Voltage Level")
    plt.title("PAM5 Square Waveform")
    plt.grid(True)
    plt.legend()
    plt.show()

def reverterCodigoDeLinha(pam5_waveform):
    outBits = []
    for i in range(len(pam5_waveform)):
        if pam5_waveform[i] == -2:
            outBits.append(0)
            outBits.append(0)
        elif pam5_waveform[i] == -1:
            outBits.append(1)
            outBits.append(0)
        elif pam5_waveform[i] == 1:
            outBits.append(0)
            outBits.append(1)
        elif pam5_waveform[i] == 2:
            outBits.append(1)
            outBits.append(1)
        elif pam5_waveform[i] == 0:
            print("No signal")  #probably useless
        else:
            print("Invalid")

    #return outBits
    return ''.join(map(str, outBits))

#Layout
sg.theme('Reddit')
layout =  [
        [sg.Text('Servidor', font=('Helvetica', 15))],
        [sg.Text('Mensagem:'), sg.Input(key='mensagemBox')],
        [sg.Button('Enviar'),sg.Button('Transmitir')],
        [sg.Text('Mensagem criptografada:'), sg.Text("", key='mensagemCriptoK')],
        [sg.Text('Mensagem em binário:'), sg.Text("", key='mensagemBinK')],
        [sg.Text('Mensagem em cóodigo de linha:'), sg.Text("", key='mensagemLinhaK')],
        [sg.Text('Mensagem em cóodigo de linha enviada:'), sg.Text("", key='mensagemLinhaEnvK')],
        #--------------------------------------------------
        [sg.Text('\nCliente', font=('Helvetica', 15))],
        [sg.Text('Mensagem em cóodigo de linha recebida:'), sg.Text("", key='mensagemLinhaRecK')],
        [sg.Text('Mensagem em cóodigo de linha revertida:'), sg.Text("", key='mensagemLinhaDecK')],
        [sg.Text('Mensagem desconvertida de binário:'), sg.Text("", key='mensagemDesconvK')],
        [sg.Text('Mensagem inicial:'), sg.Text("", key='mensagemDescriptoK')]
]

#Janela
janela = sg.Window('Codificação de linha - 4D-Pam5', layout)

#Eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break;
    elif eventos == 'Enviar':
        #Servidor-------------------------------------
        mensagem = valores['mensagemBox']
        #msg_bytes = mensagem.encode('utf-8')  # Converte para bytes usando UTF-8 (encrypt não aceita string)
        chave = get_random_bytes(16) #16 bytes para serem a chave do AES-128
        mensagemCripto = criptografiaAES(chave, mensagem)
        janela['mensagemCriptoK'].update(mensagemCripto)
        mensagemBin = converterBinario(mensagemCripto)
        janela['mensagemBinK'].update(mensagemBin)
        #Codigo de linha/Servidor---------------------
        mensagemLinha, time=aplicarCodigoDeLinha(mensagemBin)
        janela['mensagemLinhaK'].update(mensagemLinha)
    elif eventos == 'Transmitir':
        for tam in range(0, len(mensagemLinha) + 4, 4):
            fazerGrafico(mensagemLinha[0:tam], time)
            janela['mensagemLinhaEnvK'].update(mensagemLinha[0:tam])
        #Codigo de linha/Cliente---------------------
            janela['mensagemLinhaRecK'].update(mensagemLinha[0:tam])
            mensagemLinhaDec = reverterCodigoDeLinha(mensagemLinha[0:tam])
            janela['mensagemLinhaDecK'].update(mensagemLinhaDec[0:2*tam])
        #Cliente--------------------------------------
            msg_desconv = desconverterBinario(mensagemLinhaDec)
            janela['mensagemDesconvK'].update(msg_desconv)
        msg_descripto = descriptografiaAES(chave, msg_desconv)
        janela['mensagemDescriptoK'].update(msg_descripto)

#msg_desconv_bytes = msg_desconv.encode('utf-8')  # Converte para bytes usando UTF-8 (decrypt não aceita string)
