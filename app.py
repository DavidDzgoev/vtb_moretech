from flask import Flask, render_template, redirect, request
from game import create_tasks
import os

app = Flask(__name__)


@app.route('/')
async def root():
    return create_tasks()

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
