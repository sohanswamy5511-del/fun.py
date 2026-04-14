from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import queue
import time
import os
import re
import signal

app = Flask(__name__, static_folder='static')
app.secret_key = 'fun-game-secret'

# Global state
game_process = None
output_queue = queue.Queue()
input_queue = queue.Queue()

SYMBOL_IMAGES = {
    'Coin': 'coin.svg',
    'Spinner': 'spinner.svg',
    'Dice': 'dice.svg',
    'Card': 'card.svg',
    'Wheel': 'wheel.svg'
}

def process_line_for_images(line):
    """Replace symbol names with HTML image tiles."""
    for symbol_name, image_file in SYMBOL_IMAGES.items():
        if symbol_name == 'Coin':
            pattern = r'Coin \((Heads|Tails)\)'
            def coin_replacer(match):
                result = match.group(1)
                mult = '5' if result == 'Heads' else '1'
                return (
                    f'<div class="symbol-container">'
                    f'<img src="/static/images/{image_file}" class="symbol-image">'
                    f'<div class="multiplier-overlay">{mult}</div>'
                    f'</div>'
                )
            line = re.sub(pattern, coin_replacer, line)
        else:
            pattern = rf'({re.escape(symbol_name)}\s*\(x(\d+)\))'
            def replacer(match):
                full_match = match.group(1)
                mult = match.group(2)
                return (
                    f'<div class="symbol-container">'
                    f'<img src="/static/images/{image_file}" class="symbol-image">'
                    f'<div class="multiplier-overlay">{mult}</div>'
                    f'</div>'
                )
            line = re.sub(pattern, replacer, line)
    return line

def read_output():
    """Continuously read output from the game process and flush instantly."""
    global game_process

    while True:
        if not game_process:
            time.sleep(0.05)
            continue

        line = game_process.stdout.readline()
        if not line:
            time.sleep(0.01)
            continue

        processed_line = process_line_for_images(line)

        # INSTANT FLUSH — no buffering at all
        output_queue.put(processed_line)

def send_input():
    """Send queued input to the game process."""
    global game_process

    while True:
        if not game_process:
            time.sleep(0.05)
            continue

        try:
            user_input = input_queue.get(timeout=1)
            game_process.stdin.write(user_input + '\n')
            game_process.stdin.flush()
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Error sending input: {e}")

def stop_game():
    """Kill any existing game process."""
    global game_process
    if game_process and game_process.poll() is None:
        try:
            game_process.terminate()
            try:
                game_process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                game_process.kill()
        except Exception as e:
            print(f"Error stopping game: {e}")
    game_process = None

def reset_state():
    """Reset all queues."""
    global output_queue, input_queue
    output_queue = queue.Queue()
    input_queue = queue.Queue()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Always start a fresh game on every page load."""
    global game_process

    stop_game()
    reset_state()

    try:
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        game_process = subprocess.Popen(
            ['python', '-u', '/workspaces/fun.py/fun.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
            universal_newlines=True,
            env=env
        )

        threading.Thread(target=read_output, daemon=True).start()
        threading.Thread(target=send_input, daemon=True).start()

        return jsonify({'status': 'started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get-output', methods=['GET'])
def get_output():
    output = ""
    try:
        while True:
            output += output_queue.get_nowait()
    except queue.Empty:
        pass
    return jsonify({'output': output})

@app.route('/api/send-input', methods=['POST'])
def send_user_input():
    user_input = request.json.get('input', '').strip()
    if user_input:
        input_queue.put(user_input)
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error', 'message': 'Empty input'}), 400

if __name__ == '__main__':
    app.run(debug=False, host='localhost', port=5000)
