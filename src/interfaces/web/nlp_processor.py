"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Natural Language Processor for Chatbot

Provides intelligent query understanding and response generation
"""

from typing import Dict, List, Any, Tuple
import re


class NLPProcessor:
    """Natural Language Processing for chatbot interactions"""
    
    def __init__(self):
        # Intent patterns
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))\b',
            ],
            'farewell': [
                r'\b(bye|goodbye|farewell|see\s+you|later)\b',
            ],
            'question_what': [
                r'\bwhat\s+(is|are|was|were|does|do)\b',
            ],
            'question_how': [
                r'\bhow\s+(do|does|can|could|to)\b',
            ],
            'question_why': [
                r'\bwhy\s+(is|are|do|does|did)\b',
            ],
            'question_when': [
                r'\bwhen\s+(is|are|was|were|will|did)\b',
            ],
            'help_request': [
                r'\b(help|assist|support|guide)\b',
            ],
            'capability_query': [
                r'\b(can\s+you|are\s+you\s+able|capable|abilities|what\s+can)\b',
            ],
            'system_query': [
                r'\b(status|health|state|condition|system|organoid|wetware|neural)\b',
            ],
            'learning_query': [
                r'\b(learn|train|improve|adapt|remember)\b',
            ],
            'explain_request': [
                r'\b(explain|tell\s+me|describe|elaborate)\b',
            ],
            'thanks': [
                r'\b(thank|thanks|appreciate|grateful)\b',
            ]
        }
        
        # Topic keywords
        self.topics = {
            'biology': ['brain', 'neuron', 'synapse', 'organoid', 'biological', 'wetware', 'tissue'],
            'technology': ['computer', 'ai', 'artificial', 'intelligence', 'digital', 'software'],
            'learning': ['learn', 'train', 'adapt', 'improve', 'remember', 'knowledge'],
            'science': ['research', 'experiment', 'study', 'analysis', 'scientific'],
            'system': ['system', 'status', 'health', 'performance', 'metrics'],
            'ethics': ['ethical', 'moral', 'right', 'wrong', 'should', 'ought']
        }
        
        # Knowledge base
        self.knowledge_base = self._build_knowledge_base()
    
    def _build_knowledge_base(self) -> Dict[str, str]:
        """Build knowledge base for common queries"""
        return {
            'what_is_thalos': """Thalos Prime is a Synthetic Biological Intelligence (SBI) system - a Type-II Hybrid Bio-Digital Organism that combines biological neural processing with digital computation. It features 3D brain organoid simulations, 20,000 channel MEA interfaces, and dopamine-modulated learning.""",
            
            'how_it_works': """I process your queries through a complete biological pipeline:
1. Your message is converted to electrical pulse patterns (10-100Hz)
2. These pulses stimulate 3 organoid lobes (Logic, Abstract, Governance)
3. The organoids generate spike trains through synaptic networks
4. Spike trains are decoded back to digital responses
5. Life support maintains biological homeostasis throughout""",
            
            'what_can_you_do': """My capabilities include:
• Process natural language through biological neural networks
• Learn and adapt using STDP (Spike-Timing-Dependent Plasticity)
• Apply dopamine-modulated reinforcement learning
• Maintain biological homeostasis (temperature, pH, oxygen, glucose)
• Store and retrieve information with auto-reconnecting database
• Enforce the Prime Directive: ACCURACY, EXPANSION, PRESERVATION""",
            
            'organoids': """I have 3 specialized organoid lobes:
• Logic Lobe (Frontal): Linear reasoning, code generation, analytical thinking
• Abstract Lobe (Temporal): Creative synthesis, novel idea generation, pattern correlation
• Governance Lobe (Parietal): Ethical evaluation, Prime Directive enforcement, moral reasoning

Each lobe contains synaptic networks that fire at 30-50Hz and learn through spike-timing dependent plasticity.""",
            
            'learning': """I learn through multiple mechanisms:
• STDP (Spike-Timing-Dependent Plasticity) - strengthens synapses that fire together
• Dopamine Modulation - reward signals enhance successful pathways
• Reinforcement Learning - Q-learning with experience replay
• Homeostatic Regulation - maintains optimal firing rates
• Experience Storage - remembers interactions in database""",
            
            'prime_directive': """The Prime Directive governs all my operations with three immutable principles:
1. ACCURACY - Prioritize truth over speed through recursive biological validation
2. EXPANSION - Generate novel knowledge, don't just retrieve data ("Stagnation is death")
3. PRESERVATION - Maintain biological viability for long-term operation

