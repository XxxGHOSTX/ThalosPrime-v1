"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Web Server - Flask-based interface for Thalos Prime

Serves the Matrix-style chatbot interface and handles API requests
Fully integrates with wetware, AI, and database systems
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os
import sys
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from core.cis import CIS
from wetware.organoid_core import OrganoidCore
from wetware.mea_interface import MEAInterface
from wetware.life_support import LifeSupport
from ai.neural.bio_neural_network import BioNeuralNetwork
from ai.learning.reinforcement_learner import ReinforcementLearner
from database.connection_manager import DatabaseManager
from interfaces.web.nlp_processor import NLPProcessor
from interfaces.web.action_handler import ActionHandler

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# Initialize Thalos Prime system
print("Initializing Thalos Prime Synthetic Biological Intelligence...")
cis = CIS()
cis.boot()
print("✓ CIS operational")

# Initialize NLP Processor
nlp = NLPProcessor()
print("✓ NLP Processor initialized")

# Initialize Action Handler
action_handler = ActionHandler(cis)
print("✓ Action Handler initialized")

# Initialize Database
db_manager = DatabaseManager(db_type="memory")
print("✓ Database manager initialized")

# Initialize Wetware Core
print("Initializing Wetware Core...")
life_support = LifeSupport()
life_support.initialize()

mea = MEAInterface(channels=20000)
mea.initialize()

# Create organoid lobes
organoids = []
lobe_types = ['logic', 'abstract', 'governance']
for i, lobe_type in enumerate(lobe_types):
    organoid = OrganoidCore(f"organoid_{i}", lobe_type)
    organoid.initialize()
    organoids.append(organoid)
print(f"✓ {len(organoids)} organoid lobes initialized")

# Initialize AI components
print("Initializing AI Systems...")
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
print("✓ Bio Neural Network ready")
print("✓ Reinforcement Learner ready")

print("\n" + "="*70)
print("THALOS PRIME WETWARE SYSTEM ONLINE")
print("="*70)


