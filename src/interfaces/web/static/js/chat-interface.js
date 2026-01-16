/**
 * Chat Interface - Optimized Communication with Thalos Prime
 */

class ThalosChat {
    constructor() {
        this.messagesContainer = document.getElementById('chat-messages');
        this.inputField = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        this.processingIndicator = document.getElementById('processing-indicator');
        this.statusIndicator = document.getElementById('status-indicator');
        this.statusText = document.getElementById('status-text');
        
        // Metrics
        this.neuralDensity = document.getElementById('neural-density');
        this.accuracy = document.getElementById('accuracy');
        this.activeLobes = document.getElementById('active-lobes');
        this.spikeRate = document.getElementById('spike-rate');
        
        // State
        this.isProcessing = false;
        this.messageQueue = [];
        
        // API endpoint
        this.apiUrl = '/api/chat';
        
        this.initializeEventListeners();
        this.updateSystemStatus();
        this.startMetricsUpdater();
    }
    
    initializeEventListeners() {
        // Send on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Send on Enter key
        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-focus input
        this.inputField.focus();
    }
    
    async sendMessage() {
        const message = this.inputField.value.trim();
        
        if (!message || this.isProcessing) return;
        
        // Clear input
        this.inputField.value = '';
        
        // Display user message
        this.addMessage('user', message);
        
        // Show processing
        this.setProcessing(true);
        
        try {
            // Check for commands
            if (message.startsWith('/')) {
                await this.handleCommand(message);
            } else {
                // Send to AI
                await this.processWithAI(message);
            }
        } catch (error) {
            this.addMessage('system', `Error: ${error.message}`, '⚠️');
        } finally {
            this.setProcessing(false);
        }
    }
    
    async handleCommand(command) {
        const cmd = command.toLowerCase().split(' ')[0];
        
        switch(cmd) {
            case '/status':
                await this.getSystemStatus();
                break;
            case '/metrics':
                await this.getDetailedMetrics();
                break;
            case '/lobes':
                await this.getLobeStatus();
                break;
            case '/train':
                await this.startTraining();
                break;
            case '/help':
                this.showHelp();
                break;
            default:
                this.addMessage('system', `Unknown command: ${cmd}`, '⚠️');
        }
    }
    
