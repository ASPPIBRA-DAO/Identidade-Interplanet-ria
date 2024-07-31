def validate_form_data(json_data):
    """Valida os dados do JSON do formulário.

    Args:
        json_data: Os dados do formulário.

    Returns:
        None

    Raises:
        ValueError: Se alguma inconsistência for detectada.
    """
    print(json_data)
    
    # Verifica se a data de início é anterior à data de término
    if "start_date" in json_data and "end_date" in json_data:
        if json_data["start_date"] > json_data["end_date"]:
            raise ValueError("A data de início deve ser anterior à data de término.")
    
    # Adicione outras validações conforme necessário

    # Exemplo: Verificar se campos obrigatórios estão presentes
    required_fields = ["name", "email", "phone", "association"]
    for field in required_fields:
        if field not in json_data:
            raise ValueError(f"O campo {field} é obrigatório.")

# Exemplo de uso
data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "123-456-7890",
    "association": "Sample Association",
    "start_date": "2023-01-01",
    "end_date": "2022-12-31"
}

try:
    validate_form_data(data)
except ValueError as e:
    print(e)
