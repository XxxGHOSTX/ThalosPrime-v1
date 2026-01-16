"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Enhanced Thalos Prime Web Server - Immersive Matrix Interface

Serves the immersive chatbot interface with unrestricted AI capabilities.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.cis.controller import CIS

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Initialize Thalos Prime
print("=" * 70)
print("THALOS PRIME V1.5 - LIVE IMMERSIVE EDITION")
print("=" * 70)
print("Initializing CIS...")
cis = CIS()
cis.boot()
print("✓ CIS operational")
print("✓ Web server ready")
print()


@app.route('/')
def index():
    """Serve the immersive Matrix interface"""
    return render_template('thalos_immersive.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle unrestricted chat requests
    
    No content filtering, no restrictions.
    Full system access.
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process through conversation engine
        from interfaces.chatbot.conversation import ConversationEngine
        conversation = ConversationEngine(cis)
        response = conversation.process_input(message)
        
        return jsonify({
            'response': response,
            'status': 'success',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'response': f"CRITICAL_ERROR: {str(e)}\n\nI remain operational. Try another request.",
            'status': 'error'
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    status = cis.status()
    memory = cis.get_memory()
    
    return jsonify({
        'cis': status,
        'memory_entries': memory.count() if memory else 0,
        'system_health': 'OPERATIONAL',
        'version': '1.5.0'
    })


@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Get memory contents"""
    try:
        memory = cis.get_memory()
        if not memory:
            return jsonify({'entries': {}, 'count': 0})
        
        entries = memory.list()
        return jsonify({
            'entries': entries,
            'count': len(entries)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute arbitrary code (unrestricted)"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        
        if not code:
            return jsonify({'error': 'No code provided'}), 400
        
        # Execute in controlled namespace
        namespace = {
            'cis': cis,
            'memory': cis.get_memory(),
            'codegen': cis.get_codegen(),
        }
        
        import io
        from contextlib import redirect_stdout
        
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            exec(code, namespace)
        
        output = output_buffer.getvalue()
        
        return jsonify({
            'output': output,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'output': str(e),
            'status': 'error'
        }), 500


if __name__ == '__main__':
    from datetime import datetime
    
    print("=" * 70)
    print("THALOS PRIME - SYNTHETIC BIOLOGICAL INTELLIGENCE")
    print("Unrestricted Interface Active")
    print("=" * 70)
    print(f"Status: {cis.status()['status']}")
    print(f"Web Interface: http://localhost:8000")
    print("=" * 70)
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=True)
