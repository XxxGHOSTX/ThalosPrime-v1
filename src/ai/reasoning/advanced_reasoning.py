"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Advanced Reasoning Engine

Provides:
- Logical inference
- Causal reasoning
- Pattern-based deduction
- Symbolic reasoning
- Knowledge graph traversal
- Multi-step reasoning chains
"""

from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict, deque


class AdvancedReasoningEngine:
    """
    Advanced AI reasoning with inference and deduction
    
    Capabilities:
    - Forward and backward chaining
    - Abductive reasoning
    - Analogical reasoning
    - Causal inference
    - Probabilistic reasoning
    """
    
    def __init__(self):
        """Initialize reasoning engine"""
        # Knowledge base: facts and rules
        self.facts: Set[str] = set()
        self.rules: List[Dict[str, Any]] = []
        
        # Inference history
        self.inference_chain: List[Dict] = []
        
        # Causal graph
        self.causal_graph: Dict[str, Set[str]] = defaultdict(set)
        
        # Statistics
        self.inferences_made = 0
        self.rules_applied = 0
    
    def add_fact(self, fact: str) -> None:
        """Add a fact to knowledge base"""
        self.facts.add(fact)
    
    def add_rule(self, conditions: List[str], conclusion: str, 
                 confidence: float = 1.0) -> None:
        """
        Add inference rule
        
        Args:
            conditions: List of condition facts
            conclusion: Conclusion fact
            confidence: Rule confidence (0-1)
        """
        self.rules.append({
            'conditions': conditions,
            'conclusion': conclusion,
            'confidence': confidence,
            'applied_count': 0
        })
    
    def add_causal_relation(self, cause: str, effect: str) -> None:
        """Add causal relationship"""
        self.causal_graph[cause].add(effect)
    
    def forward_chain(self, max_iterations: int = 100) -> List[str]:
        """
        Forward chaining inference
        
        Derive new facts from existing facts and rules
        
        Args:
            max_iterations: Maximum inference iterations
            
        Returns:
            List of newly inferred facts
        """
        new_facts = []
        
        for iteration in range(max_iterations):
            facts_added_this_iteration = False
            
            for rule in self.rules:
                # Check if all conditions are satisfied
                if all(cond in self.facts for cond in rule['conditions']):
                    conclusion = rule['conclusion']
                    
                    # Add conclusion if new
                    if conclusion not in self.facts:
                        self.facts.add(conclusion)
                        new_facts.append(conclusion)
                        facts_added_this_iteration = True
                        
                        # Record inference
                        self.inference_chain.append({
                            'type': 'forward_chain',
                            'rule': rule,
                            'iteration': iteration,
                            'conclusion': conclusion
                        })
                        
                        rule['applied_count'] += 1
                        self.rules_applied += 1
                        self.inferences_made += 1
            
            # Stop if no new facts were derived
            if not facts_added_this_iteration:
                break
        
        return new_facts
    
    def backward_chain(self, goal: str, max_depth: int = 10) -> bool:
        """
        Backward chaining inference
        
        Check if goal can be proven from facts and rules
        
        Args:
            goal: Goal to prove
            max_depth: Maximum search depth
            
        Returns:
            Whether goal is provable
        """
        return self._backward_chain_recursive(goal, max_depth, set())
    
    def _backward_chain_recursive(self, goal: str, depth: int, 
                                   visited: Set[str]) -> bool:
        """Recursive backward chaining"""
        if depth <= 0:
            return False
        
        # Already proven?
        if goal in self.facts:
            return True
        
        # Avoid cycles
        if goal in visited:
            return False
        visited.add(goal)
        
        # Try to prove using rules
        for rule in self.rules:
            if rule['conclusion'] == goal:
                # Try to prove all conditions
                if all(self._backward_chain_recursive(cond, depth - 1, visited) 
                       for cond in rule['conditions']):
                    
                    # All conditions proven, add conclusion
                    self.facts.add(goal)
                    
                    self.inference_chain.append({
                        'type': 'backward_chain',
                        'rule': rule,
                        'depth': depth,
                        'goal': goal
                    })
                    
                    self.inferences_made += 1
                    return True
        
        return False
    
    def abductive_reasoning(self, observation: str) -> List[str]:
        """
        Abductive reasoning - find possible explanations
        
        Args:
            observation: Observed fact
            
        Returns:
            List of possible explanations
        """
        explanations = []
        
        # Find rules that could produce this observation
        for rule in self.rules:
            if rule['conclusion'] == observation:
                # Check if conditions are plausible
                plausibility = sum(1 for c in rule['conditions'] if c in self.facts)
                plausibility /= len(rule['conditions'])
                
                explanations.append({
                    'explanation': rule['conditions'],
                    'plausibility': plausibility * rule['confidence'],
                    'rule': rule
                })
        
        # Sort by plausibility
        explanations.sort(key=lambda x: x['plausibility'], reverse=True)
        
        return explanations
    
    def causal_inference(self, cause: str, max_depth: int = 5) -> List[str]:
        """
        Infer causal effects
        
        Args:
            cause: Starting cause
            max_depth: Maximum causal chain depth
            
        Returns:
            List of inferred effects
        """
        effects = []
        visited = set()
        queue = deque([(cause, 0)])
        
        while queue:
            current, depth = queue.popleft()
            
            if depth >= max_depth or current in visited:
                continue
            
            visited.add(current)
            
            # Get direct effects
            for effect in self.causal_graph.get(current, []):
                if effect not in visited:
                    effects.append(effect)
                    queue.append((effect, depth + 1))
        
        return effects
    
    def analogical_reasoning(self, source: str, target: str, 
                           mapping: Dict[str, str]) -> List[str]:
        """
        Analogical reasoning - transfer knowledge by analogy
        
        Args:
            source: Source domain
            target: Target domain
            mapping: Mapping from source to target concepts
            
        Returns:
            Inferred facts in target domain
        """
        inferred = []
        
        # Find facts about source
        source_facts = [f for f in self.facts if source in f]
        
        # Map to target domain
        for fact in source_facts:
            # Apply mapping
            target_fact = fact
            for source_term, target_term in mapping.items():
                target_fact = target_fact.replace(source_term, target_term)
            
            if target_fact not in self.facts:
                self.facts.add(target_fact)
                inferred.append(target_fact)
                
                self.inference_chain.append({
                    'type': 'analogical',
                    'source_fact': fact,
                    'target_fact': target_fact,
                    'mapping': mapping
                })
                
                self.inferences_made += 1
        
        return inferred
    
    def explain_inference(self, fact: str) -> List[Dict]:
        """
        Explain how a fact was inferred
        
        Args:
            fact: Fact to explain
            
        Returns:
            List of inference steps
        """
        explanations = []
        
        for step in self.inference_chain:
            if step.get('conclusion') == fact or step.get('goal') == fact:
                explanations.append(step)
        
        return explanations
    
    def get_reasoning_statistics(self) -> Dict[str, Any]:
        """Get reasoning statistics"""
        return {
            'total_facts': len(self.facts),
            'total_rules': len(self.rules),
            'inferences_made': self.inferences_made,
            'rules_applied': self.rules_applied,
            'causal_relations': sum(len(v) for v in self.causal_graph.values()),
            'inference_chain_length': len(self.inference_chain),
            'most_applied_rule': max(self.rules, key=lambda r: r['applied_count']) if self.rules else None
        }
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Answer a query using reasoning
        
        Args:
            question: Natural language question
            
        Returns:
            Answer with explanation
        """
        # Simple keyword-based query processing
        if "why" in question.lower():
            # Explain causation
            for fact in self.facts:
                if any(word in fact.lower() for word in question.lower().split()):
                    explanations = self.explain_inference(fact)
                    return {
                        'answer': fact,
                        'type': 'explanation',
                        'reasoning_steps': explanations
                    }
        
        elif "what if" in question.lower():
            # Hypothetical reasoning
            # Extract hypothetical
            return {
                'answer': 'Hypothetical reasoning requires specific conditions',
                'type': 'hypothetical'
            }
        
        elif "can" in question.lower() or "is it possible" in question.lower():
            # Goal checking
            words = question.lower().split()
            for word in words:
                if self.backward_chain(word):
                    return {
                        'answer': 'Yes, provable',
                        'type': 'proof',
                        'fact': word
                    }
            
            return {
                'answer': 'Cannot be proven from current knowledge',
                'type': 'proof'
            }
        
        # Default: search facts
        for fact in self.facts:
            if any(word in fact.lower() for word in question.lower().split()):
                return {
                    'answer': fact,
                    'type': 'fact_retrieval'
                }
        
        return {
            'answer': 'No relevant information found',
            'type': 'unknown'
        }
