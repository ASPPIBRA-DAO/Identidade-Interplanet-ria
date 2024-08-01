import cv2
import os
import numpy as np
import logging

class TrainImages:
    """
    Classe para extrair e processar imagens para treinamento de reconhecimento facial usando múltiplos métodos de detecção.
    """

    def __init__(self, use_dnn=False, confidence_threshold=0.5, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)):
        """
        Inicializa as listas para armazenar imagens e IDs das imagens. 
        Permite a escolha do método de detecção de faces.

        Args:
        - use_dnn: Se True, usa o detector baseado em DNN, caso contrário, usa o Haar Cascade.
        - confidence_threshold: Limite de confiança para detecção de faces usando DNN.
        - scaleFactor: Parâmetro scaleFactor para Haar Cascade.
        - minNeighbors: Parâmetro minNeighbors para Haar Cascade.
        - minSize: Parâmetro minSize para Haar Cascade.
        """
        self.images = []
        self.imageId = []
        self.use_dnn = use_dnn
        self.confidence_threshold = confidence_threshold
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.minSize = minSize

        # Verificar a presença dos arquivos de modelo
        if self.use_dnn:
            self.prototxt_path = "deploy.prototxt"
            self.model_path = "res10_300x300_ssd_iter_140000.caffemodel"
            if not os.path.isfile(self.prototxt_path):
                raise FileNotFoundError(f"Arquivo de configuração do modelo não encontrado: {self.prototxt_path}")
            if not os.path.isfile(self.model_path):
                raise FileNotFoundError(f"Arquivo do modelo não encontrado: {self.model_path}")
            self.net = cv2.dnn.readNetFromCaffe(self.prototxt_path, self.model_path)
        else:
            self.cascade_path = "haarcascade_frontalface_default.xml"
            if not os.path.isfile(self.cascade_path):
                raise FileNotFoundError(f"Arquivo do classificador Haar Cascade não encontrado: {self.cascade_path}")
            self.cascade = cv2.CascadeClassifier(self.cascade_path)
        
        logging.basicConfig(level=logging.INFO)

    def detect_faces(self, image):
        """
        Detecta faces em uma imagem usando o método escolhido.

        Args:
        - image: Imagem onde as faces serão detectadas.

        Returns:
        - faces: Lista de retângulos de faces detectadas.
        """
        try:
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
                detected_faces = self.cascade.detectMultiScale(gray_image, scaleFactor=self.scaleFactor, minNeighbors=self.minNeighbors, minSize=self.minSize)
                return list(detected_faces)
        except Exception as e:
            logging.error(f"Erro na detecção de faces: {e}")
            return []

    def extract_images(self, path):
        """
        Extrai imagens do diretório especificado e prepara para o treinamento usando o método de detecção escolhido.

        Args:
        - path: Caminho do diretório contendo subdiretórios nomeados pelos IDs das imagens.

        Returns:
        - images: Lista das imagens processadas em escala de cinza.
        - imageId: Lista dos IDs correspondentes das imagens.
        """
        if not os.path.isdir(path):
            raise FileNotFoundError(f"O diretório especificado não foi encontrado: {path}")

        for root, dirs, files in os.walk(path):
            for fname in files:
                img_id = os.path.basename(root)
                
                # Validar se img_id é numérico
                if not img_id.isdigit():
                    logging.warning(f"Subdiretório {img_id} não é um ID numérico. Ignorando.")
                    continue
                
                img = os.path.join(root, fname)
                try:
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
                    
                    try:
                        img_id = int(img_id)
                        self.imageId.append(img_id)
                        self.images.append(eq_image)
                    except ValueError:
                        logging.error(f"ID da imagem {img_id} é inválido. Ignorando.")
                        continue
                    
                    logging.info(f"Imagem {img} processada com sucesso.")
                except Exception as e:
                    logging.error(f"Erro ao processar a imagem {img}: {e}")

        return self.images, self.imageId

# Testes unitários básicos
if __name__ == "__main__":
    import unittest
    from unittest.mock import patch, MagicMock

    class TestTrainImages(unittest.TestCase):
        def setUp(self):
            # Criar instâncias da classe com diferentes configurações
            self.trainer_dnn = TrainImages(use_dnn=True, confidence_threshold=0.6)
            self.trainer_haar = TrainImages(use_dnn=False, scaleFactor=1.2, minNeighbors=4)
            
            # Mock de caminho de imagem válido
            self.test_image_path = 'face_data/test_image.jpg'
            
            # Mock para simular a existência de uma imagem
            if not os.path.isfile(self.test_image_path):
                cv2.imwrite(self.test_image_path, np.zeros((300, 300, 3), dtype=np.uint8))

        @patch('cv2.imread', return_value=np.zeros((300, 300, 3), dtype=np.uint8))
        def test_detect_faces_dnn(self, mock_imread):
            image = cv2.imread(self.test_image_path)
            faces = self.trainer_dnn.detect_faces(image)
            self.assertIsInstance(faces, list, "Faces não detectadas corretamente usando DNN")

        @patch('cv2.imread', return_value=np.zeros((300, 300, 3), dtype=np.uint8))
        def test_detect_faces_haar(self, mock_imread):
            image = cv2.imread(self.test_image_path)
            faces = self.trainer_haar.detect_faces(image)
            self.assertIsInstance(faces, list, "Faces não detectadas corretamente usando Haar Cascade")

        @patch('os.path.isdir', return_value=True)
        @patch('cv2.imread', return_value=np.zeros((300, 300, 3), dtype=np.uint8))
        def test_extract_images(self, mock_imread, mock_isdir):
            images, imageIds = self.trainer_dnn.extract_images('face_data')  # Mock do caminho de diretório
            self.assertIsInstance(images, list, "Imagens não extraídas corretamente")
            self.assertIsInstance(imageIds, list, "IDs das imagens não extraídos corretamente")
            self.assertTrue(all(isinstance(i, int) for i in imageIds), "Todos os IDs devem ser inteiros")

    unittest.main()

# Exemplo de uso
# Crie uma instância da classe com o método de detecção desejado
trainer = TrainImages(use_dnn=True, confidence_threshold=0.6)  # Defina use_dnn como True para usar o método DNN

# Defina o caminho para o diretório 'face_data'
path = 'face_data'

# Extraia as imagens do diretório 'face_data'
images, imageIds = trainer.extract_images(path)
