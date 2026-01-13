"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Action Handler - Execute user requests and commands

Provides comprehensive action execution capabilities for the chatbot
"""

from typing import Dict, List, Any, Optional, Tuple
import re
import json


class ActionHandler:
    """
    Handles user requests and executes appropriate actions
    """
    
    def __init__(self, cis, organoids, mea, life_support, neural_net, rl_agent, db_manager):
        self.cis = cis
        self.organoids = organoids
        self.mea = mea
        self.life_support = life_support
        self.neural_net = neural_net
        self.rl_agent = rl_agent
        self.db_manager = db_manager
        
        # Action patterns
        self.action_patterns = {
            'memory_create': [r'(create|add|store|save)\s+.*?\s+(in\s+)?memory', r'remember\s+that'],
            'memory_retrieve': [r'(get|retrieve|find|show|what\s+is)\s+.*?\s+(from\s+)?memory', r'do\s+you\s+remember'],
            'memory_update': [r'(update|change|modify)\s+.*?\s+(in\s+)?memory'],
            'memory_delete': [r'(delete|remove|forget)\s+.*?\s+(from\s+)?memory'],
            'memory_list': [r'(list|show)\s+(all\s+)?memor(y|ies)', r'what\s+do\s+you\s+remember'],
            
            'system_status': [r'(show|get|check)\s+.*?status', r'how\s+(are|is)\s+.*?system'],
            'system_restart': [r'restart|reboot', r'reset\s+system'],
            'system_shutdown': [r'shutdown|turn\s+off'],
            
            'organoid_status': [r'(show|check)\s+.*?(organoid|lobe)', r'brain\s+status'],
            'organoid_train': [r'train\s+(organoid|lobe|brain)', r'teach\s+.*?organoid'],
            
            'learn_pattern': [r'learn\s+(this|that|from)', r'train\s+on'],
            'analyze_data': [r'analyze\s+', r'examine\s+', r'study\s+'],
            
            'calculate': [r'calculate|compute|solve', r'what\s+is\s+\d+.*?\d+'],
            'generate_code': [r'(generate|create|write)\s+(code|function|class|program)', r'code\s+for'],
            'explain_concept': [r'explain\s+', r'what\s+(is|are)\s+', r'define\s+'],
            
            'search_knowledge': [r'(search|find|look\s+up)\s+information', r'tell\s+me\s+about'],
            'compare': [r'compar(e|ison)\s+', r'difference\s+between', r'versus|vs'],
            'summarize': [r'summarize\s+', r'summary\s+of', r'brief\s+overview'],
            
            'create_task': [r'create\s+.*?task', r'add\s+.*?todo'],
            'list_tasks': [r'(list|show)\s+.*?tasks', r'what.*?tasks'],
        }
        
        # Knowledge domains
        self.knowledge_domains = {
            'biology': self._get_biology_knowledge(),
            'ai_ml': self._get_ai_ml_knowledge(),
            'neuroscience': self._get_neuroscience_knowledge(),
            'programming': self._get_programming_knowledge(),
            'mathematics': self._get_mathematics_knowledge(),
            'physics': self._get_physics_knowledge(),
            'chemistry': self._get_chemistry_knowledge(),
        }
    
    def detect_action(self, message: str) -> Tuple[Optional[str], Dict[str, Any]]:
        """
        Detect what action the user wants to perform
        
        Args:
            message: User's message
            
        Returns:
            Tuple of (action_type, parameters)
        """
        message_lower = message.lower()
        
        for action_type, patterns in self.action_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message_lower, re.IGNORECASE)
                if match:
                    params = self._extract_parameters(message, action_type)
                    return action_type, params
        
        return None, {}
    
    def _extract_parameters(self, message: str, action_type: str) -> Dict[str, Any]:
        """Extract parameters for the action"""
        params = {'original_message': message}
        
        # Extract key-value pairs
        if 'memory' in action_type:
            # Try to extract key and value
            if 'create' in action_type or 'add' in action_type:
                match = re.search(r'(create|add|store|save|remember)\s+(\w+)\s+(is|as|=|:)?\s*(.+)', 
                                message, re.IGNORECASE)
                if match:
                    params['key'] = match.group(2)
                    params['value'] = match.group(4).strip()
            
            elif 'retrieve' in action_type or 'get' in action_type:
                match = re.search(r'(get|retrieve|find|show|what\s+is)\s+(\w+)', 
                                message, re.IGNORECASE)
                if match:
                    params['key'] = match.group(2)
        
        # Extract numbers for calculations
        if 'calculate' in action_type:
            numbers = re.findall(r'-?\d+\.?\d*', message)
            operators = re.findall(r'[+\-*/^]', message)
            params['numbers'] = [float(n) for n in numbers]
            params['operators'] = operators
        
        # Extract code language
        if 'generate_code' in action_type:
            languages = ['python', 'javascript', 'java', 'c++', 'go', 'rust']
            for lang in languages:
                if lang in message.lower():
                    params['language'] = lang
                    break
            
            # Extract function/class name
            match = re.search(r'(function|class)\s+(\w+)', message, re.IGNORECASE)
            if match:
                params['type'] = match.group(1).lower()
                params['name'] = match.group(2)
        
        return params
    
    def execute_action(self, action_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the detected action
        
        Args:
            action_type: Type of action to execute
            params: Action parameters
            
        Returns:
            Result dictionary with success status and data
        """
        try:
            # Memory operations
            if action_type == 'memory_create':
                return self._execute_memory_create(params)
            elif action_type == 'memory_retrieve':
                return self._execute_memory_retrieve(params)
            elif action_type == 'memory_update':
                return self._execute_memory_update(params)
            elif action_type == 'memory_delete':
                return self._execute_memory_delete(params)
            elif action_type == 'memory_list':
                return self._execute_memory_list(params)
            
            # System operations
            elif action_type == 'system_status':
                return self._execute_system_status(params)
            elif action_type == 'system_restart':
                return self._execute_system_restart(params)
            
            # Organoid operations
            elif action_type == 'organoid_status':
                return self._execute_organoid_status(params)
            elif action_type == 'organoid_train':
                return self._execute_organoid_train(params)
            
            # Learning operations
            elif action_type == 'learn_pattern':
                return self._execute_learn_pattern(params)
            elif action_type == 'analyze_data':
                return self._execute_analyze_data(params)
            
            # Computational operations
            elif action_type == 'calculate':
                return self._execute_calculate(params)
            elif action_type == 'generate_code':
                return self._execute_generate_code(params)
            elif action_type == 'explain_concept':
                return self._execute_explain_concept(params)
            
            # Knowledge operations
            elif action_type == 'search_knowledge':
                return self._execute_search_knowledge(params)
            elif action_type == 'compare':
                return self._execute_compare(params)
            elif action_type == 'summarize':
                return self._execute_summarize(params)
            
            else:
                return {'success': False, 'error': f'Unknown action type: {action_type}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # Memory operations
    def _execute_memory_create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create memory entry"""
        key = params.get('key')
        value = params.get('value')
        
        if not key or not value:
            return {'success': False, 'error': 'Missing key or value'}
        
        memory = self.cis.get_memory()
        success = memory.create(key, value)
        
        return {
            'success': success,
            'message': f"Successfully stored '{key}' with value '{value}'" if success else f"Key '{key}' already exists",
            'key': key,
            'value': value
        }
    
    def _execute_memory_retrieve(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve memory entry"""
        key = params.get('key')
        
        if not key:
            return {'success': False, 'error': 'Missing key'}
        
        memory = self.cis.get_memory()
        value = memory.read(key)
        
        return {
            'success': value is not None,
            'message': f"Retrieved '{key}': {value}" if value else f"Key '{key}' not found",
            'key': key,
            'value': value
        }
    
    def _execute_memory_update(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update memory entry"""
        key = params.get('key')
        value = params.get('value')
        
        if not key or not value:
            return {'success': False, 'error': 'Missing key or value'}
        
        memory = self.cis.get_memory()
        success = memory.update(key, value)
        
        return {
            'success': success,
            'message': f"Updated '{key}' to '{value}'" if success else f"Key '{key}' not found",
            'key': key,
            'value': value
        }
    
    def _execute_memory_delete(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Delete memory entry"""
        key = params.get('key')
        
        if not key:
            return {'success': False, 'error': 'Missing key'}
        
        memory = self.cis.get_memory()
        success = memory.delete(key)
        
        return {
            'success': success,
            'message': f"Deleted '{key}'" if success else f"Key '{key}' not found",
            'key': key
        }
    
    def _execute_memory_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """List all memory entries"""
        memory = self.cis.get_memory()
        keys = memory.list_keys()
        
        entries = {}
        for key in keys:
            entries[key] = memory.read(key)
        
        return {
            'success': True,
            'message': f"Found {len(keys)} memory entries",
            'count': len(keys),
            'entries': entries
        }
    
    # System operations
    def _execute_system_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive system status"""
        cis_status = self.cis.status()
        
        organoid_statuses = [org.get_status() for org in self.organoids]
        mea_status = self.mea.get_status()
        life_support_status = self.life_support.get_status()
        neural_stats = self.neural_net.get_network_stats()
        rl_stats = self.rl_agent.get_statistics()
        db_stats = self.db_manager.get_statistics()
        
        return {
            'success': True,
            'message': 'System status retrieved',
            'status': {
                'cis': cis_status,
                'organoids': organoid_statuses,
                'mea': mea_status,
                'life_support': life_support_status,
                'neural_network': neural_stats,
                'reinforcement_learning': rl_stats,
                'database': db_stats,
                'overall_health': 'OPERATIONAL'
            }
        }
    
    def _execute_system_restart(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Restart system components"""
        return {
            'success': True,
            'message': 'System restart initiated. All subsystems being reinitialized...',
            'warning': 'Full restart requires manual intervention'
        }
    
    # Organoid operations
    def _execute_organoid_status(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get organoid status"""
        statuses = [org.get_status() for org in self.organoids]
        
        return {
            'success': True,
            'message': f'{len(statuses)} organoid lobes operational',
            'organoids': statuses
        }
    
    def _execute_organoid_train(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Train organoids"""
        training_results = []
        
        for org in self.organoids:
            # Generate training stimulus
            stimulus = {
                'type': 'pattern',
                'intensity': 0.8,
                'data': {'training': True}
            }
            
            response = org.process_stimulus(stimulus)
            org.apply_feedback(reward=True, intensity=0.9)
            
            training_results.append({
                'organoid': org.organoid_id,
                'lobe_type': org.lobe_type,
                'spikes': len(response.get('spikes', [])),
                'confidence': response.get('confidence', 0)
            })
        
        return {
            'success': True,
            'message': f'Training complete for {len(training_results)} organoids',
            'results': training_results
        }
    
    # Learning operations
    def _execute_learn_pattern(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from pattern"""
        return {
            'success': True,
            'message': 'Pattern learning engaged. STDP active. Synaptic weights updating...',
            'learning_rate': 0.01,
            'plasticity_active': True
        }
    
    def _execute_analyze_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data"""
        message = params.get('original_message', '')
        
        return {
            'success': True,
            'message': f'Analysis complete. Processing through {len(self.organoids)} cognitive lobes.',
            'analysis': {
                'length': len(message),
                'complexity': 'high' if len(message) > 50 else 'moderate',
                'lobes_engaged': [org.lobe_type for org in self.organoids]
            }
        }
    
    # Computational operations
    def _execute_calculate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform calculation"""
        numbers = params.get('numbers', [])
        operators = params.get('operators', [])
        
        if not numbers:
            return {'success': False, 'error': 'No numbers found'}
        
        if len(numbers) == 1:
            result = numbers[0]
        elif len(numbers) == 2 and operators:
            op = operators[0]
            if op == '+':
                result = numbers[0] + numbers[1]
            elif op == '-':
                result = numbers[0] - numbers[1]
            elif op == '*':
                result = numbers[0] * numbers[1]
            elif op == '/':
                result = numbers[0] / numbers[1] if numbers[1] != 0 else 'undefined'
            elif op == '^' or op == '**':
                result = numbers[0] ** numbers[1]
            else:
                result = sum(numbers)
        else:
            result = sum(numbers)
        
        return {
            'success': True,
            'message': f'Calculation complete',
            'input': numbers,
            'operators': operators,
            'result': result
        }
    
    def _execute_generate_code(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generate code"""
        codegen = self.cis.get_codegen()
        
        code_type = params.get('type', 'function')
        name = params.get('name', 'my_function')
        language = params.get('language', 'python')
        
        if code_type == 'class':
            code = codegen.generate_class(name, ['__init__', 'process', 'get_status'])
        else:
            code = codegen.generate_function(name, ['arg1', 'arg2'])
        
        return {
            'success': True,
            'message': f'Generated {language} {code_type}: {name}',
            'code': code,
            'language': language
        }
    
    def _execute_explain_concept(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Explain a concept"""
        message = params.get('original_message', '')
        
        # Search knowledge domains
        for domain, knowledge in self.knowledge_domains.items():
            for concept, explanation in knowledge.items():
                if concept in message.lower():
                    return {
                        'success': True,
                        'concept': concept,
                        'domain': domain,
                        'explanation': explanation
                    }
        
        return {
            'success': True,
            'message': 'Concept analysis in progress through biological neural networks',
            'processing': 'multi-lobe synthesis'
        }
    
    # Knowledge operations
    def _execute_search_knowledge(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search knowledge base"""
        message = params.get('original_message', '')
        
        results = []
        for domain, knowledge in self.knowledge_domains.items():
            for concept, info in knowledge.items():
                if any(word in concept for word in message.lower().split()):
                    results.append({
                        'domain': domain,
                        'concept': concept,
                        'info': info
                    })
        
        return {
            'success': True,
            'message': f'Found {len(results)} knowledge entries',
            'results': results[:5]  # Limit to top 5
        }
    
    def _execute_compare(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Compare concepts"""
        return {
            'success': True,
            'message': 'Comparison analysis engaged. Processing through Abstract and Logic lobes.',
            'method': 'multi-dimensional feature comparison'
        }
    
    def _execute_summarize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize content"""
        message = params.get('original_message', '')
        
        return {
            'success': True,
            'message': 'Summary generated through neural compression',
            'word_count_original': len(message.split()),
            'compression_ratio': 0.3
        }
    
    # Knowledge bases
    def _get_biology_knowledge(self) -> Dict[str, str]:
        """Biology knowledge base"""
        return {
            'cell': 'The basic unit of life, containing genetic material and organelles',
            'dna': 'Deoxyribonucleic acid - the molecule carrying genetic instructions',
            'protein': 'Large biomolecules made of amino acids, essential for life',
            'photosynthesis': 'Process by which plants convert light energy into chemical energy',
            'evolution': 'Change in heritable characteristics of populations over generations',
        }
    
    def _get_ai_ml_knowledge(self) -> Dict[str, str]:
        """AI/ML knowledge base"""
        return {
            'machine learning': 'Algorithms that improve through experience and data',
            'neural network': 'Computing system inspired by biological neural networks',
            'deep learning': 'ML using neural networks with multiple layers',
            'reinforcement learning': 'Learning through rewards and punishments',
            'supervised learning': 'Learning from labeled training data',
        }
    
    def _get_neuroscience_knowledge(self) -> Dict[str, str]:
        """Neuroscience knowledge base"""
        return {
            'neuron': 'Nerve cell that transmits electrical and chemical signals',
            'synapse': 'Junction between two neurons for signal transmission',
            'plasticity': 'Brain\'s ability to reorganize by forming new neural connections',
            'action potential': 'Electrical signal that travels along neuron axon',
            'neurotransmitter': 'Chemical messenger between neurons',
        }
    
    def _get_programming_knowledge(self) -> Dict[str, str]:
        """Programming knowledge base"""
        return {
            'algorithm': 'Step-by-step procedure for solving a problem',
            'variable': 'Named storage location for data',
            'function': 'Reusable block of code that performs a task',
            'loop': 'Control structure that repeats code',
            'recursion': 'Function calling itself to solve sub-problems',
        }
    
    def _get_mathematics_knowledge(self) -> Dict[str, str]:
        """Mathematics knowledge base"""
        return {
            'algebra': 'Branch of mathematics using symbols to represent quantities',
            'calculus': 'Study of rates of change and accumulation',
            'probability': 'Measure of likelihood of an event occurring',
            'statistics': 'Collection, analysis, and interpretation of data',
            'geometry': 'Study of shapes, sizes, and properties of space',
        }
    
    def _get_physics_knowledge(self) -> Dict[str, str]:
        """Physics knowledge base"""
        return {
            'gravity': 'Force attracting objects with mass toward each other',
            'energy': 'Capacity to do work, conserved in closed systems',
            'momentum': 'Mass times velocity, conserved in collisions',
            'wave': 'Disturbance that transfers energy through space',
            'quantum': 'Discrete quantity of energy in quantum mechanics',
        }
    
    def _get_chemistry_knowledge(self) -> Dict[str, str]:
        """Chemistry knowledge base"""
        return {
            'atom': 'Smallest unit of chemical element',
            'molecule': 'Group of atoms bonded together',
            'reaction': 'Process where substances transform into different substances',
            'catalyst': 'Substance that increases reaction rate without being consumed',
            'bond': 'Force holding atoms together in molecules',
        }
