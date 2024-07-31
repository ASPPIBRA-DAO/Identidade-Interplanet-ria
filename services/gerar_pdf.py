import weasyprint
from jinja2 import Template
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_template(template_path: str) -> Template:
    """Lê o conteúdo do arquivo de template HTML e retorna um objeto Template."""
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return Template(f.read())
    except Exception as e:
        logger.error(f"Erro ao ler o template HTML: {e}")
        raise

def render_html(template: Template, contract: dict) -> str:
    """Renderiza o conteúdo do template HTML com os dados do contrato."""
    try:
        return template.render(
            document=contract['document'],
            owners=contract['owners'],
            area_description=contract['area_description'],
            professionals=contract['professionals'],
            topography_plans=contract['topography_plans'],
            house_plans=contract['house_plans'],
            photo_report=contract['photo_report'],
            construction_licensing=contract['construction_licensing'],
            city_hall=contract['city_hall'],
            registry_office=contract['registry_office'],
            onus_reais=contract['onus_reais'],
            notarial_minutes=contract['notarial_minutes'],
            judicial_note=contract['judicial_note']
        )
    except KeyError as e:
        logger.error(f"Campo ausente no contrato: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro ao renderizar o HTML: {e}")
        raise

def generate_pdf(contract: dict, template_html: str, base_url: str, stylesheets_path: str) -> bytes:
    """Gera um arquivo PDF a partir do layout HTML e CSS do documento.

    Args:
        contract (dict): O contrato preenchido com os dados JSON.
        template_html (str): Caminho para o arquivo de template HTML.
        base_url (str): URL base para resolução de recursos relativos.
        stylesheets_path (str): Caminho para o arquivo CSS.

    Returns:
        bytes: O arquivo PDF gerado.
    """
    try:
        # Ler e renderizar o template HTML
        template = read_template(template_html)
        html = render_html(template, contract)

        # Criar um documento WeasyPrint com o HTML renderizado e o arquivo CSS
        document = weasyprint.HTML(string=html, encoding="utf-8", base_url=base_url).render(stylesheets=[stylesheets_path])

        # Retornar o documento PDF gerado
        return document.write_pdf()
    except Exception as e:
        logger.error(f"Erro ao gerar o PDF: {e}")
        raise
