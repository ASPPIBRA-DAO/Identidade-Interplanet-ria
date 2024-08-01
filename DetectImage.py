# Importa as bibliotecas necessárias
import numpy as np
import pandas as pd
import os
import cv2
import openpyxl
from openpyxl import load_workbook
from datetime import datetime

# Dicionário para mapear rótulos de reconhecimento facial a nomes de alunos
names = {0: 'n', 1: 'm', 2: 'v', 3: 'l'}

def verify_and_load_workbook(filename):
    """
    Verifica se o arquivo existe e se é um arquivo Excel (.xlsx).
    
    Parâmetros:
    - filename: Nome do arquivo a ser verificado e carregado
    
    Retorna:
    - workbook: Objeto Workbook do openpyxl se o carregamento for bem-sucedido
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Arquivo não encontrado: {filename}")
    if not filename.endswith('.xlsx'):
        raise ValueError(f"Arquivo não é um arquivo Excel (.xlsx): {filename}")
    
    try:
        workbook = load_workbook(filename=filename)
        print(f"Arquivo {filename} carregado com sucesso.")
        return workbook
    except Exception as e:
        raise ValueError(f"Erro ao carregar o arquivo {filename}: {e}")

class detect_image:
    def __init__(self, recordSheet, attendenceSheet):
        """
        Inicializa a classe de detecção de imagem com planilhas de registro e presença.
        
        Parâmetros:
        - recordSheet: Nome do arquivo Excel de registro
        - attendenceSheet: Nome do arquivo Excel de presença
        """
        self.recordSheet = recordSheet
        self.attendenceSheet = attendenceSheet
        
        # Carrega o classificador de faces Haar Cascade
        self.cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        if self.cascade.empty():
            raise ValueError("Classificador Haar Cascade não carregado corretamente.")
        
        # Inicializa o reconhecedor facial LBPH e carrega um modelo treinado
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        if not os.path.isfile('trained.yml'):
            raise FileNotFoundError("Modelo treinado não encontrado.")
        self.recognizer.read('trained.yml')
        
        # Lista para armazenar alunos já marcados como presentes
        self.students_marked = []
        
        # Carrega as planilhas de registro e de presença
        self.recordWorkbook = verify_and_load_workbook(filename=recordSheet)
        self.attendenceWorkbook = verify_and_load_workbook(filename=attendenceSheet)

    def identify(self):
        """
        Identifica um aluno usando reconhecimento facial em tempo real.
        
        Retorna:
        - Nome do aluno identificado
        """
        print("Iniciando identificação...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Erro ao abrir a captura de vídeo.")
            return None

        f = 0
        pred_name = "None"

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar o frame.")
                break
            
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            equalize = cv2.equalizeHist(gray_frame)
            image = cv2.medianBlur(equalize, 3)
            faces = self.cascade.detectMultiScale(image, 1.1, 5)
            
            if len(faces) == 0:
                print("Nenhuma face detectada.")
            
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 4)
                label, conf = self.recognizer.predict(gray_frame[y:y+h, x:x+w])
                p_name = names.get(label, "Desconhecido")
                pred_name = p_name
                print(f"Face detectada: {p_name} (Confiança: {conf})")
                cv2.imshow("Recognizing Face", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Tecla 'q' pressionada. Encerrando.")
                    break

                f += 1
                if f > 15:
                    print("Mais de 15 quadros processados. Encerrando.")
                    break

        cap.release()
        cv2.destroyAllWindows()
        return pred_name

    def writeEntry(self, p_name, branch, year):
        """
        Escreve a entrada de presença na planilha de presença.
        
        Parâmetros:
        - p_name: Nome do aluno
        - branch: Ramo de estudo do aluno
        - year: Ano do aluno
        """
        sheet = self.attendenceWorkbook.active
        sheet.insert_rows(idx=2, amount=1)
        sheet["A2"] = p_name
        sheet["B2"] = year
        sheet["C2"] = branch
        
        time = datetime.now()
        curr_time = time.strftime("%H:%M:%S")
        sheet["D2"] = curr_time
        
        self.attendenceWorkbook.save(self.attendenceSheet)
        print(f"Presença registrada para {p_name}.")

    def markEntry(self, p_name):
        """
        Marca a entrada de um aluno na planilha de presença.
        
        Parâmetros:
        - p_name: Nome do aluno
        """
        if p_name in self.students_marked:
            print("Entrada já marcada!")
        else:
            self.students_marked.append(p_name)
            sheet = self.recordWorkbook.active
            
            for values in sheet.iter_rows(min_col=1, max_col=3, values_only=True):
                rec_name = values[0]
                if rec_name.lower() == p_name.lower():
                    branch = values[1]
                    year = values[2]
                    self.writeEntry(p_name, branch, year)
                    print(f"Entrada marcada para {p_name}.")
                    break

    def close_entry(self, p_name):
        """
        Fecha a entrada de presença de um aluno na planilha de presença.
        
        Parâmetros:
        - p_name: Nome do aluno
        """
        if p_name not in self.students_marked:
            print("Entrada não marcada!")
        else:
            sheet = self.attendenceWorkbook.active
            index = 0
            
            for values in sheet.iter_rows(values_only=True):
                rec_name = values[0]
                index += 1
                if rec_name.lower() == p_name.lower():
                    time = datetime.now()
                    curr_time = time.strftime("%H:%M:%S")
                    sheet["E" + str(index)] = curr_time
                    print("Entrada fechada!")
                    
                    self.attendenceWorkbook.save(self.attendenceSheet)
                    self.students_marked.remove(p_name)
                    break
