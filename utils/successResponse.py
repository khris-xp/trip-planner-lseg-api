def success_response(message: str, data: list = None):
    return {"status": 200, "message": message, "timestamp": __import__('datetime').datetime.utcnow().isoformat() + 'Z', "data": data or []}