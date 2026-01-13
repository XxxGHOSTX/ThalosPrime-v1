"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime is an original proprietary software system, including but not limited to
its source code, system architecture, internal logic descriptions, documentation,
interfaces, diagrams, and design materials.

Unauthorized reproduction, modification, distribution, public display, or use of
this software or its associated materials is strictly prohibited without the
express written permission of the copyright holder.

Thalos Prime™ is a proprietary system.
"""

"""
Organoid Core - Brain Organoid Simulation/Interface

Represents the biological computing substrate:
- 3D brain organoids (cortical/hippocampal fused spheroids)
- Neural network state management
- Synaptic weight matrices
- Spike train processing
"""

from typing import Dict, List, Optional, Tuple, Any
import json
from datetime import datetime


class OrganoidCore:
    """
    Organoid Core - Biological Computing Substrate
    
    Simulates/interfaces with brain organoid clusters for massively parallel
    pattern recognition, intuition, and creative synthesis.
    
    Components:
    - Logic Lobe (Frontal): Linear reasoning and code generation
    - Abstract Lobe (Temporal): Creative synthesis and novel field generation
    - Governance Lobe (Parietal): Prime Directive enforcement and ethical weighting
    """
    
    def __init__(self, organoid_id: str, lobe_type: str = "logic"):
        """
        Initialize an organoid core instance
        
        Args:
            organoid_id: Unique identifier for this organoid
            lobe_type: Type of specialized lobe (logic, abstract, governance)
        """
        self.organoid_id = organoid_id
        self.lobe_type = lobe_type
        self.active = False
        self.health_status = "dormant"
        
        # Neural state
        self.synaptic_weights: Dict[str, float] = {}
        self.neural_density = 0.0
        self.plasticity_coefficient = 1.0
        
        # Processing state
        self.current_spike_train: List[Dict[str, Any]] = []
        self.processing_queue: List[Dict[str, Any]] = []
        
        # Performance metrics
        self.accuracy_score = 0.0
        self.creativity_index = 0.0
        self.ethical_alignment = 1.0
        
    def initialize(self) -> bool:
        """
        Initialize the organoid - bring it to operational state
        
        Returns:
            bool: True if initialization successful
        """
        if self.active:
            return True
            
        # Initialize default synaptic weights
        self._initialize_synaptic_weights()
        
        # Set initial neural density based on lobe type
        self.neural_density = self._get_initial_density()
        
        self.active = True
        self.health_status = "operational"
        return True
        
    def _initialize_synaptic_weights(self) -> None:
        """Initialize default synaptic connection weights"""
        # Simplified representation of synaptic connections
        base_connections = [
            "input_sensory", "pattern_recognition", "associative_memory",
            "executive_function", "creative_synthesis", "ethical_evaluation",
            "output_motor"
        ]
        
        for connection in base_connections:
            # Different lobes have different initial weight distributions
            if self.lobe_type == "logic":
                self.synaptic_weights[connection] = 0.7 if "executive" in connection else 0.5
            elif self.lobe_type == "abstract":
                self.synaptic_weights[connection] = 0.8 if "creative" in connection else 0.5
            elif self.lobe_type == "governance":
                self.synaptic_weights[connection] = 0.9 if "ethical" in connection else 0.5
            else:
                self.synaptic_weights[connection] = 0.5
                
    def _get_initial_density(self) -> float:
        """Get initial neural density based on lobe type"""
        densities = {
            "logic": 0.65,
            "abstract": 0.70,
            "governance": 0.75
        }
        return densities.get(self.lobe_type, 0.60)
        
    def process_stimulus(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming stimulus through the organoid
        
        Args:
            stimulus: Input stimulus containing pattern data
            
        Returns:
            Dict containing spike train response
        """
        if not self.active:
            return {"error": "Organoid not active", "spike_train": []}
            
        # Add to processing queue
        self.processing_queue.append(stimulus)
        
        # Generate spike train response based on stimulus and synaptic weights
        response = self._generate_spike_train(stimulus)
        
        # Update current spike train
        self.current_spike_train = response["spikes"]
        
        # Apply STDP (Spike-Timing-Dependent Plasticity) for learning
        self._apply_stdp(stimulus, response)
        
        return response
        
    def _generate_spike_train(self, stimulus: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate neural spike train response to stimulus
        
        Args:
            stimulus: Input pattern
            
        Returns:
            Spike train data structure
        """
        stimulus_type = stimulus.get("type", "unknown")
        intensity = stimulus.get("intensity", 0.5)
        
        # Calculate firing rate based on synaptic weights and stimulus
        base_rate = 10.0  # Hz
        modulated_rate = base_rate * intensity * self._get_weight_for_stimulus(stimulus_type)
        
        # Generate spike sequence (simplified)
        num_spikes = int(modulated_rate * 0.1)  # 100ms window
        spikes = []
        
        for i in range(num_spikes):
            spike = {
                "timestamp": i * (100.0 / num_spikes),  # ms
                "amplitude": intensity * (0.8 + 0.4 * (i / max(num_spikes, 1))),
                "channel": self._select_output_channel(stimulus_type)
            }
            spikes.append(spike)
            
        return {
            "organoid_id": self.organoid_id,
            "lobe_type": self.lobe_type,
            "spikes": spikes,
            "firing_rate": modulated_rate,
            "confidence": self._calculate_confidence(spikes)
        }
        
    def _get_weight_for_stimulus(self, stimulus_type: str) -> float:
        """Get appropriate synaptic weight for stimulus type"""
        weight_map = {
            "pattern": "pattern_recognition",
            "logic": "executive_function",
            "creative": "creative_synthesis",
            "ethical": "ethical_evaluation"
        }
        
        connection = weight_map.get(stimulus_type, "input_sensory")
        return self.synaptic_weights.get(connection, 0.5)
        
    def _select_output_channel(self, stimulus_type: str) -> str:
        """Select appropriate output channel based on processing"""
        channel_map = {
            "pattern": "pattern_output",
            "logic": "logic_output",
            "creative": "creative_output",
            "ethical": "governance_output"
        }
        return channel_map.get(stimulus_type, "general_output")
        
    def _calculate_confidence(self, spikes: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on spike train characteristics"""
        if not spikes:
            return 0.0
            
        # Confidence based on spike count and amplitude consistency
        avg_amplitude = sum(s["amplitude"] for s in spikes) / len(spikes)
        return min(1.0, avg_amplitude * len(spikes) / 10.0)
        
    def _apply_stdp(self, stimulus: Dict[str, Any], response: Dict[str, Any]) -> None:
        """
        Apply Spike-Timing-Dependent Plasticity for learning
        
        Strengthens or weakens synaptic connections based on spike timing
        """
        confidence = response.get("confidence", 0.5)
        stimulus_type = stimulus.get("type", "unknown")
        
        # Find relevant connection
        connection = self._get_weight_for_stimulus(stimulus_type)
        
        # Update synaptic weight based on response confidence
        if stimulus_type in ["pattern", "logic", "creative", "ethical"]:
            weight_key = list(self.synaptic_weights.keys())[0]  # Simplified
            current_weight = self.synaptic_weights.get(weight_key, 0.5)
            
            # STDP rule: increase weight if confident, decrease if not
            delta = (confidence - 0.5) * self.plasticity_coefficient * 0.01
            new_weight = max(0.1, min(1.0, current_weight + delta))
            
            self.synaptic_weights[weight_key] = new_weight
            
            # Update neural density (expansion principle)
            self.neural_density = min(1.0, self.neural_density + 0.001)
            
    def apply_feedback(self, reward: bool, intensity: float = 1.0) -> None:
        """
        Apply dopamine (reward) or inhibition (punishment) feedback
        
        Args:
            reward: True for reward (dopamine), False for punishment (inhibition)
            intensity: Strength of feedback (0.0 to 1.0)
        """
        if not self.active:
            return
            
        modifier = intensity if reward else -intensity
        
        # Update plasticity coefficient based on feedback
        self.plasticity_coefficient = max(0.1, min(2.0, 
            self.plasticity_coefficient + modifier * 0.1))
        
        # Update accuracy score
        self.accuracy_score = max(0.0, min(1.0,
            self.accuracy_score + modifier * 0.05))
            
    def get_status(self) -> Dict[str, Any]:
        """
        Get current organoid status
        
        Returns:
            Status dictionary with all key metrics
        """
        return {
            "organoid_id": self.organoid_id,
            "lobe_type": self.lobe_type,
            "active": self.active,
            "health_status": self.health_status,
            "neural_density": round(self.neural_density, 4),
            "plasticity_coefficient": round(self.plasticity_coefficient, 4),
            "accuracy_score": round(self.accuracy_score, 4),
            "creativity_index": round(self.creativity_index, 4),
            "ethical_alignment": round(self.ethical_alignment, 4),
            "synaptic_connections": len(self.synaptic_weights),
            "queue_depth": len(self.processing_queue)
        }
        
    def shutdown(self) -> bool:
        """
        Gracefully shutdown the organoid
        
        Returns:
            bool: True if shutdown successful
        """
        if not self.active:
            return True
            
        # Clear processing queue
        self.processing_queue.clear()
        self.current_spike_train.clear()
        
        self.active = False
        self.health_status = "dormant"
        return True
