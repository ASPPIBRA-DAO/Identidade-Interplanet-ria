def convert_form_input_to_json(form_data):
    """Converte os dados do formulário em um objeto JSON.

    Args:
        form_data: Os dados do formulário.

    Returns:
        Um objeto JSON.
    """
    try:
        json_data = {
            "name": form_data["name"],
            "email": form_data["email"],
            "phone": form_data["phone"],
            "association": form_data["association"],
        }
    except KeyError as e:
        raise ValueError(f"Campo ausente no formulário: {e}")

    return json_data