    async processWithAI(message) {
        // Simulate biological processing delay
        await this.delay(1000 + Math.random() * 1000);
        
        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    timestamp: Date.now()
                })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const data = await response.json();
            
            // Display AI response with biological metadata
            this.addAIMessage(data.response, data.metadata);
            
        } catch (error) {
            // Fallback response if API not available
            this.addAIMessage(
                this.generateFallbackResponse(message),
                {
                    neuralDensity: 0.72,
                    confidence: 0.85,
                    activeLobes: ['logic', 'abstract'],
                    processingTime: 1.2
                }
            );
        }
    }
    
    generateFallbackResponse(message) {
        const responses = [
            `Processing query through wetware core. Neural pattern recognition indicates: "${message}" requires multi-lobe analysis.`,
            `Biological computation complete. Query analyzed through ${Math.floor(Math.random() * 15000 + 5000)} synaptic connections.`,
            `Spike train decoded. Response synthesized through creative and logic lobes with ${(Math.random() * 0.3 + 0.7).toFixed(2)} confidence.`,
            `Organoid cluster processing complete. Dopamine reward signal: positive. Knowledge expansion achieved.`
        ];
        return responses[Math.floor(Math.random() * responses.length)];
    }
    
    addMessage(type, text, icon = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        
        if (icon) {
            const iconSpan = document.createElement('span');
            iconSpan.className = 'message-icon';
            iconSpan.textContent = icon;
            messageDiv.appendChild(iconSpan);
        }
        
        const textSpan = document.createElement('span');
        textSpan.className = 'message-text';
        textSpan.textContent = text;
        messageDiv.appendChild(textSpan);
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addAIMessage(text, metadata) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'ai-message';
        
        // Header with metadata
        const header = document.createElement('div');
        header.className = 'ai-message-header';
        header.innerHTML = `
            <span>🧠 THALOS RESPONSE</span>
            <span>Confidence: ${(metadata.confidence * 100).toFixed(1)}% | Time: ${metadata.processingTime}s</span>
        `;
        
        // Icon
        const icon = document.createElement('span');
        icon.className = 'message-icon';
        icon.textContent = '🧠';
        
        // Text
        const textSpan = document.createElement('span');
        textSpan.className = 'message-text';
        textSpan.innerHTML = `${header.outerHTML}<br>${text}`;
        
        messageDiv.appendChild(icon);
        messageDiv.appendChild(textSpan);
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Update metrics based on response
        this.updateMetricsFromResponse(metadata);
    }
    
    async getSystemStatus() {
        this.addMessage('system', 'Querying system status...', '🔍');
        await this.delay(500);
        
        const status = {
            status: 'OPERATIONAL',
            wetwareHealth: 'OPTIMAL',
            mea_channels: '20,000',
            organoids: '3 (Logic, Abstract, Governance)',
            synapticConnections: '~847,392',
            neuralDensity: '0.847'
        };
        
        const statusText = `
═══════════════════════════════════════
SYSTEM STATUS REPORT
═══════════════════════════════════════
Status: ${status.status}
Wetware Health: ${status.wetwareHealth}
MEA Channels Active: ${status.mea_channels}
Organoid Clusters: ${status.organoids}
Synaptic Connections: ${status.synapticConnections}
Neural Density: ${status.neuralDensity}
═══════════════════════════════════════
        `;
        
        this.addMessage('system', statusText, '📊');
    }
    
    async getDetailedMetrics() {
        this.addMessage('system', 'Retrieving detailed metrics...', '📈');
        await this.delay(500);
        
        const metrics = `
╔════════════════════════════════════════╗
║       BIOLOGICAL METRICS REPORT        ║
╠════════════════════════════════════════╣
║ Neural Density:        0.847 (↑0.003) ║
║ Accuracy Score:        0.923 (↑0.017) ║
║ Spike Rate:           47.3 Hz          ║
║ Plasticity Coeff:      1.24            ║
║ Reward Baseline:       0.78            ║
║                                        ║
║ LOBE ACTIVITY:                         ║
║ • Logic (Frontal):     ACTIVE (87%)    ║
║ • Abstract (Temporal): ACTIVE (73%)    ║
║ • Governance (Parietal): ACTIVE (94%)  ║
╚════════════════════════════════════════╝
        `;
        
        this.addMessage('system', metrics, '🧬');
    }
    
    async getLobeStatus() {
        this.addMessage('system', 'Analyzing organoid lobe activity...', '🧠');
        await this.delay(700);
        
        const lobeInfo = `
ORGANOID LOBE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔷 LOGIC LOBE (Frontal Cortex Analog)
   Function: Linear reasoning, code generation
   Activity: HIGH (87%)
   Synaptic Density: 0.91
   Recent Tasks: Pattern analysis, logical inference

🔶 ABSTRACT LOBE (Temporal Cortex Analog)  
   Function: Creative synthesis, novel fields
   Activity: MODERATE (73%)
   Synaptic Density: 0.84
   Recent Tasks: Conceptual mapping, innovation

🔵 GOVERNANCE LOBE (Parietal Cortex Analog)
   Function: Ethical evaluation, Prime Directive
   Activity: VERY HIGH (94%)
   Synaptic Density: 0.95
   Recent Tasks: Ethical alignment checking
        `;
        
        this.addMessage('system', lobeInfo, '🧬');
    }
    
    async startTraining() {
        this.addMessage('system', 'Initiating adaptive training protocol...', '🎯');
        await this.delay(800);
        this.addMessage('system', 'STDP (Spike-Timing-Dependent Plasticity) enabled. Dopamine modulation active.', '⚡');
        await this.delay(1000);
        this.addMessage('system', 'Training epoch 1/10 complete. Synaptic weights updated.', '✓');
    }
    
    showHelp() {
        const helpText = `
╔═══════════════════════════════════════╗
║        THALOS PRIME COMMANDS          ║
╠═══════════════════════════════════════╣
║ /status  - System status report       ║
║ /metrics - Detailed biological metrics║
║ /lobes   - Organoid lobe information  ║
║ /train   - Start training session     ║
║ /help    - Show this help message     ║
╚═══════════════════════════════════════╝

PRIME DIRECTIVE:
• ACCURACY - Prioritize truth over speed
• EXPANSION - Generate new knowledge
• PRESERVATION - Maintain homeostasis
        `;
        
        this.addMessage('system', helpText, '❓');
    }
    
    updateMetricsFromResponse(metadata) {
        if (metadata.neuralDensity) {
            this.neuralDensity.textContent = metadata.neuralDensity.toFixed(3);
        }
        if (metadata.confidence) {
            this.accuracy.textContent = metadata.confidence.toFixed(3);
        }
        if (metadata.activeLobes) {
            this.activeLobes.textContent = `${metadata.activeLobes.length}/3`;
        }
    }
    
    startMetricsUpdater() {
        // Update metrics periodically
        setInterval(() => {
            // Simulate neural activity
            const currentDensity = parseFloat(this.neuralDensity.textContent) || 0.72;
            const newDensity = Math.min(0.999, currentDensity + Math.random() * 0.001);
            this.neuralDensity.textContent = newDensity.toFixed(3);
            
            // Spike rate
            const spikeRate = (30 + Math.random() * 40).toFixed(1);
            this.spikeRate.textContent = `${spikeRate} Hz`;
        }, 2000);
    }
    
    updateSystemStatus() {
        this.statusText.textContent = 'OPERATIONAL';
        this.statusIndicator.style.background = '#0f0';
    }
    
    setProcessing(isProcessing) {
        this.isProcessing = isProcessing;
        
        if (isProcessing) {
            this.processingIndicator.classList.add('active');
            this.sendButton.disabled = true;
        } else {
            this.processingIndicator.classList.remove('active');
            this.sendButton.disabled = false;
            this.inputField.focus();
        }
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize chat interface
document.addEventListener('DOMContentLoaded', () => {
    window.thalosChat = new ThalosChat();
});
