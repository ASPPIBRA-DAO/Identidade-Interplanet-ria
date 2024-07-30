from jinja2 import Template
import logging

logging.basicConfig(level=logging.INFO)

def show_contract(contract: str, data: dict):
    """Mostra o layout HTML e CSS do documento preenchido com os dados validados do arquivo JSON.

    Args:
        contract: O contrato preenchido com os dados JSON.
        data: Um dicionário contendo os dados para preencher o contrato.
    """
    try:
        # Renderizar o HTML com os dados fornecidos
        html = Template(contract).render(data)

        # Imprimir o HTML
        print(html)
    except Exception as e:
        logging.error(f"Erro ao renderizar o contrato: {e}")

# Exemplo de uso
# template = "<html><body><h1>{{ nome }}</h1></body></html>"
# dados = {"nome": "João"}
# show_contract(template, dados)
