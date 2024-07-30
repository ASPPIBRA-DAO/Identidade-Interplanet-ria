import numpy as np
import os
import cv2
from train import train_images as tr
from DetectImage import detect_image as detect
import tkinter as tk

def train_recognizer():
    """
    Treina o reconhecedor facial LBPH se o arquivo 'trained.yml' não existir.
    """
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    tr_images = tr()
    images, image_id = tr_images.extractImages("./training_set")
    image_id = np.array(image_id)
    recognizer.train(images, image_id)
    recognizer.save('trained.yml')

if not os.path.isfile('trained.yml'):
    train_recognizer()

# Inicializa a janela principal do aplicativo tkinter
root = tk.Tk()
root.geometry('300x200')
root.title('FARES')

# Cria um frame dentro da janela principal
frame = tk.Frame(root, bg="#FFF")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Inicializa a classe de detecção de imagem com os arquivos de registro e presença
d = detect('Record.xlsx', 'attendence.xlsx')

def mark_entry():
    """
    Identifica um aluno, marca sua entrada na planilha de presença e exibe o nome identificado.
    """
    p_name = d.identify()
    cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV
    print(p_name)
    d.markEntry(p_name)

def close_entry():
    """
    Identifica um aluno, fecha sua entrada na planilha de presença e exibe o nome identificado.
    """
    p_name = d.identify()
    cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV
    print(p_name)
    d.close_entry(p_name)

# Cria botões para marcar e fechar entradas de presença
mark_entry_button = tk.Button(root, text="Mark Entry", command=mark_entry)
mark_entry_button.place(relx=0.2, rely=0.5)

close_entry_button = tk.Button(root, text="Close Entry", command=close_entry)
close_entry_button.place(relx=0.6, rely=0.5)

# Inicia o loop principal da aplicação tkinter
if __name__ == '__main__':
    root.mainloop()
