import os
from fastapi import FastAPI

app = FastAPI(title='OpenSpiel', version='1.0.0', description='Google DeepMind OpenSpiel')

@app.get('/health')
async def health():
    import pyspiel
    games = pyspiel.registered_games()
    return {'status': 'ok', 'games_available': len(games), 'framework': 'OpenSpiel'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('OPENSPIEL_PORT', '8080')))
