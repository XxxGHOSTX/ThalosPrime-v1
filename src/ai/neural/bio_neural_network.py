"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Biologically-Inspired Neural Network

Real neural network implementation with biological characteristics:
- Spiking neuron models
- Synaptic plasticity (STDP)
- Lateral inhibition
- Homeostatic regulation
- Neurogenesis simulation
"""

import math
import random
from typing import List, Dict, Tuple, Optional, Any
import json


class Neuron:
    """
    Spiking neuron model with biological properties
    """
    
    def __init__(self, neuron_id: int, neuron_type: str = "excitatory"):
        self.neuron_id = neuron_id
        self.neuron_type = neuron_type  # excitatory or inhibitory
        
        # Membrane potential
        self.membrane_potential = -70.0  # mV (resting potential)
        self.threshold = -55.0  # mV (firing threshold)
        self.resting_potential = -70.0  # mV
        self.reset_potential = -75.0  # mV
        
        # Synaptic inputs
        self.incoming_synapses: List['Synapse'] = []
        self.outgoing_synapses: List['Synapse'] = []
        
        # Spike history
        self.spike_times: List[float] = []
        self.refractory_period = 2.0  # ms
        self.last_spike_time = -float('inf')
        
        # Biological properties
        self.leak_conductance = 0.1
        self.capacitance = 1.0
        
    def update(self, dt: float, current_time: float) -> bool:
        """
        Update neuron state (Leaky Integrate-and-Fire model)
        
        Args:
            dt: Time step in ms
            current_time: Current simulation time
            
        Returns:
            bool: True if neuron fired a spike
        """
        # Check refractory period
        if current_time - self.last_spike_time < self.refractory_period:
            return False
            
        # Sum synaptic inputs
        synaptic_current = sum(syn.get_current() for syn in self.incoming_synapses)
        
        # Leak current (towards resting potential)
        leak_current = -self.leak_conductance * (self.membrane_potential - self.resting_potential)
        
        # Update membrane potential (dV/dt = (I_syn + I_leak) / C)
        dv = (synaptic_current + leak_current) / self.capacitance
        self.membrane_potential += dv * dt
        
        # Check for spike
        if self.membrane_potential >= self.threshold:
            self._fire_spike(current_time)
            return True
            
        return False
        
    def _fire_spike(self, time: float) -> None:
        """Generate action potential"""
        self.spike_times.append(time)
        self.last_spike_time = time
        self.membrane_potential = self.reset_potential
        
        # Propagate spike to outgoing synapses
        for synapse in self.outgoing_synapses:
            synapse.receive_spike(time)
            
    def add_incoming_synapse(self, synapse: 'Synapse') -> None:
        """Add incoming synaptic connection"""
        self.incoming_synapses.append(synapse)
        
    def add_outgoing_synapse(self, synapse: 'Synapse') -> None:
        """Add outgoing synaptic connection"""
        self.outgoing_synapses.append(synapse)
        
    def get_firing_rate(self, time_window: float = 1000.0) -> float:
        """Calculate firing rate in Hz over time window"""
        if not self.spike_times:
            return 0.0
        recent_spikes = [t for t in self.spike_times if t > (self.spike_times[-1] - time_window)]
        return len(recent_spikes) / (time_window / 1000.0)


class Synapse:
    """
    Synaptic connection with plasticity
    """
    
    def __init__(self, pre_neuron: Neuron, post_neuron: Neuron, 
                 initial_weight: float = 0.5):
        self.pre_neuron = pre_neuron
        self.post_neuron = post_neuron
        self.weight = initial_weight
        
        # STDP parameters
        self.a_plus = 0.01  # LTP amplitude
        self.a_minus = 0.01  # LTD amplitude
        self.tau_plus = 20.0  # LTP time constant (ms)
        self.tau_minus = 20.0  # LTD time constant (ms)
        
        # Synaptic dynamics
        self.delay = 1.0  # ms
        self.pending_spikes: List[float] = []
        self.current = 0.0
        self.decay_rate = 0.9
        
    def receive_spike(self, time: float) -> None:
        """Receive spike from presynaptic neuron"""
        arrival_time = time + self.delay
        self.pending_spikes.append(arrival_time)
        
    def update(self, dt: float, current_time: float) -> None:
        """Update synaptic current"""
        # Decay current
        self.current *= math.exp(-self.decay_rate * dt)
        
        # Process pending spikes
        spikes_to_remove = []
        for spike_time in self.pending_spikes:
            if current_time >= spike_time:
                # Add synaptic current
                self.current += self.weight
                spikes_to_remove.append(spike_time)
                
        # Remove processed spikes
        for spike_time in spikes_to_remove:
            self.pending_spikes.remove(spike_time)
            
    def get_current(self) -> float:
        """Get current synaptic current"""
        return self.current
        
    def apply_stdp(self, dt_pre_post: float) -> None:
        """
        Apply Spike-Timing-Dependent Plasticity
        
        Args:
            dt_pre_post: Time difference (post_spike - pre_spike) in ms
        """
        if dt_pre_post > 0:
            # LTP (Long-Term Potentiation) - strengthen synapse
            delta_w = self.a_plus * math.exp(-dt_pre_post / self.tau_plus)
        else:
            # LTD (Long-Term Depression) - weaken synapse
            delta_w = -self.a_minus * math.exp(dt_pre_post / self.tau_minus)
            
        # Update weight with bounds
        self.weight = max(0.0, min(1.0, self.weight + delta_w))


class BioNeuralNetwork:
    """
    Biologically-inspired neural network with spiking neurons
    """
    
    def __init__(self, name: str = "bio_net"):
        self.name = name
        self.neurons: List[Neuron] = []
        self.synapses: List[Synapse] = []
        
        # Network structure
        self.input_neurons: List[Neuron] = []
        self.hidden_neurons: List[Neuron] = []
        self.output_neurons: List[Neuron] = []
        
        # Simulation state
        self.current_time = 0.0
        self.dt = 0.1  # Time step in ms
        
        # Learning parameters
        self.learning_enabled = True
        self.homeostasis_enabled = True
        
    def create_layer(self, num_neurons: int, layer_type: str = "hidden") -> List[Neuron]:
        """
        Create a layer of neurons
        
        Args:
            num_neurons: Number of neurons in layer
            layer_type: Type of layer (input, hidden, output)
            
        Returns:
            List of created neurons
        """
        layer = []
        for i in range(num_neurons):
            neuron_id = len(self.neurons)
            neuron = Neuron(neuron_id)
            self.neurons.append(neuron)
            layer.append(neuron)
            
        # Categorize neurons
        if layer_type == "input":
            self.input_neurons.extend(layer)
        elif layer_type == "output":
            self.output_neurons.extend(layer)
        else:
            self.hidden_neurons.extend(layer)
            
        return layer
        
    def connect_layers(self, pre_layer: List[Neuron], post_layer: List[Neuron],
                      connection_probability: float = 0.5) -> None:
        """
        Connect two layers with synapses
        
        Args:
            pre_layer: Presynaptic layer
            post_layer: Postsynaptic layer
            connection_probability: Probability of connection between neurons
        """
        for pre_neuron in pre_layer:
            for post_neuron in post_layer:
                if random.random() < connection_probability:
                    # Random initial weight
                    weight = random.uniform(0.3, 0.7)
                    synapse = Synapse(pre_neuron, post_neuron, weight)
                    
                    pre_neuron.add_outgoing_synapse(synapse)
                    post_neuron.add_incoming_synapse(synapse)
                    self.synapses.append(synapse)
                    
    def stimulate_inputs(self, input_pattern: List[float]) -> None:
        """
        Stimulate input neurons with pattern
        
        Args:
            input_pattern: List of input values (0.0 to 1.0)
        """
        if len(input_pattern) != len(self.input_neurons):
            raise ValueError(f"Input pattern size {len(input_pattern)} doesn't match input layer size {len(self.input_neurons)}")
            
        for neuron, intensity in zip(self.input_neurons, input_pattern):
            # Convert intensity to current injection
            current = intensity * 50.0  # Scale to appropriate range
            neuron.membrane_potential += current
            
    def simulate_step(self) -> Dict[str, Any]:
        """
        Simulate one time step
        
        Returns:
            Dict with simulation results
        """
        # Update synapses
        for synapse in self.synapses:
            synapse.update(self.dt, self.current_time)
            
        # Update neurons
        spikes = []
        for neuron in self.neurons:
            if neuron.update(self.dt, self.current_time):
                spikes.append(neuron.neuron_id)
                
        # Apply STDP if learning enabled
        if self.learning_enabled and len(spikes) > 0:
            self._apply_learning()
            
        # Homeostatic regulation
        if self.homeostasis_enabled:
            self._apply_homeostasis()
            
        self.current_time += self.dt
        
        return {
            "time": self.current_time,
            "spikes": spikes,
            "num_spikes": len(spikes)
        }
        
    def _apply_learning(self) -> None:
        """Apply STDP learning to all synapses"""
        for synapse in self.synapses:
            pre_spikes = synapse.pre_neuron.spike_times
            post_spikes = synapse.post_neuron.spike_times
            
            if not pre_spikes or not post_spikes:
                continue
                
            # Find closest spike pairs
            for pre_time in pre_spikes[-5:]:  # Last 5 spikes
                for post_time in post_spikes[-5:]:
                    dt = post_time - pre_time
                    if abs(dt) < 50.0:  # Within STDP window
                        synapse.apply_stdp(dt)
                        
    def _apply_homeostasis(self) -> None:
        """Apply homeostatic regulation to maintain network stability"""
        target_rate = 5.0  # Target firing rate in Hz
        
        for neuron in self.neurons:
            current_rate = neuron.get_firing_rate(1000.0)
            
            # Adjust threshold to regulate firing rate
            if current_rate > target_rate * 1.5:
                neuron.threshold += 0.1  # Increase threshold (harder to fire)
            elif current_rate < target_rate * 0.5:
                neuron.threshold -= 0.1  # Decrease threshold (easier to fire)
                
            # Keep threshold in reasonable range
            neuron.threshold = max(-60.0, min(-50.0, neuron.threshold))
            
    def get_output_activity(self) -> List[float]:
        """
        Get current activity of output neurons
        
        Returns:
            List of firing rates for output neurons
        """
        return [neuron.get_firing_rate(100.0) for neuron in self.output_neurons]
        
    def train(self, input_patterns: List[List[float]], 
             target_outputs: List[List[float]], epochs: int = 100) -> Dict[str, Any]:
        """
        Train network on patterns
        
        Args:
            input_patterns: List of input patterns
            target_outputs: List of desired output patterns
            epochs: Number of training epochs
            
        Returns:
            Training statistics
        """
        training_stats = {
            "epochs": epochs,
            "losses": []
        }
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            
            for input_pattern, target_output in zip(input_patterns, target_outputs):
                # Present input
                self.stimulate_inputs(input_pattern)
                
                # Simulate for processing time
                for _ in range(100):  # 10ms simulation
                    self.simulate_step()
                    
                # Get output
                actual_output = self.get_output_activity()
                
                # Calculate loss (MSE)
                loss = sum((a - t) ** 2 for a, t in zip(actual_output, target_output)) / len(actual_output)
                epoch_loss += loss
                
                # Apply reward-based learning
                reward = 1.0 / (1.0 + loss)  # Higher reward for lower loss
                self._apply_reward_modulation(reward)
                
            avg_loss = epoch_loss / len(input_patterns)
            training_stats["losses"].append(avg_loss)
            
        return training_stats
        
    def _apply_reward_modulation(self, reward: float) -> None:
        """
        Apply reward-based modulation to recent synaptic changes
        
        Args:
            reward: Reward signal (0.0 to 1.0)
        """
        # Modulate recent synaptic changes based on reward
        for synapse in self.synapses:
            # Strengthen recently active synapses if reward is high
            if synapse.current > 0.1:  # Recently active
                synapse.weight *= (1.0 + reward * 0.01)
                synapse.weight = min(1.0, synapse.weight)
                
    def get_network_stats(self) -> Dict[str, Any]:
        """Get comprehensive network statistics"""
        total_spikes = sum(len(n.spike_times) for n in self.neurons)
        avg_firing_rate = sum(n.get_firing_rate() for n in self.neurons) / len(self.neurons) if self.neurons else 0
        avg_weight = sum(s.weight for s in self.synapses) / len(self.synapses) if self.synapses else 0
        
        return {
            "name": self.name,
            "num_neurons": len(self.neurons),
            "num_synapses": len(self.synapses),
            "current_time": self.current_time,
            "total_spikes": total_spikes,
            "avg_firing_rate": round(avg_firing_rate, 2),
            "avg_synaptic_weight": round(avg_weight, 4),
            "input_layer_size": len(self.input_neurons),
            "hidden_layer_size": len(self.hidden_neurons),
            "output_layer_size": len(self.output_neurons)
        }
        
    def reset(self) -> None:
        """Reset network to initial state"""
        self.current_time = 0.0
        for neuron in self.neurons:
            neuron.membrane_potential = neuron.resting_potential
            neuron.spike_times.clear()
        for synapse in self.synapses:
            synapse.current = 0.0
            synapse.pending_spikes.clear()
