def custom_preprocessing_hook(endpoints):
    """
    Исключение не API endpoint'ов из openapi и swagger
    """
    api_path = "/api/"
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if path.startswith(api_path)
    ]
