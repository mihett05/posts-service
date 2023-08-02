def custom_preprocessing_hook(endpoints):
    print(endpoints)
    api_path = "/api/"
    return [
        (path, path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
        if path.startswith(api_path)
    ]
