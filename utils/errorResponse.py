def error_response(message: str):
    return {"status": 400, "message": message, "timestamp": __import__('datetime').datetime.utcnow().isoformat() + 'Z', "data": []}