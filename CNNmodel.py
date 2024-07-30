# Importa as bibliotecas necessárias
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, MaxPooling2D, Conv2D, Flatten

class CNN:
    def __init__(self):
        """
        Inicializa uma rede neural convolucional (CNN) para classificação de imagens.

        A arquitetura inclui duas camadas convolucionais seguidas por camadas de pooling para redução de dimensionalidade,
        seguidas por camadas densas para aprendizado de características complexas e uma camada de saída para classificação.

        A entrada é esperada como imagens coloridas de 128x128 pixels.
        """
        # Inicializa o modelo sequencial
        self.model = Sequential()
        
        # Camada convolucional 1: 32 filtros 3x3, ativação ReLU, entrada para imagens coloridas de 128x128 pixels
        self.model.add(Conv2D(32, (3, 3), input_shape=(128, 128, 3), activation='relu'))
        
        # Camada de pooling 1: Reduz a dimensionalidade por 2x2
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        # Camada convolucional 2: 32 filtros 3x3, ativação ReLU
        self.model.add(Conv2D(32, (3, 3), activation='relu'))
        
        # Camada de pooling 2: Reduz a dimensionalidade por 2x2
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        
        # Camada de flattening: Converte a matriz 2D em um vetor 1D para entrada em camadas densas
        self.model.add(Flatten())
        
        # Camada densa (totalmente conectada) com 64 unidades, ativação ReLU
        self.model.add(Dense(units=64, activation='relu'))
        
        # Camada de saída: 2 unidades (para classificação binária), ativação softmax para probabilidade de classes
        self.model.add(Dense(units=2, activation='softmax'))
        
        # Compila o modelo usando Adam como otimizador, entropia cruzada categórica esparsa como função de perda para rótulos inteiros,
        # e métrica de precisão para avaliação durante o treinamento
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    def fit_model(self, x_train, y_train, epochs=50):
        """
        Treina o modelo nos dados de treinamento fornecidos.

        Parâmetros:
        - x_train: dados de entrada de treinamento
        - y_train: rótulos de classe correspondentes
        - epochs: número de épocas de treinamento (padrão: 50)
        """
        self.model.fit(x_train, y_train, epochs=epochs)

    def predict(self, x_test):
        """
        Realiza previsões nos dados de teste fornecidos.

        Parâmetros:
        - x_test: dados de entrada de teste

        Retorna:
        - Previsões do modelo para os dados de teste
        """
        return self.model.predict(x_test)
