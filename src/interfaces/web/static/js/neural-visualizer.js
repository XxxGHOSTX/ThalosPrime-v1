/**
 * Neural Activity Visualizer - Real-time spike visualization
 * Optimized with efficient rendering
 */

class NeuralVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Set canvas size
        this.canvas.width = 300;
        this.canvas.height = 200;
        
        // Spike data
        this.spikeData = [];
        this.maxSpikes = 100;
        
        // Rendering config
        this.spikeColor = '#0f0';
        this.bgColor = 'rgba(0, 10, 0, 0.1)';
        
        // Start animation
        this.animate();
    }
    
    addSpike(intensity = Math.random()) {
        this.spikeData.push({
            x: this.canvas.width,
            y: this.canvas.height / 2 + (Math.random() - 0.5) * intensity * 100,
            intensity: intensity,
            age: 0
        });
        
        // Limit data points for performance
        if (this.spikeData.length > this.maxSpikes) {
            this.spikeData.shift();
        }
    }
    
    draw() {
        // Fade effect
        this.ctx.fillStyle = this.bgColor;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw center line
        this.ctx.strokeStyle = 'rgba(0, 255, 0, 0.2)';
        this.ctx.lineWidth = 1;
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.canvas.height / 2);
        this.ctx.lineTo(this.canvas.width, this.canvas.height / 2);
        this.ctx.stroke();
        
        // Draw spikes
        this.ctx.strokeStyle = this.spikeColor;
        this.ctx.lineWidth = 2;
        
        for (let i = 1; i < this.spikeData.length; i++) {
            const prev = this.spikeData[i - 1];
            const curr = this.spikeData[i];
            
            // Fade older spikes
            const alpha = 1 - (curr.age / this.maxSpikes);
            this.ctx.globalAlpha = alpha;
            
            this.ctx.beginPath();
            this.ctx.moveTo(prev.x, prev.y);
            this.ctx.lineTo(curr.x, curr.y);
            this.ctx.stroke();
            
            // Update position (scroll left)
            curr.x -= 3;
            curr.age++;
        }
        
        this.ctx.globalAlpha = 1.0;
        
        // Remove off-screen spikes
        this.spikeData = this.spikeData.filter(spike => spike.x > 0);
    }
    
    animate() {
        // Generate random spikes
        if (Math.random() < 0.3) {
            this.addSpike(0.5 + Math.random() * 0.5);
        }
        
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize visualizer
document.addEventListener('DOMContentLoaded', () => {
    window.neuralVisualizer = new NeuralVisualizer('neural-canvas');
});
