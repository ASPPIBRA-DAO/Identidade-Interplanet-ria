import json
import os
import logging

def load_json(json_path: str) -> dict:
    """Lê os dados do arquivo json e retorna ele em dict.

    Args:
        json_path: Caminho do arquivo.

    Returns:
        Json dict se a leitura for bem-sucedida, senão None.
    """

    if not os.path.exists(json_path):
        logging.error(f"O arquivo {json_path} não existe.")
        return None

    try:
        with open(json_path, 'r', encoding="utf-8") as json_file:
            # Load the JSON data from the file
            data = json.load(json_file)
        return data

    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {json_path}")
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar JSON no arquivo: {json_path}")
    except Exception as e:
        logging.error(f"Ocorreu um erro ao ler o arquivo {json_path}: {e}")

    return None
