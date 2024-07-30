# Importa bibliotecas necessárias
import cv2
import os
from PIL import Image
import numpy as np

# Define a classe train_images
class train_images:
    """
    Classe para extrair e processar imagens para treinamento de reconhecimento facial.
    """

    def __init__(self):
        """
        Inicializa as listas para armazenar imagens e IDs das imagens.
        """
        self.images = []
        self.imageId = []

    def extractImages(self, path):
        """
        Extrai imagens do diretório especificado e prepara para o treinamento.

        Args:
        - path: Caminho do diretório contendo subdiretórios nomeados pelos IDs das imagens.

        Returns:
        - images: Lista das imagens processadas em escala de cinza.
        - imageId: Lista dos IDs correspondentes das imagens.
        """
        # Percorre todos os arquivos e diretórios no caminho especificado
        for root, dirs, files in os.walk(path):
            for fname in files:
                # Obtém o ID da imagem a partir do nome do diretório
                img_id = os.path.basename(root)
                
                # Constrói o caminho completo da imagem
                img = os.path.join(root, fname)
                
                # Lê a imagem usando OpenCV
                image = cv2.imread(img)
                
                # Converte a imagem para escala de cinza
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Carrega o classificador Haar Cascade para detecção de faces
                cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                
                # Detecta faces na imagem
                face = cascade.detectMultiScale(gray_image, 1.1, 5)

                # Continua para a próxima imagem se não houver exatamente uma face detectada
                if len(face) != 1:
                    continue

                # Obtém as coordenadas da face detectada
                x, y, w, h = face[0]
                
                # Extrai a região da face da imagem em escala de cinza
                gray = gray_image[y:y+h, x:x+w]
                
                # Equaliza o histograma da imagem da face
                equalize = cv2.equalizeHist(gray)
                
                # Aplica filtro de mediana para reduzir ruído
                eq_image = cv2.medianBlur(equalize, 3)
                
                # Adiciona o ID da imagem à lista de IDs
                self.imageId.append(int(img_id))
                
                # Adiciona a imagem processada à lista de imagens
                self.images.append(eq_image)

        # Retorna as listas de imagens e IDs das imagens
        return self.images, self.imageId
