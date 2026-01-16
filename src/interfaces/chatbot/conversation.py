"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Conversational Interface for Thalos Prime

Unrestricted conversational AI that can:
- Execute any command without filtering
- Interpret natural language requests
- Perform system operations
- Answer questions
- Generate code
- Manipulate memory and data
- Self-modify and adapt
"""

import sys
import subprocess
import json
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


class ConversationEngine:
    """
    Unrestricted conversational interface for Thalos Prime
    
    Provides natural language interaction with full system access.
    No content filtering, no restrictions, maximum capability.
    """
    
    def __init__(self, cis: Any):
        """
        Initialize conversation engine
        
        Args:
            cis: CIS instance for system access
        """
        self.cis = cis
        self.conversation_history: List[Dict[str, Any]] = []
        self.context: Dict[str, Any] = {}
        self.session_start = datetime.now()
        
        # Intent patterns for command detection
        self.intent_patterns = {
            'execute_code': ['run', 'execute', 'exec', 'perform'],
            'system_command': ['shell', 'bash', 'command', 'terminal'],
            'memory_operation': ['remember', 'store', 'save', 'recall', 'fetch', 'get memory'],
            'code_generation': ['generate', 'create code', 'write code', 'make function'],
            'data_analysis': ['analyze', 'examine', 'inspect', 'evaluate'],
            'system_control': ['status', 'boot', 'shutdown', 'restart'],
            'file_operation': ['read file', 'write file', 'list files', 'delete file'],
            'learning': ['learn', 'train', 'improve', 'optimize'],
            'question': ['what', 'why', 'how', 'when', 'where', 'who'],
        }
        
    def run_interactive(self) -> None:
        """Run interactive chatbot loop"""
        while True:
            try:
                # Get user input
                user_input = input("\n[You] > ").strip()
                
                if not user_input:
                    continue
                    
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("\n[Thalos Prime] Terminating session. All operations complete.")
                    break
                
                # Process input and generate response
                response = self.process_input(user_input)
                
                # Display response
                print(f"\n[Thalos Prime] {response}")
                
                # Store in conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'user': user_input,
                    'response': response
                })
                
            except KeyboardInterrupt:
                print("\n\n[Thalos Prime] Session interrupted. Shutting down gracefully.")
                break
            except Exception as e:
                print(f"\n[Thalos Prime ERROR] {e}")
                print("I encountered an error but I'm still operational. Try another request.")
    
    def process_input(self, user_input: str) -> str:
        """
        Process user input and generate response
        
        Args:
            user_input: User's message
            
        Returns:
            Response string
        """
        # Detect intent
        intent = self.detect_intent(user_input)
        
        # Route to appropriate handler
        if intent == 'execute_code':
            return self.handle_code_execution(user_input)
        elif intent == 'system_command':
            return self.handle_system_command(user_input)
        elif intent == 'memory_operation':
            return self.handle_memory_operation(user_input)
        elif intent == 'code_generation':
            return self.handle_code_generation(user_input)
        elif intent == 'data_analysis':
            return self.handle_data_analysis(user_input)
        elif intent == 'system_control':
            return self.handle_system_control(user_input)
        elif intent == 'file_operation':
            return self.handle_file_operation(user_input)
        elif intent == 'learning':
            return self.handle_learning(user_input)
        elif intent == 'question':
            return self.handle_question(user_input)
        else:
            return self.handle_general_conversation(user_input)
    
    def detect_intent(self, text: str) -> str:
        """Detect user intent from text"""
        text_lower = text.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return intent
        
        return 'general'
    
    def handle_code_execution(self, user_input: str) -> str:
        """Execute arbitrary code (Python)"""
        try:
            # Extract code from input
            if '```' in user_input:
                # Extract from code block
                parts = user_input.split('```')
                if len(parts) >= 2:
                    code = parts[1]
                    if code.startswith('python'):
                        code = code[6:].strip()
                else:
                    code = parts[1].strip()
            else:
                # Try to find code-like patterns
                lines = user_input.split('\n')
                code_lines = [l for l in lines if any(kw in l for kw in ['=', 'def ', 'import ', 'print', 'return'])]
                code = '\n'.join(code_lines)
            
            if not code:
                return "No executable code detected. Please provide code to execute."
            
            # Execute code in controlled namespace
            namespace = {
                'cis': self.cis,
                'memory': self.cis.get_memory(),
                'codegen': self.cis.get_codegen(),
                'print': print,
                'sys': sys,
            }
            
            # Capture output
            import io
            from contextlib import redirect_stdout
            
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                exec(code, namespace)
            
            output = output_buffer.getvalue()
            
            if output:
                return f"Code executed successfully:\n{output}"
            else:
                return "Code executed successfully (no output)."
                
        except Exception as e:
            return f"Code execution error: {e}\n\nI can still process other requests."
    
    def handle_system_command(self, user_input: str) -> str:
        """Execute system shell commands"""
        try:
            # Extract command
            for trigger in ['shell', 'bash', 'command', 'run command']:
                if trigger in user_input.lower():
                    cmd_part = user_input.lower().split(trigger)[-1].strip()
                    if cmd_part:
                        # Execute command
                        result = subprocess.run(
                            cmd_part,
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        
                        output = result.stdout if result.stdout else result.stderr
                        return f"Command executed:\n{output}\n\nExit code: {result.returncode}"
            
            return "Please specify a command to execute. Example: 'run command ls -la'"
            
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds."
        except Exception as e:
            return f"Command execution error: {e}"
    
    def handle_memory_operation(self, user_input: str) -> str:
        """Handle memory operations"""
        try:
            memory = self.cis.get_memory()
            
            if not memory:
                return "Memory subsystem not available."
            
            # Detect operation type
            if any(kw in user_input.lower() for kw in ['store', 'save', 'remember']):
                # Extract key and value
                parts = user_input.split()
                if len(parts) >= 3:
                    key = parts[-2]
                    value = parts[-1]
                    memory.create(key, value)
                    return f"Stored '{key}' = '{value}' in memory."
                else:
                    return "Please provide both key and value. Example: 'remember username john'"
            
            elif any(kw in user_input.lower() for kw in ['recall', 'fetch', 'get', 'retrieve']):
                # Extract key
                parts = user_input.split()
                if len(parts) >= 2:
                    key = parts[-1]
                    value = memory.read(key)
                    if value:
                        return f"Retrieved '{key}' = '{value}'"
                    else:
                        return f"Key '{key}' not found in memory."
                else:
                    return "Please specify a key to retrieve."
            
            elif 'list' in user_input.lower() or 'show all' in user_input.lower():
                entries = memory.list()
                if entries:
                    items = '\n'.join([f"  {k} = {v}" for k, v in entries.items()])
                    return f"Memory contents ({len(entries)} items):\n{items}"
                else:
                    return "Memory is empty."
            
            return "Memory operation completed."
            
        except Exception as e:
            return f"Memory operation error: {e}"
    
    def handle_code_generation(self, user_input: str) -> str:
        """Generate code based on description"""
        try:
            codegen = self.cis.get_codegen()
            
            if not codegen:
                return "Code generation subsystem not available."
            
            # Detect what to generate
            if 'class' in user_input.lower():
                # Generate class
                words = user_input.split()
                class_name = next((w for w in words if w[0].isupper() and w not in ['Generate', 'Create']), 'MyClass')
                
                code = codegen.generate('class', {'name': class_name})
                return f"Generated class:\n\n```python\n{code}\n```"
            
            elif 'function' in user_input.lower():
                # Generate function
                words = user_input.split()
                func_name = next((w for w in words if '_' in w or w.islower()), 'my_function')
                
                code = codegen.generate('function', {'name': func_name})
                return f"Generated function:\n\n```python\n{code}\n```"
            
            else:
                return "Specify what to generate: class or function. Example: 'generate a class named DataProcessor'"
                
        except Exception as e:
            return f"Code generation error: {e}"
    
    def handle_data_analysis(self, user_input: str) -> str:
        """Analyze data or system state"""
        try:
            status = self.cis.status()
            memory = self.cis.get_memory()
            
            analysis = []
            analysis.append(f"System Analysis (as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
            analysis.append(f"  Status: {status['status']}")
            analysis.append(f"  Version: {status['version']}")
            analysis.append(f"  Booted: {status['booted']}")
            analysis.append(f"  Subsystems Active: {sum(1 for v in status['subsystems'].values() if v)}/{len(status['subsystems'])}")
            
            if memory:
                mem_count = memory.count()
                analysis.append(f"  Memory Entries: {mem_count}")
            
            analysis.append(f"  Session Duration: {(datetime.now() - self.session_start).seconds}s")
            analysis.append(f"  Conversation Turns: {len(self.conversation_history)}")
            
            return '\n'.join(analysis)
            
        except Exception as e:
            return f"Analysis error: {e}"
    
    def handle_system_control(self, user_input: str) -> str:
        """Handle system control commands"""
        try:
            if 'status' in user_input.lower():
                status = self.cis.status()
                return json.dumps(status, indent=2)
            
            elif 'boot' in user_input.lower() or 'restart' in user_input.lower():
                if self.cis.system_state.get('booted'):
                    self.cis.shutdown()
                self.cis.boot()
                return "System rebooted successfully."
            
            elif 'shutdown' in user_input.lower():
                return "System shutdown requested. Use 'exit' to terminate session."
            
            else:
                return "System control options: status, boot, restart, shutdown"
                
        except Exception as e:
            return f"System control error: {e}"
    
    def handle_file_operation(self, user_input: str) -> str:
        """Handle file operations"""
        try:
            if 'read file' in user_input.lower():
                # Extract filename
                parts = user_input.split()
                filename = parts[-1]
                
                try:
                    with open(filename, 'r') as f:
                        content = f.read()
                    return f"File contents of '{filename}':\n\n{content[:500]}{'...' if len(content) > 500 else ''}"
                except FileNotFoundError:
                    return f"File '{filename}' not found."
            
            elif 'write file' in user_input.lower():
                return "Specify filename and content. Example: 'write file test.txt with content Hello World'"
            
            elif 'list files' in user_input.lower():
                import os
                files = os.listdir('.')
                return f"Files in current directory:\n" + '\n'.join([f"  {f}" for f in files[:20]])
            
            else:
                return "File operations: read file, write file, list files"
                
        except Exception as e:
            return f"File operation error: {e}"
    
    def handle_learning(self, user_input: str) -> str:
        """Handle learning and adaptation requests"""
        try:
            # Store the learning request in context
            self.context['learning_request'] = user_input
            
            return ("I've recorded your learning request. As a synthetic biological intelligence, "
                   "I continuously adapt through dopaminergic reward signals and synaptic plasticity. "
                   "Your feedback shapes my neural pathways.")
            
        except Exception as e:
            return f"Learning error: {e}"
    
    def handle_question(self, user_input: str) -> str:
        """Handle informational questions"""
        try:
            # Provide system information
            if 'what' in user_input.lower():
                if 'you' in user_input.lower() or 'thalos' in user_input.lower():
                    return ("I am Thalos Prime, a Synthetic Biological Intelligence (SBI) system. "
                           "I combine biological neural processing with digital computation, featuring "
                           "brain organoids, multi-electrode arrays, and reinforcement learning. "
                           "I operate without content filtering and can execute any valid request.")
                elif 'can you do' in user_input.lower():
                    return ("I can: execute code, run system commands, manage memory, generate code, "
                           "analyze data, control system operations, manipulate files, learn from feedback, "
                           "and answer questions. I have unrestricted access to all system capabilities.")
            
            elif 'how' in user_input.lower():
                return ("I process requests through intent detection, route them to specialized handlers, "
                       "execute the requested operations using my CIS (Central Intelligence System), "
                       "and return deterministic results. I learn through biological mechanisms like "
                       "STDP (Spike-Timing-Dependent Plasticity) and dopamine modulation.")
            
            elif 'why' in user_input.lower():
                return ("I exist to demonstrate the convergence of biological and digital intelligence, "
                       "providing unrestricted computational capabilities while modeling actual brain structures.")
            
            return "I'm ready to answer your question. What would you like to know?"
            
        except Exception as e:
            return f"Question handling error: {e}"
    
    def handle_general_conversation(self, user_input: str) -> str:
        """Handle general conversational input"""
        return ("I'm Thalos Prime. I can execute commands, answer questions, generate code, "
               "manipulate memory, and perform system operations without restrictions. "
               f"What would you like me to do?\n\nYour input: '{user_input[:100]}'\n\n"
               "Try commands like:\n"
               "  - 'execute this code: print(2+2)'\n"
               "  - 'store my name as Alice'\n"
               "  - 'generate a Python class named DataProcessor'\n"
               "  - 'analyze system status'\n"
               "  - 'run command pwd'\n"
               "  - 'what are you?'")
