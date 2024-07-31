import numpy as np
import os
import cv2
import logging
import tkinter as tk
from tkinter import messagebox
from train import train_images as tr
from DetectImage import detect_image as detect

# Configuração de logging
def setup_logging():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Validação de caminhos de arquivos
def validate_file_paths(file_paths):
    for path in file_paths:
        if not os.path.isfile(path):
            logging.error(f"Arquivo não encontrado: {path}")
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

# Função para treinar o reconhecedor
def train_recognizer():
    """
    Treina o reconhecedor facial LBPH se o arquivo 'trained.yml' não existir.
    """
    recognizer = configure_recognizer()
    tr_images = tr()
    images, image_id = tr_images.extractImages("./training_set")
    image_id = np.array(image_id)
    recognizer.train(images, image_id)
    recognizer.save('trained.yml')

# Configura o reconhecedor facial com parâmetros específicos
def configure_recognizer(radius=1, neighbors=8):
    return cv2.face.LBPHFaceRecognizer_create(radius=radius, neighbors=neighbors)

# Função para mostrar mensagens ao usuário
def show_message(title, message):
    messagebox.showinfo(title, message)

# Função para marcar entrada de presença
def mark_entry():
    """
    Identifica um aluno, marca sua entrada na planilha de presença e exibe o nome identificado.
    """
    try:
        p_name = d.identify()
        cv2.destroyAllWindows()
        logging.info(f"Entrada marcada para: {p_name}")
        d.markEntry(p_name)
        show_message('Sucesso', f"Entrada marcada para: {p_name}")
    except Exception as e:
        logging.error(f"Erro ao marcar entrada: {e}")
        show_message('Erro', f"Erro ao marcar entrada: {e}")

# Função para fechar entrada de presença
def close_entry():
    """
    Identifica um aluno, fecha sua entrada na planilha de presença e exibe o nome identificado.
    """
    try:
        p_name = d.identify()
        cv2.destroyAllWindows()
        logging.info(f"Entrada fechada para: {p_name}")
        d.close_entry(p_name)
        show_message('Sucesso', f"Entrada fechada para: {p_name}")
    except Exception as e:
        logging.error(f"Erro ao fechar entrada: {e}")
        show_message('Erro', f"Erro ao fechar entrada: {e}")

# Função para reinicializar o reconhecedor facial
def reset_recognizer():
    """
    Reinicializa o treinamento do reconhecedor facial excluindo o modelo existente.
    """
    if os.path.isfile('trained.yml'):
        os.remove('trained.yml')
    train_recognizer()
    show_message('Sucesso', 'Reconhecedor reinicializado com sucesso.')

# Função para atualizar registros
def update_records(record_file, attendance_file):
    """
    Atualiza as planilhas de registro e presença.
    """
    try:
        # Lógica para atualizar registros e presenças (exemplo fictício)
        show_message('Atualização', 'Registros e presenças atualizados com sucesso.')
    except Exception as e:
        logging.error(f"Erro ao atualizar registros: {e}")
        show_message('Erro', f"Erro ao atualizar registros: {e}")

# Configuração inicial
setup_logging()
validate_file_paths(['trained.yml', './training_set'])

# Inicializa o treinamento se necessário
if not os.path.isfile('trained.yml'):
    train_recognizer()

# Inicializa a janela principal do aplicativo tkinter
root = tk.Tk()
root.geometry('300x200')
root.title('FARES')

# Configura a interface
frame = tk.Frame(root, bg="#FFF")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Inicializa a classe de detecção de imagem
d = detect('Record.xlsx', 'attendence.xlsx')

# Botões para marcar e fechar entradas de presença
mark_entry_button = tk.Button(root, text="Mark Entry", command=mark_entry)
mark_entry_button.place(relx=0.2, rely=0.5)

close_entry_button = tk.Button(root, text="Close Entry", command=close_entry)
close_entry_button.place(relx=0.6, rely=0.5)

# Função principal
if __name__ == '__main__':
    root.mainloop()
