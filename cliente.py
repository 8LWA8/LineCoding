#Biblioteca para o Bluetooth
import socket

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
def desconverterBinario(binario):
    # Divide a sequência binária em grupos de 8 bits
    bytes = [binario[i:i+8] for i in range(0, len(binario), 8)]

    # Converte cada grupo de 8 bits de volta para um caractere ASCII
    texto = ''.join(chr(int(byte, 2)) for byte in bytes)

    return texto

def pad_base64(s):
    return s + '=' * (-len(s) % 4)

def descriptografiaAES(chave, texto, iv):
    #texto = pad_base64(texto)
    #texto_deco = base64.b64decode(texto)
    #print(texto_deco)
    print("iv")
    print(iv)
    #texto_deco = texto_deco[AES.block_size:]
    cifra = AES.new(chave, AES.MODE_CBC, iv)
    textoDescriptografado = unpad(cifra.decrypt(texto), AES.block_size)
    print(textoDescriptografado)
    return textoDescriptografado.decode('utf-8')

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


def fazerGrafico(sinal, T):
    # Create time axis
    print("grafico")
    time = np.arange(0, len(sinal) * T, T)

    # Upsample PAM5 levels to create a square waveform
    square_waveform = np.repeat(sinal, int(1 / T))

    # Plot the waveform
    plt.ion()
    plt.clf()
    plt.plot(time, square_waveform, drawstyle="steps-pre", marker="o", linestyle="-", color="b", label="PAM5 Signal")
    plt.axhline(y=0, color='red', linestyle='--', label='Zero Voltage')
    plt.xlabel("Time")
    plt.ylabel("Voltage Level")
    plt.title("PAM5 Square Waveform")
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.pause(0.001)

def fazerList(v):
    v = v.replace('1','1 ')
    v = v.replace("-1","-1 ")
    v = v.replace("-12","-1 2")
    v = v.replace("-2","-2 ")
    v = v.replace("2","2 ")
    return v.split()

#Configuracao do Bluetooth do cliente
cliente =  socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
cliente.connect(("04:6c:59:0e:23:32", 4))#MAC do servidor e canal

#Layout
sg.theme('Reddit')
layout =  [
    [sg.Text('\nCliente', font=('Helvetica', 15))],
    [sg.Text('Mensagem em cóodigo de linha recebida:'), sg.Text("", key='mensagemLinhaRecK')],
    [sg.Text('Mensagem em cóodigo de linha revertida:'), sg.Text("", key='mensagemLinhaDecK')],
    [sg.Text('Mensagem desconvertida de binário:'), sg.Text("", key='mensagemDesconvK')],
    [sg.Text('Mensagem inicial:'), sg.Text("", key='mensagemDescriptoK')]
]

#Janela
janela = sg.Window('Codificação de linha(Cliente) - 4D-Pam5', layout)

try:
    print("try")
    while True:
        print("while true")
        eventos, valores = janela.read(timeout=100)
        print("chegou")
        if eventos == sg.WINDOW_CLOSED:
            break
        else:
            print("else msg")
            decoded_text = cliente.recv(1040).decode('utf-8', errors='replace')
            m = fazerList(decoded_text)
            print(m)
            m2 = list(map(float, m))
            print(m2)
            mensagemLinha = list(map(int, m2))
            print("mensagemLinha")
            print(mensagemLinha)
        if not mensagemLinha:
            
            break
        print(decoded_text)
        time = (decoded_text)
        print(time)
        time_list=fazerList(time)
        print(time_list)
        time_float = np.array(time_list, dtype=float)
        print("time_float: ")
        print(time_float)
        if not time:
            print("quebrou")
            break
        chave = cliente.recv(1040)
        print(chave)
        if not chave:
            break
        
        iv = cliente.recv(1040)
        print("iv")
        print(iv)
        '''
        iv2 = cliente.recv(1040)
        print("iv2")
        print(iv2)
        iv3 = cliente.recv(1040)
        print("iv3")
        print(iv3)
        iv4 = cliente.recv(1040)
        print("iv4")
        print(iv4)
        '''

        for tam in range(4, len(mensagemLinha) + 4, 4):
            fazerGrafico(mensagemLinha[0:tam], 1.0)
            print("final grafico")
            #Codigo de linha/Cliente---------------------
            janela['mensagemLinhaRecK'].update(mensagemLinha)
            mensagemLinhaDec = reverterCodigoDeLinha(mensagemLinha)
            print("reverter cod")
            #janela['mensagemLinhaDecK'].update(mensagemLinhaDec[0:2*tam])
            #Cliente--------------------------------------
            msg_desconv = desconverterBinario(mensagemLinhaDec)
            print("desconv bin")
            janela['mensagemDesconvK'].update(msg_desconv)
            print(msg_desconv)
            msg_desconv_pad = pad_base64(msg_desconv)
            print("chave")
            print(chave)
            if chave.startswith(b'1.0'):
                chave = chave[len(b'1.0'):]
            #chave_deco=chave.decode('utf-8')
            print("chave_if")
            print(chave)
            msg_descripto = descriptografiaAES(chave, msg_desconv, iv)
            print("descripto")
            janela['mensagemDescriptoK'].update(msg_descripto)
        
except OSError as e:
    pass

cliente.close()