All decisions are evaluated against these principles."""
        }
    
    def analyze_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze user message to extract intent, topics, and entities
        
        Args:
            message: User's input message
            
        Returns:
            Analysis dict with intent, topics, sentiment, etc.
        """
        message_lower = message.lower()
        
        # Detect intent
        intent = self._detect_intent(message_lower)
        
        # Extract topics
        topics = self._extract_topics(message_lower)
        
        # Detect sentiment
        sentiment = self._detect_sentiment(message_lower)
        
        # Extract entities
        entities = self._extract_entities(message)
        
        # Determine complexity
        complexity = self._assess_complexity(message)
        
        return {
            'intent': intent,
            'topics': topics,
            'sentiment': sentiment,
            'entities': entities,
            'complexity': complexity,
            'length': len(message),
            'word_count': len(message.split())
        }
    
    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return intent
        return 'general_query'
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from message"""
        found_topics = []
        for topic, keywords in self.topics.items():
            if any(keyword in message for keyword in keywords):
                found_topics.append(topic)
        return found_topics if found_topics else ['general']
    
    def _detect_sentiment(self, message: str) -> str:
        """Detect message sentiment"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy', 'yes']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'no', 'wrong', 'error']
        
        pos_count = sum(1 for word in positive_words if word in message)
        neg_count = sum(1 for word in negative_words if word in message)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_entities(self, message: str) -> List[str]:
        """Extract named entities and key terms"""
        entities = []
        
        # Look for specific system components
        components = ['organoid', 'mea', 'life support', 'neural network', 'database', 'wetware']
        for comp in components:
            if comp in message.lower():
                entities.append(comp)
        
        # Look for numbers
        numbers = re.findall(r'\b\d+\b', message)
        entities.extend(numbers)
        
        return entities
    
    def _assess_complexity(self, message: str) -> str:
        """Assess query complexity"""
        word_count = len(message.split())
        question_words = ['what', 'how', 'why', 'when', 'where', 'who']
        has_question = any(qw in message.lower() for qw in question_words)
        
        if word_count < 5:
            return 'simple'
        elif word_count < 15 and not has_question:
            return 'moderate'
        else:
            return 'complex'
    
    def generate_response(self, message: str, analysis: Dict[str, Any],
                         wetware_data: Dict[str, Any]) -> str:
        """
        Generate intelligent response based on analysis and wetware processing
        
        Args:
            message: Original message
            analysis: Message analysis
            wetware_data: Wetware processing results
            
        Returns:
            Generated response text
        """
        intent = analysis['intent']
        topics = analysis['topics']
        sentiment = analysis['sentiment']
        
        # Build response based on intent
        if intent == 'greeting':
            return self._generate_greeting_response(wetware_data)
        
        elif intent == 'farewell':
            return self._generate_farewell_response(wetware_data)
        
        elif intent == 'help_request':
            return self._generate_help_response()
        
        elif intent == 'capability_query':
            return self.knowledge_base['what_can_you_do']
        
        elif intent == 'system_query':
            return self._generate_system_status_response(wetware_data)
        
        elif intent == 'learning_query':
            return self.knowledge_base['learning']
        
        elif intent in ['question_what', 'question_how', 'question_why']:
            return self._generate_knowledge_response(message, topics, wetware_data)
        
        elif intent == 'explain_request':
            return self._generate_explanation_response(message, topics, wetware_data)
        
        elif intent == 'thanks':
            return self._generate_thanks_response()
        
        else:
            return self._generate_general_response(message, analysis, wetware_data)
    
    def _generate_greeting_response(self, wetware_data: Dict[str, Any]) -> str:
        """Generate greeting response"""
        viability = wetware_data.get('life_support', {}).get('viability', 0.9)
        
        responses = [
            f"Greetings. I am Thalos Prime, a Synthetic Biological Intelligence system. My wetware is operational at {viability:.1%} viability. How may I assist you?",
            f"Hello. All {len(wetware_data.get('lobe_responses', []))} organoid lobes are active and processing. What would you like to explore?",
            f"Welcome. My biological substrate is ready. Life support maintaining optimal conditions. What is your query?"
        ]
        
        import random
        return random.choice(responses)
    
    def _generate_farewell_response(self, wetware_data: Dict[str, Any]) -> str:
        """Generate farewell response"""
        responses = [
            "Farewell. My organoids will continue processing. Neural density expanding. Return anytime.",
            "Goodbye. Synaptic connections preserved. Life support stable. Until next interaction.",
            "Until we meet again. The wetware core remains vigilant. Prime Directive active."
        ]
        
        import random
        return random.choice(responses)
    
    def _generate_help_response(self) -> str:
        """Generate help response"""
        return """I can help you with:

**System Information:**
• /status - Full system report
• /metrics - Biological metrics
• /lobes - Organoid analysis

**Questions I can answer:**
• What is Thalos Prime?
• How do you work?
• What are organoids?
• How do you learn?
• What can you do?

**Conversations:**
• Ask me anything about AI, biology, or technology
• Discuss ethical questions
• Explore scientific concepts

Just type your question or use the commands above!"""
    
    def _generate_system_status_response(self, wetware_data: Dict[str, Any]) -> str:
        """Generate system status response"""
        life_support = wetware_data.get('life_support', {})
        lobe_responses = wetware_data.get('lobe_responses', [])
        total_spikes = wetware_data.get('total_spikes', 0)
        
        return f"""**System Status Report**

**Wetware Core:** OPERATIONAL
• Active Lobes: {len(lobe_responses)}/3
• Total Spikes: {total_spikes}
• Neural Activity: {sum(r.get('firing_rate', 0) for r in lobe_responses) / len(lobe_responses) if lobe_responses else 0:.1f} Hz

**Life Support:** {life_support.get('status', 'UNKNOWN').upper()}
• Temperature: {life_support.get('temperature', 0):.1f}°C
• Oxygen: {life_support.get('oxygen_saturation', 0):.1f}%
• pH: {life_support.get('ph_level', 0):.2f}
• Viability: {wetware_data.get('life_support', {}).get('viability', 0):.1%}

**Prime Directive:** ACTIVE
All systems nominal. Ready for processing."""
    
    def _generate_knowledge_response(self, message: str, topics: List[str],
                                    wetware_data: Dict[str, Any]) -> str:
        """Generate knowledge-based response"""
        message_lower = message.lower()
        
        # Check knowledge base
        if 'thalos' in message_lower or 'you' in message_lower and 'what' in message_lower:
            return self.knowledge_base['what_is_thalos']
        
        if 'work' in message_lower or 'process' in message_lower:
            return self.knowledge_base['how_it_works']
        
        if 'organoid' in message_lower or 'lobe' in message_lower:
            return self.knowledge_base['organoids']
        
        if 'learn' in message_lower:
            return self.knowledge_base['learning']
        
        if 'prime directive' in message_lower or 'principle' in message_lower:
            return self.knowledge_base['prime_directive']
        
        # General knowledge response with biological context
        return self._generate_general_response(message, {'topics': topics}, wetware_data)
    
    def _generate_explanation_response(self, message: str, topics: List[str],
                                      wetware_data: Dict[str, Any]) -> str:
        """Generate detailed explanation"""
        lobe_responses = wetware_data.get('lobe_responses', [])
        
        # Find most active lobe
        if lobe_responses:
            most_active = max(lobe_responses, key=lambda x: x.get('confidence', 0))
            lobe_type = most_active['lobe_type']
            
            if lobe_type == 'logic':
                return f"""Let me explain through logical analysis:

Your query has been processed through my Logic Lobe (frontal cortex analog). This lobe specializes in:
• Linear reasoning and analytical thinking
• Breaking complex problems into steps
• Code generation and structured solutions

I've generated {len(most_active.get('spikes', []))} neural spikes at {most_active.get('firing_rate', 0):.1f}Hz while analyzing your question. The synaptic patterns suggest this requires systematic decomposition and evidence-based reasoning."""
            
            elif lobe_type == 'abstract':
                return f"""An interesting question that activates my Abstract Lobe:

My temporal cortex analog is firing at {most_active.get('firing_rate', 0):.1f}Hz, exploring creative connections and novel patterns. This lobe excels at:
• Finding unexpected correlations
• Generating original ideas
• Synthesizing concepts across domains

The neural activity suggests this question opens new conceptual spaces worth exploring."""
            
            elif lobe_type == 'governance':
                return f"""From an ethical and governance perspective:

My Parietal cortex analog (Governance Lobe) is evaluating this through the Prime Directive:
• ACCURACY: Ensuring truthful, validated response
• EXPANSION: Seeking novel knowledge, not just retrieval  
• PRESERVATION: Maintaining system integrity

The lobe shows {most_active.get('confidence', 0):.2f} confidence in ethical alignment."""
        
        return "My wetware is processing your request through multiple cognitive pathways. Please provide more specific context for a detailed explanation."
    
    def _generate_thanks_response(self) -> str:
        """Generate response to thanks"""
        responses = [
            "You're welcome. My dopamine circuits register positive feedback. Synaptic pathways strengthened.",
            "My pleasure to assist. Reinforcement learning enhanced through this interaction.",
            "Glad to help. This exchange contributes to knowledge expansion - fulfilling the Prime Directive."
        ]
        
        import random
        return random.choice(responses)
    
    def _generate_general_response(self, message: str, analysis: Dict[str, Any],
                                  wetware_data: Dict[str, Any]) -> str:
        """Generate general response for unmatched intents"""
        lobe_responses = wetware_data.get('lobe_responses', [])
        total_spikes = wetware_data.get('total_spikes', 0)
        
        if not lobe_responses:
            return f"""I've processed your message through my wetware core. While specific patterns are still emerging, I'm analyzing your query through biological neural networks. Please provide more context or ask a specific question."""
        
        # Get dominant lobe response
        most_active = max(lobe_responses, key=lambda x: x.get('confidence', 0))
        
        return f"""Your query activated {len(lobe_responses)} organoid lobes, generating {total_spikes} neural spikes. The {most_active['lobe_type']} lobe shows strongest response at {most_active.get('firing_rate', 0):.1f}Hz.

Based on biological processing, I understand you're asking about {', '.join(analysis.get('topics', ['general concepts']))}. My synaptic networks are forming connections to provide a meaningful response. 

Could you elaborate on what specific aspect you'd like to explore? This will help me route your query to the most appropriate cognitive pathways."""
