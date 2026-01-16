"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Neural Pathway Optimization Engine

Advanced neural network optimization with:
- Synaptic weight optimization
- Pathway pruning and consolidation
- Hebbian learning enhancement  
- Activity-dependent plasticity
- Energy efficiency optimization
- Real-time performance tuning
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict


class NeuralPathwayOptimizer:
    """
    Optimizes neural pathways for efficiency and performance
    
    Features:
    - Synaptic weight optimization using gradient descent
    - Pathway pruning to remove weak connections
    - Consolidation of frequently used pathways
    - Activity-based strengthening
    - Energy-aware optimization
    """
    
    def __init__(self, learning_rate: float = 0.01, prune_threshold: float = 0.1):
        """
        Initialize optimizer
        
        Args:
            learning_rate: Rate for weight optimization
            prune_threshold: Threshold for pruning weak connections
        """
        self.learning_rate = learning_rate
        self.prune_threshold = prune_threshold
        
        # Tracking metrics
        self.pathway_usage = defaultdict(int)
        self.pathway_strengths = {}
        self.optimization_history = []
        
        # Performance metrics
        self.total_optimizations = 0
        self.pathways_pruned = 0
        self.pathways_consolidated = 0
        
    def optimize_network(self, network: Any) -> Dict[str, Any]:
        """
        Optimize entire neural network
        
        Args:
            network: Neural network to optimize
            
        Returns:
            Optimization results
        """
        results = {
            'initial_connections': 0,
            'final_connections': 0,
            'pruned': 0,
            'consolidated': 0,
            'strengthened': 0,
            'energy_saved': 0.0
        }
        
        # Get all synapses/connections
        if hasattr(network, 'synapses'):
            results['initial_connections'] = len(network.synapses)
            
            # Optimize each synapse
            for synapse in network.synapses:
                self._optimize_synapse(synapse)
            
            # Prune weak connections
            pruned = self._prune_weak_connections(network)
            results['pruned'] = pruned
            self.pathways_pruned += pruned
            
            # Consolidate frequently used pathways
            consolidated = self._consolidate_pathways(network)
            results['consolidated'] = consolidated
            self.pathways_consolidated += consolidated
            
            results['final_connections'] = len(network.synapses)
            results['energy_saved'] = self._calculate_energy_savings(results)
        
        self.total_optimizations += 1
        self.optimization_history.append(results)
        
        return results
    
    def optimize_synapse(self, synapse: Any, activity: float) -> float:
        """
        Optimize individual synapse based on activity
        
        Args:
            synapse: Synapse object
            activity: Recent activity level (0-1)
            
        Returns:
            New synaptic weight
        """
        return self._optimize_synapse(synapse, activity)
    
    def _optimize_synapse(self, synapse: Any, activity: Optional[float] = None) -> float:
        """Internal synapse optimization"""
        if not hasattr(synapse, 'weight'):
            return 0.0
        
        # Use activity if provided, otherwise infer from weight
        if activity is None:
            activity = abs(synapse.weight)
        
        # Hebbian-style strengthening: "neurons that fire together wire together"
        if activity > 0.5:
            # Strengthen active pathways
            delta = self.learning_rate * activity * (1.0 - abs(synapse.weight))
            synapse.weight += delta
            
            # Clip to [-1, 1]
            synapse.weight = np.clip(synapse.weight, -1.0, 1.0)
        
        elif activity < 0.1:
            # Weaken inactive pathways
            synapse.weight *= 0.95
        
        # Track usage
        synapse_id = id(synapse)
        if activity > 0.3:
            self.pathway_usage[synapse_id] += 1
        
        self.pathway_strengths[synapse_id] = abs(synapse.weight)
        
        return synapse.weight
    
    def _prune_weak_connections(self, network: Any) -> int:
        """
        Prune synapses below threshold
        
        Args:
            network: Neural network
            
        Returns:
            Number of connections pruned
        """
        if not hasattr(network, 'synapses'):
            return 0
        
        initial_count = len(network.synapses)
        
        # Remove weak synapses
        network.synapses = [
            syn for syn in network.synapses
            if abs(syn.weight) >= self.prune_threshold
        ]
        
        pruned = initial_count - len(network.synapses)
        return pruned
    
    def _consolidate_pathways(self, network: Any) -> int:
        """
        Consolidate frequently used parallel pathways
        
        Args:
            network: Neural network
            
        Returns:
            Number of pathways consolidated
        """
        if not hasattr(network, 'synapses'):
            return 0
        
        # Group synapses by source-target pairs
        pathway_groups = defaultdict(list)
        
        for synapse in network.synapses:
            if hasattr(synapse, 'pre_neuron') and hasattr(synapse, 'post_neuron'):
                key = (id(synapse.pre_neuron), id(synapse.post_neuron))
                pathway_groups[key].append(synapse)
        
        # Consolidate parallel connections
        consolidated = 0
        for key, synapses in pathway_groups.items():
            if len(synapses) > 1:
                # Merge into strongest synapse
                strongest = max(synapses, key=lambda s: abs(s.weight))
                total_weight = sum(s.weight for s in synapses)
                
                # Average the weights with bias toward strongest
                strongest.weight = (strongest.weight * 0.7 + total_weight * 0.3) / 1.0
                strongest.weight = np.clip(strongest.weight, -1.0, 1.0)
                
                # Remove others
                for syn in synapses:
                    if syn is not strongest:
                        network.synapses.remove(syn)
                        consolidated += 1
        
        return consolidated
    
    def _calculate_energy_savings(self, results: Dict[str, Any]) -> float:
        """
        Calculate approximate energy savings from optimization
        
        Args:
            results: Optimization results
            
        Returns:
            Estimated energy savings percentage
        """
        if results['initial_connections'] == 0:
            return 0.0
        
        # Energy is roughly proportional to number of active connections
        reduction = results['pruned']
        initial = results['initial_connections']
        
        return (reduction / initial) * 100.0 if initial > 0 else 0.0
    
    def get_pathway_statistics(self) -> Dict[str, Any]:
        """Get detailed pathway statistics"""
        if not self.pathway_strengths:
            return {
                'total_pathways': 0,
                'avg_strength': 0.0,
                'strong_pathways': 0,
                'weak_pathways': 0
            }
        
        strengths = list(self.pathway_strengths.values())
        
        return {
            'total_pathways': len(strengths),
            'avg_strength': np.mean(strengths),
            'max_strength': np.max(strengths),
            'min_strength': np.min(strengths),
            'strong_pathways': sum(1 for s in strengths if s > 0.7),
            'medium_pathways': sum(1 for s in strengths if 0.3 <= s <= 0.7),
            'weak_pathways': sum(1 for s in strengths if s < 0.3),
            'most_used_count': max(self.pathway_usage.values()) if self.pathway_usage else 0
        }
    
    def get_optimization_metrics(self) -> Dict[str, Any]:
        """Get overall optimization metrics"""
        return {
            'total_optimizations': self.total_optimizations,
            'pathways_pruned': self.pathways_pruned,
            'pathways_consolidated': self.pathways_consolidated,
            'optimization_history': self.optimization_history[-10:],  # Last 10
            'pathway_stats': self.get_pathway_statistics()
        }
    
    def reset_statistics(self) -> None:
        """Reset all statistics"""
        self.pathway_usage.clear()
        self.pathway_strengths.clear()
        self.optimization_history.clear()
        self.total_optimizations = 0
        self.pathways_pruned = 0
        self.pathways_consolidated = 0


