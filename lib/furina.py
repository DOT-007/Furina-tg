import os
from config import MODE

plugins = []
middleware = []

def Furina(config, handler):
    config.setdefault("fromMe", True)
    config.setdefault("noprefix", False)
    plugins.append({"config": config, "handler": handler})
    return handler

def register_middleware(func):
    middleware.append(func)
    return func

isPrivate = MODE == "private"

_middleware_cache = {}

async def run_middleware(msg, client):
    if len(_middleware_cache) > 1000:
        _middleware_cache.clear()
        
    for mid in middleware:
        try:
            cache_key = f"{mid.__name__}_{msg.id}"
            if cache_key in _middleware_cache:
                result = _middleware_cache[cache_key]
            else:
                result = await mid(msg, client)
                _middleware_cache[cache_key] = result
                
            if result is False:
                return False
        except Exception as e:
            print(f"Middleware error: {str(e)}")
    return True
