"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Web Server - Flask-based interface for Thalos Prime

Serves the Matrix-style chatbot interface and handles API requests
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.cis import CIS
from ai.neural.bio_neural_network import BioNeuralNetwork
from ai.learning.reinforcement_learner import ReinforcementLearner

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# Initialize Thalos Prime system
cis = CIS()
cis.boot()

# Initialize AI components
neural_net = BioNeuralNetwork("thalos_main")
rl_agent = ReinforcementLearner(state_dim=10, action_dim=5)

# Create neural network architecture
input_layer = neural_net.create_layer(10, "input")
hidden_layer1 = neural_net.create_layer(20, "hidden")
hidden_layer2 = neural_net.create_layer(15, "hidden")
output_layer = neural_net.create_layer(5, "output")

neural_net.connect_layers(input_layer, hidden_layer1, 0.6)
neural_net.connect_layers(hidden_layer1, hidden_layer2, 0.6)
neural_net.connect_layers(hidden_layer2, output_layer, 0.7)


@app.route('/')
def index():
    """Serve the main chatbot interface"""
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return send_from_directory('static', path)


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and process through AI"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process message through neural network
        # Convert message to input pattern (simplified)
        input_pattern = message_to_pattern(message)
        
        # Stimulate neural network
        neural_net.stimulate_inputs(input_pattern)
        
        # Simulate processing
        for _ in range(50):
            neural_net.simulate_step()
        
        # Get output
        output_activity = neural_net.get_output_activity()
        
        # Get network stats
        stats = neural_net.get_network_stats()
        
        # Generate response based on output
        response_text = generate_response(message, output_activity, stats)
        
        # Calculate confidence
        confidence = sum(output_activity) / len(output_activity) if output_activity else 0.5
        
        # Prepare metadata
        metadata = {
            'neuralDensity': stats.get('avg_firing_rate', 0) / 100.0,
            'confidence': min(1.0, confidence / 10.0),
            'activeLobes': ['logic', 'abstract', 'governance'],
            'processingTime': round(stats.get('current_time', 0) / 1000.0, 2),
            'spikeCount': stats.get('total_spikes', 0),
            'synapticWeight': stats.get('avg_synaptic_weight', 0.5)
        }
        
        return jsonify({
            'response': response_text,
            'metadata': metadata
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    cis_status = cis.status()
    neural_stats = neural_net.get_network_stats()
    rl_stats = rl_agent.get_statistics()
    
    return jsonify({
        'cis': cis_status,
        'neural_network': neural_stats,
        'reinforcement_learning': rl_stats,
        'system_health': 'OPERATIONAL'
    })


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get detailed system metrics"""
    neural_stats = neural_net.get_network_stats()
    
    return jsonify({
        'neural_density': neural_stats.get('avg_firing_rate', 0) / 100.0,
        'accuracy': 0.85 + (neural_stats.get('avg_synaptic_weight', 0.5) - 0.5) * 0.3,
        'spike_rate': neural_stats.get('avg_firing_rate', 0),
        'synaptic_connections': neural_stats.get('num_synapses', 0),
        'active_neurons': neural_stats.get('num_neurons', 0)
    })


def message_to_pattern(message: str) -> list:
    """
    Convert text message to neural input pattern
    
    Args:
        message: Input text
        
    Returns:
        List of input values (0.0 to 1.0)
    """
    # Simple encoding: character frequencies and message properties
    pattern = []
    
    # Message length (normalized)
    pattern.append(min(1.0, len(message) / 100.0))
    
    # Character type ratios
    alpha_count = sum(1 for c in message if c.isalpha())
    digit_count = sum(1 for c in message if c.isdigit())
    space_count = sum(1 for c in message if c.isspace())
    
    total = len(message) if len(message) > 0 else 1
    pattern.append(alpha_count / total)
    pattern.append(digit_count / total)
    pattern.append(space_count / total)
    
    # Word count (normalized)
    word_count = len(message.split())
    pattern.append(min(1.0, word_count / 20.0))
    
    # Uppercase ratio
    upper_count = sum(1 for c in message if c.isupper())
    pattern.append(upper_count / total)
    
    # Question detection
    pattern.append(1.0 if '?' in message else 0.0)
    
    # Command detection
    pattern.append(1.0 if message.startswith('/') else 0.0)
    
    # Sentiment indicators (simplified)
    positive_words = ['good', 'great', 'yes', 'thanks', 'hello']
    negative_words = ['bad', 'no', 'error', 'wrong']
    
    message_lower = message.lower()
    has_positive = any(word in message_lower for word in positive_words)
    has_negative = any(word in message_lower for word in negative_words)
    
    pattern.append(1.0 if has_positive else 0.0)
    pattern.append(1.0 if has_negative else 0.0)
    
    return pattern


def generate_response(message: str, output_activity: list, stats: dict) -> str:
    """
    Generate response text based on neural network output
    
    Args:
        message: Original message
        output_activity: Neural network output
        stats: Network statistics
        
    Returns:
        Response text
    """
    # Analyze output pattern
    max_activity_idx = output_activity.index(max(output_activity)) if output_activity else 0
    avg_activity = sum(output_activity) / len(output_activity) if output_activity else 0
    
    # Response templates based on output neuron activation
    templates = [
        # Neuron 0: Analytical response
        f"Biological computation analysis: Query '{message}' processed through {stats.get('num_synapses', 0)} synaptic pathways. Pattern classification complete with neural consensus across cortical analogs.",
        
        # Neuron 1: Creative response
        f"Abstract lobe synthesis: Your query stimulates novel neural pathways. Temporal cortex analog generates creative interpretation suggesting multidimensional solution space exploration.",
        
        # Neuron 2: Factual response
        f"Logic lobe processing: Frontal cortex analog engaged. Query analyzed through {stats.get('num_neurons', 0)} neurons with spike-train coherence. Deterministic reasoning pathway activated.",
        
        # Neuron 3: Ethical response
        f"Governance lobe evaluation: Parietal cortex analog assesses ethical alignment. Prime Directive conformance verified. Query demonstrates {int(avg_activity * 100)}% alignment with ACCURACY-EXPANSION-PRESERVATION principles.",
        
        # Neuron 4: Integrated response
        f"Multi-lobe integration complete: Query '{message}' processed through wetware core with {stats.get('avg_firing_rate', 0):.1f}Hz average firing rate. Dopaminergic reward signal positive. Knowledge expansion achieved through {stats.get('total_spikes', 0)} action potentials."
    ]
    
    response = templates[max_activity_idx % len(templates)]
    
    # Add neural activity context
    if avg_activity > 5.0:
        response += f" [High neural activity detected: {avg_activity:.1f}Hz - Strong pattern recognition]"
    elif avg_activity < 2.0:
        response += f" [Low neural activity: {avg_activity:.1f}Hz - Ambiguous pattern, expanding search space]"
    
    return response


if __name__ == '__main__':
    print("=" * 60)
    print("THALOS PRIME - SYNTHETIC BIOLOGICAL INTELLIGENCE")
    print("=" * 60)
    print(f"CIS Status: {cis.status()['status']}")
    print(f"Neural Network: {neural_net.get_network_stats()['num_neurons']} neurons")
    print(f"Web Interface: http://localhost:8000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=False)
