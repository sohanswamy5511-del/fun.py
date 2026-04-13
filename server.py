from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import queue
import time
import os
import re

app = Flask(__name__, static_folder='static')
app.secret_key = 'fun-game-secret'

# Global state for game process
game_process = None
output_queue = queue.Queue()
input_queue = queue.Queue()
game_thread = None
output_buffer = []  # Buffer for collecting output before sending
last_output_time = time.time()

# Symbol mapping for images
SYMBOL_IMAGES = {
    'Coin': 'coin.svg',
    'Spinner': 'spinner.svg', 
    'Dice': 'dice.svg',
    'Card': 'card.svg',
    'Wheel': 'wheel.svg'
}

def read_output():
    """Read output from game process and buffer it before sending"""
    global game_process, output_buffer, last_output_time
    if game_process:
        while True:
            try:
                line = game_process.stdout.readline()
                if not line:
                    break
                # Process the line to replace symbols with images
                processed_line = process_line_for_images(line.decode('utf-8', errors='ignore'))
                
                # Send welcome message immediately (don't buffer it)
                if "Welcome to the Slot Machine Game" in processed_line:
                    output_queue.put(processed_line)
                    last_output_time = time.time()
                    continue
                
                # Check if this is the start of a new spin
                if "--- SPIN" in processed_line:
                    # Send any buffered output first
                    if output_buffer:
                        combined_output = ''.join(output_buffer)
                        output_queue.put(combined_output)
                        output_buffer.clear()
                    
                    # Add a delay before the spin (1 second)
                    time.sleep(1.0)
                    
                    # Send the spin header
                    output_queue.put(processed_line)
                    last_output_time = time.time()
                    continue
                
                # Add other lines to buffer
                output_buffer.append(processed_line)
                
                # Send buffer if it's been more than 200ms or buffer is getting large
                current_time = time.time()
                if (current_time - last_output_time > 0.2) or (len(output_buffer) > 10):
                    if output_buffer:
                        combined_output = ''.join(output_buffer)
                        output_queue.put(combined_output)
                        output_buffer.clear()
                        last_output_time = current_time
                        
            except Exception as e:
                output_queue.put(f"[Error reading output: {e}]\n")
                break

def process_line_for_images(line):
    """Replace symbol display names with HTML image tags with multiplier overlay"""
    # Pattern to match symbol display names like "Coin (Heads)", "Spinner (x12)", etc.
    for symbol_name, image_file in SYMBOL_IMAGES.items():
        # Replace symbol names with image tags including multiplier
        if symbol_name == 'Coin':
            # Special handling for Coin - extract Heads/Tails and convert to multiplier
            pattern = r'Coin \((Heads|Tails)\)'
            def coin_replacer(match):
                result = match.group(1)
                mult = '5' if result == 'Heads' else '1'
                return f'<div class="symbol-container"><img src="/static/images/{image_file}" alt="Coin ({result})" title="Coin ({result})" class="symbol-image"><div class="multiplier-overlay">{mult}</div></div>'
            line = re.sub(pattern, coin_replacer, line)
        else:
            # For other symbols, extract the multiplier from (x{number})
            pattern = rf'({re.escape(symbol_name)}\s*\(x(\d+)\))'
            def replacer(match):
                full_match = match.group(1)
                mult = match.group(2)
                return f'<div class="symbol-container"><img src="/static/images/{image_file}" alt="{full_match}" title="{full_match}" class="symbol-image"><div class="multiplier-overlay">{mult}</div></div>'
            line = re.sub(pattern, replacer, line)
    
    return line

def send_input():
    """Send input from queue to game process"""
    global game_process
    if game_process:
        while True:
            try:
                user_input = input_queue.get(timeout=1)
                if user_input:
                    game_process.stdin.write((user_input + '\n').encode())
                    game_process.stdin.flush()
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Error sending input: {e}")
                break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Start the slot machine game"""
    global game_process, game_thread
    
    try:
        # Start the game process with unbuffered output so text appears immediately
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'
        game_process = subprocess.Popen(
            ['python', '-u', '/workspaces/fun.py/fun.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=False,
            env=env
        )
        
        # Start threads to handle I/O
        threading.Thread(target=read_output, daemon=True).start()
        threading.Thread(target=send_input, daemon=True).start()
        
        return jsonify({'status': 'ok', 'message': 'Game started'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get-output', methods=['GET'])
def get_output():
    """Get accumulated output from game"""
    output = ""
    try:
        while True:
            output += output_queue.get_nowait()
    except queue.Empty:
        pass
    return jsonify({'output': output})

@app.route('/api/send-input', methods=['POST'])
def send_user_input():
    """Send user input to game"""
    user_input = request.json.get('input', '').strip()
    if user_input:
        input_queue.put(user_input)
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error', 'message': 'Empty input'}), 400

if __name__ == '__main__':
    app.run(debug=False, host='localhost', port=5000)
