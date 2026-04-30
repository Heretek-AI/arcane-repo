import os
from fastapi import FastAPI

app = FastAPI(title='NanoBot', version='1.0.0', description='HKU NanoBot')

@app.get('/health')
async def health():
    return {'status': 'ok', 'framework': 'NanoBot'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('NANOBOT_PORT', '8000')))
