import qrcode
import os
import logging
from urllib.parse import urlparse

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fotos Aéreas
fotos_aereas = [
    "https://i.postimg.cc/rsJpjKWd/Aerofotografia-04.png",
    "https://i.postimg.cc/GmSH68fG/Aerofotografia-05.png",
    "https://i.postimg.cc/0yNztdV9/Aerofotografia-06.png",
    "https://i.postimg.cc/FsTRJkN8/Aerofotografia-07.png"
]

# Fotos de Casa
fotos_casa = [
    "https://i.postimg.cc/VLmrtcMr/Casa-01.png",
    "https://i.postimg.cc/nzqrsdhG/Casa-02.png",
    "https://i.postimg.cc/MH8ctCFL/Casa-03.png",
    "https://i.postimg.cc/CLTC6t8S/Casa-04.png"
]

# Plantas
plantas = [
    "https://i.postimg.cc/MZsBCmG3/Distrito.png",
    "https://i.postimg.cc/8CDsJ75r/Pl-baixa-01.png",
    "https://i.postimg.cc/3x2dxXKT/Pl-baixa-02.png",
    "https://i.postimg.cc/htRt6XV3/Pl-cadastral.png",
    "https://i.postimg.cc/1RTt0CXS/Pl-situa-o.png"
]

# Certidões
certidoes = [
    "https://i.postimg.cc/4324mDGc/Art.png",
    "https://i.postimg.cc/GhvpqgP0/Ata-notarial.png",
    "https://i.postimg.cc/44DdvR9b/Declarat-ria.png",
    "https://i.postimg.cc/2yBsjJjC/nus-reais.png"
]

# Função para verificar se uma URL é válida
def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Função para gerar e salvar QR codes
def gerar_qrcode(lista: list[str], categoria: str) -> None:
    # Criar diretório para a categoria se não existir
    if not os.path.exists(categoria):
        os.makedirs(categoria)

    for item in lista:
        if is_valid_url(item):
            try:
                meu_qrcode = qrcode.make(item)
                filename = os.path.join(categoria, f"qrcode_{item.split('/')[-1]}.png")
                meu_qrcode.save(filename)
                logging.info(f"QR code salvo: {filename}")
            except Exception as e:
                logging.error(f"Erro ao gerar QR code para {item}: {e}")
        else:
            logging.warning(f"URL inválida: {item}")

# Gerar QR codes para cada categoria
gerar_qrcode(fotos_aereas, "Fotos_Aereas")
gerar_qrcode(fotos_casa, "Fotos_Casa")
gerar_qrcode(plantas, "Plantas")
gerar_qrcode(certidoes, "Certidoes")
