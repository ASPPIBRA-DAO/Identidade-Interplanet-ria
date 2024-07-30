from datetime import datetime
import os
import logging

logging.basicConfig(level=logging.ERROR)

def save_document(documento_bytes: bytes) -> bool:
    """Salva documento gerado em pdf na pasta documentos

    Args:
        documento_bytes: Bytes do documento

    Returns:
        bool: True se o documento for salvo com sucesso, False caso contrário.
    """
    try:
        # Criar uma pasta "documents" se não existir
        if not os.path.exists("documents"):
            os.makedirs("documents")

        # Criar um nome de arquivo com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"documents/escritura_{timestamp}.pdf"

        # Salvamento do documento PDF
        with open(filename, "wb") as f:
            f.write(documento_bytes)

        return True
    except Exception as e:
        logging.error(f"Erro ao salvar o documento: {e}")
        return False
