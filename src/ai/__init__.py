"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
AI Module - Synthetic Biological Intelligence

Real machine learning and neural network implementations modeling biological cognition:
- Neural networks with biological-inspired architectures
- Reinforcement learning with dopamine-like reward systems
- Pattern recognition and associative memory
- Reasoning and decision-making engines
"""

from .neural.bio_neural_network import BioNeuralNetwork
from .learning.reinforcement_learner import ReinforcementLearner
from .learning.hebbian_learner import HebbianLearner
from .reasoning.logic_engine import LogicEngine
from .reasoning.inference_engine import InferenceEngine
from .perception.pattern_recognizer import PatternRecognizer

__all__ = [
    'BioNeuralNetwork',
    'ReinforcementLearner', 
    'HebbianLearner',
    'LogicEngine',
    'InferenceEngine',
    'PatternRecognizer'
]
