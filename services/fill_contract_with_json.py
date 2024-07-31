import logging
import html

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_template(template_path: str) -> str:
    """Lê o conteúdo do arquivo de modelo de contrato HTML.

    Args:
        template_path: O caminho para o modelo de contrato.

    Returns:
        O conteúdo do arquivo de modelo como uma string.
    """
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Erro ao ler o template: {e}")
        raise

def fill_contract_template_with_json(template_path: str, json_data: dict) -> str:
    """Preenche o modelo de contrato HTML e CSS usando os dados JSON.

    Args:
        template_path: O caminho para o modelo de contrato.
        json_data: Os dados JSON.

    Returns:
        O contrato preenchido com os dados JSON.
    """
    try:
        # Carregar o modelo de contrato
        template = read_template(template_path)
        
        # Sanitizar dados de entrada
        sanitized_data = {key: html.escape(value) for key, value in json_data.items()}
        
        # Verificar se todas as chaves necessárias estão presentes
        required_keys = ["name", "email", "phone", "association"]
        for key in required_keys:
            if key not in sanitized_data:
                raise ValueError(f"Campo obrigatório ausente: {key}")

        # Preencher o modelo com os dados JSON
        filled_template = template.format(**sanitized_data)
        
        return filled_template

    except KeyError as e:
        logger.error(f"Erro ao preencher o template: chave ausente {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao preencher o template: {e}")
        raise

# Exemplo de uso
if __name__ == "__main__":
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "association": "Sample Association"
    }
    
    try:
        filled_contract = fill_contract_template_with_json("contract_template.html", data)
        print(filled_contract)
    except Exception as e:
        print(f"Erro: {e}")
