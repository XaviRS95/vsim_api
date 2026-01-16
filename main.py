import uvicorn
from config.config import API_CONFIG

if __name__ == "__main__":
    uvicorn.run("app.app:app", host=API_CONFIG['host'], port=int(API_CONFIG['port']), reload=False,
        #access_log=False,
        #log_level="critical"  # disables info/debug logs from uvicorn.*
    )