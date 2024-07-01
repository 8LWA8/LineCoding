#Biblioteca para o Bluetooth
import socket

#Bibliotecas de criptografia
'''
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import unicodedata
'''
import string

#Bibliotecas de interface
from PySimpleGUI import PySimpleGUI as sg

#Bibliotecas de grafico
import numpy as np
import matplotlib.pylab as plt

#Funcoes
'''
def criptografiaAES(chave, texto):
    cifra = AES.new(chave, AES.MODE_CBC)
    iv = cifra.iv
    print("iv funcao")
    print(iv)
    msg_cripto = cifra.encrypt(pad(texto.encode('utf-8'), AES.block_size))
    return (base64.b64encode(iv + msg_cripto).decode('utf-8'), iv)
'''
def criptografar(mensagem, chave):
    alfabeto = string.ascii_letters + string.digits + string.punctuation + ' áéíóúãõâêîôûçÁÉÍÓÚÃÕÂÊÎÔÛÇ'
    alfabeto_cifrado = alfabeto[chave:] + alfabeto[:chave]
    tabela = str.maketrans(alfabeto, alfabeto_cifrado)
    return mensagem.translate(tabela)

def converterBinario(texto):
    #Converte cada caractere de texto para seu valor ASCII e formata para uma representação binária de 8 bits.
    #Depois concatena tudo em uma string só
    binario = ''.join(format(ord(char), '08b') for char in texto)
    return binario

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

#Configuracao do Bluetooth do servidor
servidor =  socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
servidor.bind(("04:6c:59:0e:23:32", 4))#MAC do servidor e canal
servidor.listen(1)#Quantidade de dispositivos que podem se comunicar no canal

cliente, addr = servidor.accept()#Aceitar conexao com o cliente

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
]

#Janela
janela = sg.Window('Codificação de linha(Servidor) - 4D-Pam5', layout)

try:
    while True:
        plt.figure(figsize=(10,6))
        eventos, valores = janela.read()
        if eventos == sg.WINDOW_CLOSED:
            break;
        elif eventos == 'Enviar':
            #Servidor-------------------------------------
            mensagem = valores['mensagemBox']
            mensagemCripto = criptografar(mensagem, 4)
            janela['mensagemCriptoK'].update(mensagemCripto)
            mensagemBin = converterBinario(mensagemCripto)
            janela['mensagemBinK'].update(mensagemBin)
            #Codigo de linha/Servidor---------------------
            mensagemLinha, time=aplicarCodigoDeLinha(mensagemBin)
            janela['mensagemLinhaK'].update(mensagemLinha)
        elif eventos == 'Transmitir':
            for tam in range(4, len(mensagemLinha) + 4, 4):
                fazerGrafico(mensagemLinha[0:tam], time)
                janela['mensagemLinhaEnvK'].update(mensagemLinha[0:tam])
                m = ''.join(map(str, mensagemLinha[0:tam]))
                print(mensagemLinha[0:tam])
                print(m)
                cliente.send(m.encode('utf-8'))
                print(m.encode('utf-8'))
except OSError as e:
    pass

cliente.close()
servidor.close()