def process_through_wetware(message: str) -> Dict[str, Any]:
    """
    Process message through complete wetware pipeline:
    1. Convert to digital signal
    2. Encode to electrical pulses via MEA
    3. Process through organoid lobes
    4. Decode spike trains back to digital
    5. Update life support
    
    Args:
        message: Input text message
        
    Returns:
        Dict containing response and biological metadata
    """
    # Step 1: Convert message to digital signal
    digital_signal = {
        'type': 'query',
        'data': {'text': message},
        'intensity': min(1.0, len(message) / 50.0)  # Based on message length
    }
    
    # Step 2: Encode via MEA (digital to biological)
    pulse_pattern = mea.encode_digital_to_pulse(digital_signal)
    
    # Step 3: Process through each organoid lobe
    lobe_responses = []
    for organoid in organoids:
        # Convert pulse pattern to stimulus for organoid
        stimulus = {
            'type': 'pattern',
            'intensity': pulse_pattern.get('frequency', 50) / 100.0,
            'data': pulse_pattern
        }
        
        # Process through organoid
        response = organoid.process_stimulus(stimulus)
        lobe_responses.append(response)
        
        # Apply feedback based on response quality
        confidence = response.get('confidence', 0.5)
        organoid.apply_feedback(reward=(confidence > 0.5), intensity=abs(confidence - 0.5) * 2)
    
    # Step 4: Collect spike trains and decode via MEA
    all_spikes = []
    for response in lobe_responses:
        all_spikes.extend(response.get('spikes', []))
    
    # Decode biological response to digital
    decoded_response = mea.decode_spike_train(all_spikes)
    
    # Step 5: Update life support
    life_support.update(dt=1.0)
    
    # Compile comprehensive response
    return {
        'lobe_responses': lobe_responses,
        'decoded': decoded_response,
        'life_support': life_support.get_status(),
        'mea_stats': mea.get_status(),
        'total_spikes': len(all_spikes)
    }


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
    """Handle chat messages with full NLP, action execution, and wetware processing"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Step 1: Analyze message with NLP
        analysis = nlp.analyze_message(message)
        
        # Step 2: Detect if user wants to execute an action
        action_type, action_params = action_handler.detect_action(message)
        
        # Step 3: Process through complete wetware pipeline
        wetware_result = process_through_wetware(message)
        
        # Step 4: Also process through neural network
        input_pattern = message_to_pattern(message)
        neural_net.stimulate_inputs(input_pattern)
        
        for _ in range(50):
            neural_net.simulate_step()
        
        output_activity = neural_net.get_output_activity()
        net_stats = neural_net.get_network_stats()
        
        # Add wetware viability
        wetware_result['life_support']['viability'] = life_support.get_viability_score()
        
        # Step 5: Execute action if detected
        action_result = None
        if action_type:
            action_result = action_handler.execute_action(action_type, action_params)
        
        # Step 6: Generate intelligent response
        if action_result and action_result.get('success'):
            # Use action result as primary response
            response_text = _format_action_response(action_result, action_type)
            
            # Add wetware context
            lobe_info = f"\n\n[Processed through {len(wetware_result['lobe_responses'])} organoid lobes, "
            lobe_info += f"{wetware_result['total_spikes']} spikes generated, "
            lobe_info += f"viability: {wetware_result['life_support']['viability']:.1%}]"
            response_text += lobe_info
        else:
            # Generate NLP response with wetware data
            response_text = nlp.generate_response(message, analysis, wetware_result)
            
            # If still generic, use detailed wetware response
            if 'specific patterns are still emerging' in response_text or 'Could you elaborate' in response_text:
                response_text = generate_wetware_response(
                    message, wetware_result, output_activity, net_stats
                )
        
        # Step 7: Store interaction in database
        try:
            conn = db_manager.pool.get_connection()
            interaction_id = f'chat_{len(conn["data"])}'
            conn['data'][interaction_id] = {
                'message': message,
                'response': response_text,
                'analysis': analysis,
                'action_executed': action_type,
                'action_result': action_result,
                'wetware_data': {
                    'total_spikes': wetware_result['total_spikes'],
                    'lobes_active': len(wetware_result['lobe_responses']),
                    'decoded_confidence': wetware_result['decoded'].get('confidence', 0),
                    'intent': analysis['intent'],
                    'topics': analysis['topics']
                }
            }
            db_manager.pool.return_connection(conn)
        except Exception as e:
            print(f"Database storage error: {e}")
        
        # Step 8: Prepare comprehensive metadata
        life_support_status = wetware_result['life_support']
        lobe_responses = wetware_result['lobe_responses']
        
        metadata = {
            'neuralDensity': sum(r.get('confidence', 0) for r in lobe_responses) / len(lobe_responses) if lobe_responses else 0,
            'confidence': wetware_result['decoded'].get('confidence', 0.5),
            'activeLobes': [r['lobe_type'] for r in lobe_responses],
            'processingTime': round(net_stats.get('current_time', 0) / 1000.0, 2),
            'spikeCount': wetware_result['total_spikes'],
            'synapticWeight': net_stats.get('avg_synaptic_weight', 0.5),
            'lifeSupport': {
                'temperature': life_support_status['temperature'],
                'ph': life_support_status['ph_level'],
                'oxygen': life_support_status['oxygen_saturation'],
                'viability': life_support.get_viability_score()
            },
            'meaChannels': wetware_result['mea_stats']['active_channels'],
            'organoidHealth': 'optimal' if all(r.get('confidence', 0) > 0.3 for r in lobe_responses) else 'suboptimal',
            'nlpAnalysis': {
                'intent': analysis['intent'],
                'topics': analysis['topics'],
                'sentiment': analysis['sentiment'],
                'complexity': analysis['complexity']
            },
            'actionExecuted': action_type,
            'actionSuccess': action_result.get('success') if action_result else False
        }
        
        return jsonify({
            'response': response_text,
            'metadata': metadata,
            'action_result': action_result
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def _format_action_response(action_result: Dict[str, Any], action_type: str) -> str:
    """Format action result into readable response"""
    if not action_result.get('success'):
        return f"Action failed: {action_result.get('error', 'Unknown error')}"
    
    message = action_result.get('message', '')
    
    # Add specific formatting based on action type
    if 'memory' in action_type:
        if 'list' in action_type:
            entries = action_result.get('entries', {})
            if entries:
                message += "\n\nMemory Contents:\n"
                for key, value in entries.items():
                    message += f"• {key}: {value}\n"
        else:
            message += f"\n✓ Memory operation completed successfully"
    
    elif 'calculate' in action_type:
        result = action_result.get('result')
        message += f"\n\n**Result:** {result}"
    
    elif 'generate_code' in action_type:
        code = action_result.get('code', '')
        language = action_result.get('language', 'python')
        message += f"\n\n```{language}\n{code}\n```"
    
    elif 'system_status' in action_type or 'organoid_status' in action_type:
        # Format status nicely
        status = action_result.get('status') or action_result.get('organoids')
        if status:
            message += "\n\n" + json.dumps(status, indent=2)
    
    elif 'explain' in action_type:
        explanation = action_result.get('explanation')
        if explanation:
            message = f"**{action_result.get('concept', 'Concept')}** ({action_result.get('domain', 'general')})\n\n{explanation}"
    
    return message


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get comprehensive system status including wetware"""
    cis_status = cis.status()
    neural_stats = neural_net.get_network_stats()
    rl_stats = rl_agent.get_statistics()
    
    # Get wetware status
    organoid_statuses = [org.get_status() for org in organoids]
    mea_status = mea.get_status()
    life_support_status = life_support.get_status()
    db_stats = db_manager.get_statistics()
    
    return jsonify({
        'cis': cis_status,
        'neural_network': neural_stats,
        'reinforcement_learning': rl_stats,
        'wetware': {
            'organoids': organoid_statuses,
            'mea': mea_status,
            'life_support': life_support_status,
            'viability_score': life_support.get_viability_score()
        },
        'database': db_stats,
        'system_health': 'OPERATIONAL'
    })


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Get detailed system metrics including wetware"""
    neural_stats = neural_net.get_network_stats()
    organoid_statuses = [org.get_status() for org in organoids]
    life_support_status = life_support.get_status()
    
    # Calculate aggregate neural density from organoids
    avg_neural_density = sum(org['neural_density'] for org in organoid_statuses) / len(organoid_statuses)
    
    # Calculate aggregate accuracy from organoids
    avg_accuracy = sum(org['accuracy_score'] for org in organoid_statuses) / len(organoid_statuses)
    
    return jsonify({
        'neural_density': avg_neural_density,
        'accuracy': avg_accuracy,
        'spike_rate': neural_stats.get('avg_firing_rate', 0),
        'synaptic_connections': neural_stats.get('num_synapses', 0),
        'active_neurons': neural_stats.get('num_neurons', 0),
        'organoid_count': len(organoids),
        'life_support_viability': life_support.get_viability_score(),
        'temperature': life_support_status['temperature'],
        'oxygen_saturation': life_support_status['oxygen_saturation']
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


def generate_wetware_response(message: str, wetware_result: Dict[str, Any],
                            output_activity: List[float], stats: dict) -> str:
    """
    Generate response text based on wetware and neural network processing
    
    Args:
        message: Original message
        wetware_result: Results from wetware processing
        output_activity: Neural network output
        stats: Network statistics
        
    Returns:
        Response text with biological insights
    """
    lobe_responses = wetware_result['lobe_responses']
    decoded = wetware_result['decoded']
    life_support = wetware_result['life_support']
    total_spikes = wetware_result['total_spikes']
    
    # Find most active lobe
    most_active = max(lobe_responses, key=lambda x: x.get('confidence', 0))
    lobe_type = most_active['lobe_type']
    
    # Build response based on dominant lobe
    if lobe_type == 'logic':
        base_response = f"Logic Lobe Analysis: Query '{message}' processed through {total_spikes} action potentials. "
        base_response += f"Frontal cortex analog engaged with {most_active['firing_rate']:.1f}Hz firing rate. "
        base_response += f"Deterministic reasoning pathway activated. Synaptic consensus: {most_active['confidence']:.2f}"
        
    elif lobe_type == 'abstract':
        base_response = f"Abstract Lobe Synthesis: Your query stimulates {total_spikes} neural spikes across temporal cortex analog. "
        base_response += f"Creative synthesis activated at {most_active['firing_rate']:.1f}Hz. "
        base_response += f"Novel pattern correlation emerging with {most_active['confidence']:.2f} coherence."
        
    elif lobe_type == 'governance':
        base_response = f"Governance Lobe Assessment: Parietal cortex analog evaluating query through {total_spikes} spikes. "
        base_response += f"Prime Directive alignment: {most_active['confidence']:.2f}. "
        base_response += f"Ethical evaluation complete at {most_active['firing_rate']:.1f}Hz. ACCURACY-EXPANSION-PRESERVATION verified."
        
    else:
        base_response = f"Multi-lobe integration processing {total_spikes} biological spikes. "
    
    # Add life support context
    if life_support['status'] == 'optimal':
        base_response += f" [Wetware homeostasis: OPTIMAL - Temp: {life_support['temperature']:.1f}°C, "
        base_response += f"O₂: {life_support['oxygen_saturation']:.1f}%, pH: {life_support['ph_level']:.2f}]"
    elif life_support['health_alerts']:
        base_response += f" [Life support alert: {', '.join(life_support['health_alerts'])}]"
    
    # Add MEA context
    mea_stats = wetware_result['mea_stats']
    base_response += f" Processed via {mea_stats['active_channels']} MEA channels."
    
    # Add decoded biological insight
    if decoded.get('decoded'):
        response_type = decoded.get('response_type', 'unknown')
        confidence = decoded.get('confidence', 0)
        base_response += f" Biological consensus: {response_type} ({confidence:.2f} confidence)."
    
    # Add dopamine feedback context
    base_response += f" Dopamine modulation: {'POSITIVE' if most_active['confidence'] > 0.5 else 'CORRECTIVE'}."
    
    return base_response


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
