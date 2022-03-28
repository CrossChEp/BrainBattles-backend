def model_without_nones(model: dict) -> dict:
    output_json = {}
    for key, value in model.items():
        if value is None:
            pass
        output_json[key] = value
    return output_json
