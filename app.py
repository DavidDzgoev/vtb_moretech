from flask import Flask
import asyncio
from game import create_tasks
import os

loop = asyncio.get_event_loop()
app = Flask(__name__)


@app.route('/')
async def root():
    res = loop.run_until_complete(create_tasks())
    return res

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
