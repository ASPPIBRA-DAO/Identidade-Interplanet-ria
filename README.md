# Modelo de Identidade IPFS

## Visão Geral

Este projeto implementa um sistema de criação de um modelo de Identidade Digital para interação em sistemas descentralizados interplanetários, utilizando reconhecimento facial para a geração de credenciais e identificação dos usuários em transações financeiras que necessitam de provas de autenticidade (2FA). O sistema utiliza técnicas de aprendizado de máquina e processamento de imagens para detectar rostos em imagens, reconhecer usuários cadastrados e registrar sua presença em uma planilha Excel.

## Modelos de Biometria

- **Facial**: Reconhecimento de rostos através de imagens ou vídeos.

### Futuras Atualizações

- **Íris**: Análise da íris do olho para identificação individual.
- **Digital**: Leitura e comparação de impressões digitais.
- **Voz**: Análise das características únicas da voz de uma pessoa.

## Estrutura do Projeto

O projeto está estruturado em vários arquivos e classes principais:

- **main.py**: Implementa uma interface gráfica simples usando Tkinter para interação com o sistema.
- **train.py**: Contém a lógica para o treinamento do reconhecedor facial utilizando imagens de um diretório específico.
- **CNNmodel.py**: Define uma rede neural convolucional para processamento de imagens.
- **create_excel_files.py**: Cria arquivos Excel para registro de alunos e presenças.
- **DetectImage.py**: Realiza a detecção de rostos em tempo real utilizando um classificador Haar Cascade e o reconhecedor LBPH.
- **tree_structure.txt**: Arquivo que descreve a estrutura do projeto.
- **trained.yml**: Arquivo que armazena o modelo treinado do reconhecedor facial.

## Funções Adicionais 📝

### Automação de Geração de Credenciais 🤖

Este projeto implementa um sistema automatizado para geração de credenciais. O sistema funciona da seguinte forma:

- 📄 O usuário preenche um formulário HTML com as informações pessoais.
- ✅ As informações do formulário são validadas.
- 💾 Os dados do formulário são salvos no formato JSON em um banco de dados criptografado.
- 📋 O modelo da Certidão é preenchido com as informações validadas.
- 🖨️ O layout de impressão da Certidão é exibido para o usuário.
- 📥 O usuário pode clicar em um botão para gerar um PDF para a impressão da Certidão e da Carteirinha.

## Refereciias

- <https://github.com/topics/face-recognition-database>

## Dependências

O projeto depende das seguintes bibliotecas Python:

- OpenCV (cv2)
- Pillow (PIL)
- openpyxl
- numpy
- tkinter

As dependências podem ser instaladas executando o seguinte comando:

```bash
pip install -r requirements.txt

- Funcionalidades Principais

- Treinamento do Reconhecedor Facial: Utiliza imagens de um diretório para treinar um modelo de reconhecimento facial.

- Detecção de Rostos em Tempo Real: Utiliza um classificador Haar Cascade para detectar rostos em vídeo ao vivo.

- Registro de Presença: Registra a entrada e saída de indivíduos reconhecidos em uma planilha Excel.

- Melhorias Potenciais

- Modularização do Código: Separação mais clara das funcionalidades em módulos reutilizáveis.

- Documentação Aprofundada: Explicação detalhada das funções e classes em comentários no código.

- Tratamento de Erros Robusto: Implementação de tratamento de exceções para melhor robustez.

- Testes Unitários: Criação de testes para verificar o funcionamento correto das funcionalidades.

- Configurabilidade: Adição de opções para configurar parâmetros como caminhos de diretório e arquivos.

- Segurança: Consideração de medidas adicionais para proteger dados sensíveis e prevenir vulnerabilidades.

## Execução no Linux/macOS
Para configurar o ambiente e executar o projeto:


Configuração do Ambiente Virtual:

```bash
python3 -m venv env
source env/bin/activate

Instalação de Dependências:

```bash
pip install -r requirements.txt

Treinamento do Modelo:

```bash
python train.py

Atualização das Dependências:

```bash
pip freeze > requirements.txt

Estrutura do Projeto:

```bash
tree --prune -I 'env' > tree_structure.txt