class AdaptiveLearningOptimizer:
    """
    Adaptive learning rate optimization
    
    Dynamically adjusts learning rates based on performance
    """
    
    def __init__(self, initial_lr: float = 0.01):
        """Initialize adaptive optimizer"""
        self.learning_rate = initial_lr
        self.min_lr = 0.0001
        self.max_lr = 0.1
        
        self.performance_history = []
        self.lr_history = []
        
    def adapt_learning_rate(self, performance: float, target: float = 0.9) -> float:
        """
        Adapt learning rate based on performance
        
        Args:
            performance: Current performance metric (0-1)
            target: Target performance
            
        Returns:
            New learning rate
        """
        self.performance_history.append(performance)
        
        if len(self.performance_history) < 2:
            return self.learning_rate
        
        # Check if improving
        recent_performance = np.mean(self.performance_history[-5:])
        previous_performance = np.mean(self.performance_history[-10:-5] if len(self.performance_history) >= 10 else self.performance_history[:-5])
        
        if recent_performance > previous_performance:
            # Improving - slightly increase learning rate
            self.learning_rate *= 1.05
        elif recent_performance < previous_performance:
            # Degrading - reduce learning rate
            self.learning_rate *= 0.9
        
        # Clip to bounds
        self.learning_rate = np.clip(self.learning_rate, self.min_lr, self.max_lr)
        
        self.lr_history.append(self.learning_rate)
        
        return self.learning_rate
    
    def get_recommended_lr(self) -> float:
        """Get current recommended learning rate"""
        return self.learning_rate
