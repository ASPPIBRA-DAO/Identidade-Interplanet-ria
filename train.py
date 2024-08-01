import cv2
import os
import numpy as np
import logging

class train_images:
    """
    Classe para extrair e processar imagens para treinamento de reconhecimento facial usando múltiplos métodos de detecção.
    """

    def __init__(self, use_dnn=False, confidence_threshold=0.5, scaleFactor=1.1, minNeighbors=5):
        """
        Inicializa as listas para armazenar imagens e IDs das imagens. 
        Permite a escolha do método de detecção de faces.

        Args:
        - use_dnn: Se True, usa o detector baseado em DNN, caso contrário, usa o Haar Cascade.
        - confidence_threshold: Limite de confiança para detecção de faces usando DNN.
        - scaleFactor: Parâmetro scaleFactor para Haar Cascade.
        - minNeighbors: Parâmetro minNeighbors para Haar Cascade.
        """
        self.images = []
        self.imageId = []
        self.use_dnn = use_dnn
        self.confidence_threshold = confidence_threshold
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors

        if self.use_dnn:
            # Carregar o modelo DNN
            self.net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")
        else:
            # Carregar o classificador Haar Cascade
            self.cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        
        logging.basicConfig(level=logging.INFO)

    def detect_faces(self, image):
        """
        Detecta faces em uma imagem usando o método escolhido.

        Args:
        - image: Imagem onde as faces serão detectadas.

        Returns:
        - faces: Lista de retângulos de faces detectadas.
        """
        if self.use_dnn:
            # Detecção com DNN
            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
            self.net.setInput(blob)
            detections = self.net.forward()
            faces = []
            for i in range(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > self.confidence_threshold:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    faces.append((startX, startY, endX - startX, endY - startY))
            return faces
        else:
            # Converter para escala de cinza para detecção com Haar Cascade
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            detected_faces = self.cascade.detectMultiScale(gray_image, scaleFactor=self.scaleFactor, minNeighbors=self.minNeighbors, minSize=(30, 30))
            return list(detected_faces)  # Garantir que o retorno seja uma lista

    def extractImages(self, path):
        """
        Extrai imagens do diretório especificado e prepara para o treinamento usando o método de detecção escolhido.

        Args:
        - path: Caminho do diretório contendo subdiretórios nomeados pelos IDs das imagens.

        Returns:
        - images: Lista das imagens processadas em escala de cinza.
        - imageId: Lista dos IDs correspondentes das imagens.
        """
        for root, dirs, files in os.walk(path):
            for fname in files:
                img_id = os.path.basename(root)
                
                # Ignorar subdiretórios que não são numéricos
                if not img_id.isdigit():
                    logging.warning(f"Subdiretório {img_id} não é um ID numérico. Ignorando.")
                    continue
                
                img = os.path.join(root, fname)
                image = cv2.imread(img)
                
                if image is None:
                    logging.error(f"Erro ao ler a imagem {img}.")
                    continue

                faces = self.detect_faces(image)

                if len(faces) != 1:
                    logging.warning(f"Imagem {img} não possui exatamente uma face detectada. Faces detectadas: {len(faces)}")
                    continue

                x, y, w, h = faces[0]
                gray = cv2.cvtColor(image[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
                equalize = cv2.equalizeHist(gray)
                eq_image = cv2.medianBlur(equalize, 3)
                
                self.imageId.append(int(img_id))
                self.images.append(eq_image)
                
                logging.info(f"Imagem {img} processada com sucesso.")

        return self.images, self.imageId

# Testes unitários básicos
if __name__ == "__main__":
    import unittest

    class TestTrainImages(unittest.TestCase):
        def setUp(self):
            # Crie instâncias da classe com diferentes configurações
            self.trainer_dnn = train_images(use_dnn=True, confidence_threshold=0.6)
            self.trainer_haar = train_images(use_dnn=False, scaleFactor=1.2, minNeighbors=4)
            self.test_image_path = 'face_data/users/user1/img01.jpg'  # Atualize o caminho para uma imagem válida

        def test_detect_faces_dnn(self):
            image = cv2.imread(self.test_image_path)
            self.assertIsNotNone(image, "Não foi possível carregar a imagem de teste.")
            faces = self.trainer_dnn.detect_faces(image)
            self.assertIsInstance(faces, list, "Faces não detectadas corretamente usando DNN")

        def test_detect_faces_haar(self):
            image = cv2.imread(self.test_image_path)
            self.assertIsNotNone(image, "Não foi possível carregar a imagem de teste.")
            faces = self.trainer_haar.detect_faces(image)
            self.assertIsInstance(faces, list, "Faces não detectadas corretamente usando Haar Cascade")

        def test_extractImages(self):
            images, imageIds = self.trainer_dnn.extractImages('face_data')  # Atualize o caminho conforme necessário
            self.assertIsInstance(images, list, "Imagens não extraídas corretamente")
            self.assertIsInstance(imageIds, list, "IDs das imagens não extraídos corretamente")
            self.assertTrue(all(isinstance(i, int) for i in imageIds), "Todos os IDs devem ser inteiros")

    unittest.main()

# Exemplo de uso
# Crie uma instância da classe com o método de detecção desejado
trainer = train_images(use_dnn=True, confidence_threshold=0.6)  # Defina use_dnn como True para usar o método DNN

# Defina o caminho para o diretório 'face_data'
path = 'face_data'

# Extraia as imagens do diretório 'face_data'
images, imageIds = trainer.extractImages(path)
