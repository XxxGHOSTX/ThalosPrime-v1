"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Reinforcement Learner - Q-Learning and Actor-Critic Methods

Real reinforcement learning implementation modeling dopaminergic reward systems:
- Q-learning with experience replay
- Actor-Critic architecture
- Reward prediction error (dopamine-like signals)
- Policy gradient methods
"""

import random
import math
import ast
from typing import Dict, List, Tuple, Any, Optional
from collections import deque


class ReinforcementLearner:
    """
    Reinforcement learning system with biological reward mechanisms
    """
    
    def __init__(self, state_dim: int, action_dim: int, learning_rate: float = 0.01):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        
        # Q-table for discrete states/actions
        self.q_table: Dict[Tuple, List[float]] = {}
        
        # Experience replay buffer
        self.memory = deque(maxlen=10000)
        self.batch_size = 32
        
        # Learning parameters
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        
        # Dopamine-like reward prediction
        self.reward_baseline = 0.0
        self.reward_history = deque(maxlen=100)
        
        # Statistics
        self.total_updates = 0
        self.total_reward = 0.0
        
    def get_state_key(self, state: List[float]) -> Tuple:
        """Convert continuous state to discrete key"""
        # Discretize state for Q-table lookup
        return tuple(round(s, 2) for s in state)
        
    def get_action(self, state: List[float], training: bool = True) -> int:
        """
        Select action using epsilon-greedy policy
        
        Args:
            state: Current state
            training: Whether in training mode
            
        Returns:
            Selected action index
        """
        state_key = self.get_state_key(state)
        
        # Initialize Q-values if state not seen
        if state_key not in self.q_table:
            self.q_table[state_key] = [0.0] * self.action_dim
            
        # Epsilon-greedy exploration
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            # Exploit: choose best action
            return self.q_table[state_key].index(max(self.q_table[state_key]))
            
    def store_experience(self, state: List[float], action: int, 
                        reward: float, next_state: List[float], done: bool) -> None:
        """
        Store experience in replay buffer
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
            done: Whether episode ended
        """
        self.memory.append((state, action, reward, next_state, done))
        self.reward_history.append(reward)
        self.total_reward += reward
        
    def calculate_reward_prediction_error(self, reward: float) -> float:
        """
        Calculate reward prediction error (dopamine-like signal)
        
        Args:
            reward: Actual reward received
            
        Returns:
            Reward prediction error
        """
        # Update baseline (expected reward)
        if self.reward_history:
            self.reward_baseline = sum(self.reward_history) / len(self.reward_history)
            
        # RPE = actual - predicted
        rpe = reward - self.reward_baseline
        return rpe
        
    def update(self, state: List[float], action: int, reward: float,
              next_state: List[float], done: bool) -> float:
        """
        Update Q-values using Q-learning
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
            done: Whether episode ended
            
        Returns:
            TD error (similar to dopamine signal)
        """
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        # Initialize if needed
        if state_key not in self.q_table:
            self.q_table[state_key] = [0.0] * self.action_dim
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = [0.0] * self.action_dim
            
        # Calculate TD error (reward prediction error)
        current_q = self.q_table[state_key][action]
        
        if done:
            target_q = reward
        else:
            max_next_q = max(self.q_table[next_state_key])
            target_q = reward + self.gamma * max_next_q
            
        td_error = target_q - current_q
        
        # Update Q-value
        self.q_table[state_key][action] += self.learning_rate * td_error
        
        self.total_updates += 1
        
        # Decay exploration
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
        return td_error
        
    def replay_experience(self) -> Optional[float]:
        """
        Train on batch of experiences from replay buffer
        
        Returns:
            Average TD error from batch, or None if not enough experiences
        """
        if len(self.memory) < self.batch_size:
            return None
            
        # Sample random batch
        batch = random.sample(self.memory, self.batch_size)
        
        total_td_error = 0.0
        
        for state, action, reward, next_state, done in batch:
            td_error = self.update(state, action, reward, next_state, done)
            total_td_error += abs(td_error)
            
        return total_td_error / self.batch_size
        
    def get_policy(self, state: List[float]) -> List[float]:
        """
        Get action probabilities for state
        
        Args:
            state: Current state
            
        Returns:
            Probability distribution over actions
        """
        state_key = self.get_state_key(state)
        
        if state_key not in self.q_table:
            # Uniform distribution if unseen
            return [1.0 / self.action_dim] * self.action_dim
            
        q_values = self.q_table[state_key]
        
        # Softmax to get probabilities
        exp_q = [math.exp(q) for q in q_values]
        sum_exp = sum(exp_q)
        
        return [eq / sum_exp for eq in exp_q]
        
    def get_value_function(self, state: List[float]) -> float:
        """
        Get state value estimate
        
        Args:
            state: State to evaluate
            
        Returns:
            Estimated value of state
        """
        state_key = self.get_state_key(state)
        
        if state_key not in self.q_table:
            return 0.0
            
        # State value is max Q-value
        return max(self.q_table[state_key])
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            "total_updates": self.total_updates,
            "total_reward": round(self.total_reward, 2),
            "epsilon": round(self.epsilon, 4),
            "states_explored": len(self.q_table),
            "memory_size": len(self.memory),
            "reward_baseline": round(self.reward_baseline, 4),
            "avg_recent_reward": round(sum(self.reward_history) / len(self.reward_history), 4) if self.reward_history else 0.0
        }
        
    def save_policy(self) -> Dict[str, Any]:
        """Save learned policy"""
        return {
            "q_table": {str(k): v for k, v in self.q_table.items()},
            "parameters": {
                "state_dim": self.state_dim,
                "action_dim": self.action_dim,
                "learning_rate": self.learning_rate,
                "gamma": self.gamma,
                "epsilon": self.epsilon
            }
        }
        
    def load_policy(self, policy_data: Dict[str, Any]) -> None:
        """Load saved policy"""
        # Convert string keys back to tuples
        self.q_table = {ast.literal_eval(k): v for k, v in policy_data["q_table"].items()}
        
        params = policy_data["parameters"]
        self.learning_rate = params["learning_rate"]
        self.gamma = params["gamma"]
        self.epsilon = params["epsilon"]


class ActorCritic:
    """
    Actor-Critic reinforcement learning with separate policy and value networks
    """
    
    def __init__(self, state_dim: int, action_dim: int):
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # Actor network (policy) - simple linear model
        self.actor_weights = [[random.uniform(-0.1, 0.1) for _ in range(state_dim)] 
                             for _ in range(action_dim)]
        self.actor_bias = [0.0] * action_dim
        
        # Critic network (value function) - simple linear model  
        self.critic_weights = [random.uniform(-0.1, 0.1) for _ in range(state_dim)]
        self.critic_bias = 0.0
        
        # Learning rates
        self.actor_lr = 0.001
        self.critic_lr = 0.01
        
        # Discount factor
        self.gamma = 0.99
        
    def get_action_probs(self, state: List[float]) -> List[float]:
        """Get action probabilities from actor network"""
        # Linear transformation
        logits = []
        for i in range(self.action_dim):
            logit = sum(w * s for w, s in zip(self.actor_weights[i], state)) + self.actor_bias[i]
            logits.append(logit)
            
        # Softmax
        exp_logits = [math.exp(l) for l in logits]
        sum_exp = sum(exp_logits)
        
        return [e / sum_exp for e in exp_logits]
        
    def get_state_value(self, state: List[float]) -> float:
        """Get state value from critic network"""
        value = sum(w * s for w, s in zip(self.critic_weights, state)) + self.critic_bias
        return value
        
    def select_action(self, state: List[float]) -> int:
        """Select action from policy"""
        probs = self.get_action_probs(state)
        
        # Sample from distribution
        rand = random.random()
        cumulative = 0.0
        for i, prob in enumerate(probs):
            cumulative += prob
            if rand < cumulative:
                return i
        return len(probs) - 1
        
    def update(self, state: List[float], action: int, reward: float, 
              next_state: List[float], done: bool) -> Tuple[float, float]:
        """
        Update actor and critic
        
        Returns:
            Tuple of (actor_loss, critic_loss)
        """
        # Compute TD error (advantage)
        current_value = self.get_state_value(state)
        
        if done:
            target_value = reward
        else:
            next_value = self.get_state_value(next_state)
            target_value = reward + self.gamma * next_value
            
        td_error = target_value - current_value
        
        # Update critic (value network)
        for i in range(self.state_dim):
            self.critic_weights[i] += self.critic_lr * td_error * state[i]
        self.critic_bias += self.critic_lr * td_error
        
        # Update actor (policy network)
        action_probs = self.get_action_probs(state)
        
        for i in range(self.action_dim):
            if i == action:
                # Increase probability of taken action if advantage is positive
                gradient = (1.0 - action_probs[i]) * td_error
            else:
                # Decrease probability of other actions if advantage is positive
                gradient = -action_probs[i] * td_error
                
            for j in range(self.state_dim):
                self.actor_weights[i][j] += self.actor_lr * gradient * state[j]
            self.actor_bias[i] += self.actor_lr * gradient
            
        return abs(td_error), abs(td_error)
