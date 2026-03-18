from flask import Flask, render_template, request, jsonify
import sys
import io
import contextlib

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code', '')
    
    # Capture stdout
    f = io.StringIO()
    try:
        with contextlib.redirect_stdout(f):
            # Use restricted globals/locals for a 'mini' sandbox
            # NOTE: exec() is dangerous in production; for a course app in a local container it's acceptable for demo purposes
            exec(code, {'__builtins__': __builtins__}, {})
        output = f.getvalue()
        error = None
    except Exception as e:
        output = f.getvalue()
        error = str(e)
        
    return jsonify({'output': output, 'error': error})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
