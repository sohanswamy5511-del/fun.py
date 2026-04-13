from flask import Flask, render_template, request, jsonify, session
import subprocess
import os
import sys

app = Flask(__name__)
app.secret_key = 'fun-game-secret'

# Store game processes
game_processes = {}

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    """Start a new game instance"""
    session_id = request.json.get('session_id', 'default')
    
    # Start the game process
    try:
        # Add the fun.py directory to path so imports work
        sys.path.insert(0, '/workspaces/fun.py')
        
        # Import and run game
        from fun import main
        game_processes[session_id] = main
        
        return jsonify({'status': 'started', 'session_id': session_id})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
