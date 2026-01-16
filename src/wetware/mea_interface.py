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
MEA Interface - Multi-Electrode Array Communication

Manages communication with High-Density Multi-Electrode Arrays (HD-MEA)
- 20,000+ channel management
- Signal translation (digital to electrical pulses)
- Spike sorting and pattern recognition
- Bidirectional data flow
"""

from typing import Dict, List, Optional, Any, Tuple
import json


class MEAInterface:
    """
    Multi-Electrode Array Interface
    
    Manages the hardware interface between digital signals and biological neurons.
    Converts digital queries into electrical pulse patterns (10-100Hz) and
    reads spike trains from biological tissue.
    """
    
    def __init__(self, channels: int = 20000, sampling_rate: float = 20000.0):
        """
        Initialize MEA interface
        
        Args:
            channels: Number of electrode channels (default 20,000)
            sampling_rate: Sampling rate in Hz (default 20kHz)
        """
        self.channels = channels
        self.sampling_rate = sampling_rate
        self.active = False
        
        # Channel configuration
        self.channel_map: Dict[int, str] = {}  # Maps channel ID to function
        self.active_channels: List[int] = []
        
        # Signal processing
        self.input_buffer: List[Dict[str, Any]] = []
        self.output_buffer: List[Dict[str, Any]] = []
        
        # Spike sorting parameters
        self.spike_threshold = 0.05  # mV
        self.refractory_period = 2.0  # ms
        
        # Statistics
        self.total_spikes_sent = 0
        self.total_spikes_received = 0
        self.packet_loss_rate = 0.0
        
    def initialize(self) -> bool:
        """
        Initialize the MEA interface
        
        Returns:
            bool: True if initialization successful
        """
        if self.active:
            return True
            
        # Initialize channel mapping
        self._initialize_channel_map()
        
        # Activate interface
        self.active = True
        return True
        
    def _initialize_channel_map(self) -> None:
        """Initialize channel to function mapping"""
        # Distribute channels across functional regions
        channels_per_region = self.channels // 7
        
        regions = [
            "input_sensory",
            "pattern_recognition", 
            "associative_memory",
            "executive_function",
            "creative_synthesis",
            "ethical_evaluation",
            "output_motor"
        ]
        
        for idx, region in enumerate(regions):
            start_channel = idx * channels_per_region
            end_channel = start_channel + channels_per_region
            
            for channel in range(start_channel, min(end_channel, self.channels)):
                self.channel_map[channel] = region
                self.active_channels.append(channel)
                
    def encode_digital_to_pulse(self, digital_signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Encode digital signal into electrical pulse pattern
        
        Args:
            digital_signal: Digital query or command
            
        Returns:
            Pulse pattern for MEA transmission
        """
        if not self.active:
            return {"error": "MEA interface not active", "pulses": []}
            
        signal_type = digital_signal.get("type", "query")
        data = digital_signal.get("data", {})
        intensity = digital_signal.get("intensity", 0.5)
        
        # Convert to pulse train
        pulse_pattern = self._generate_pulse_pattern(signal_type, data, intensity)
        
        # Add to input buffer
        self.input_buffer.append(pulse_pattern)
        self.total_spikes_sent += len(pulse_pattern.get("pulses", []))
        
        return pulse_pattern
        
    def _generate_pulse_pattern(self, signal_type: str, data: Dict[str, Any], 
                                intensity: float) -> Dict[str, Any]:
        """
        Generate electrical pulse pattern from digital signal
        
        Args:
            signal_type: Type of signal (query, command, feedback)
            data: Signal data payload
            intensity: Signal strength (0.0 to 1.0)
            
        Returns:
            Pulse pattern structure
        """
        # Determine target channels based on signal type
        target_region = self._select_target_region(signal_type)
        target_channels = [ch for ch, region in self.channel_map.items() 
                          if region == target_region]
        
        # Calculate pulse frequency (10-100Hz range)
        base_frequency = 10.0  # Hz
        frequency = base_frequency + (intensity * 90.0)  # Scale to 10-100Hz
        
        # Generate pulse sequence
        duration = 100.0  # ms
        num_pulses = int((frequency * duration) / 1000.0)
        
        pulses = []
        for i in range(num_pulses):
            pulse = {
                "timestamp": i * (duration / num_pulses),  # ms
                "amplitude": intensity * 0.1,  # mV (0-100 µV)
                "duration": 1.0,  # ms
                "channels": target_channels[:min(100, len(target_channels))],  # Limit to 100 channels per pulse
                "waveform": "biphasic"
            }
            pulses.append(pulse)
            
        return {
            "signal_type": signal_type,
            "target_region": target_region,
            "frequency": frequency,
            "pulses": pulses,
            "num_channels": len(target_channels)
        }
        
    def _select_target_region(self, signal_type: str) -> str:
        """Select target brain region based on signal type"""
        region_map = {
            "query": "input_sensory",
            "pattern": "pattern_recognition",
            "logic": "executive_function",
            "creative": "creative_synthesis",
            "ethical": "ethical_evaluation",
            "command": "output_motor",
            "feedback": "associative_memory"
        }
        return region_map.get(signal_type, "input_sensory")
        
    def decode_spike_train(self, raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Decode spike train from biological tissue into digital signal
        
        Args:
            raw_data: Raw electrode readings or spike data
            
        Returns:
            Decoded digital signal
        """
        if not self.active:
            return {"error": "MEA interface not active", "decoded": False}
        
        # Handle empty or invalid input
        if not raw_data:
            return {
                "decoded": True,
                "confidence": 0.0,
                "response_type": "none",
                "firing_rate": 0.0,
                "synchrony": 0.0,
                "active_regions": 0,
                "data": {"patterns": [], "dominant_region": "none"}
            }
        
        # Perform spike sorting
        sorted_spikes = self._sort_spikes(raw_data)
        
        # Extract patterns
        patterns = self._extract_patterns(sorted_spikes)
        
        # Decode into digital representation
        decoded = self._pattern_to_digital(patterns)
        
        # Add to output buffer
        self.output_buffer.append(decoded)
        self.total_spikes_received += len(sorted_spikes)
        
        return decoded
        
    def _sort_spikes(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort and classify spikes from raw electrode data
        
        Args:
            raw_data: Raw voltage readings from electrodes
            
        Returns:
            Sorted and classified spikes
        """
        sorted_spikes = []
        
        for reading in raw_data:
            channel = reading.get("channel", 0)
            voltage = reading.get("voltage", 0.0)
            timestamp = reading.get("timestamp", 0.0)
            
            # Detect spike if voltage exceeds threshold
            if abs(voltage) > self.spike_threshold:
                spike = {
                    "channel": channel,
                    "timestamp": timestamp,
                    "amplitude": voltage,
                    "region": self.channel_map.get(channel, "unknown"),
                    "classified": True
                }
                sorted_spikes.append(spike)
                
        # Sort by timestamp
        sorted_spikes.sort(key=lambda x: x["timestamp"])
        
        return sorted_spikes
        
    def _extract_patterns(self, spikes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract temporal patterns from spike train
        
        Args:
            spikes: Sorted spike data
            
        Returns:
            Identified patterns
        """
        patterns = []
        
        # Group spikes by region
        region_groups: Dict[str, List[Dict[str, Any]]] = {}
        for spike in spikes:
            region = spike["region"]
            if region not in region_groups:
                region_groups[region] = []
            region_groups[region].append(spike)
            
        # Analyze each region's activity
        for region, region_spikes in region_groups.items():
            if len(region_spikes) < 2:
                continue
                
            # Calculate firing rate
            time_span = region_spikes[-1]["timestamp"] - region_spikes[0]["timestamp"]
            firing_rate = len(region_spikes) / (time_span / 1000.0) if time_span > 0 else 0
            
            # Calculate synchrony (simplified)
            avg_amplitude = sum(s["amplitude"] for s in region_spikes) / len(region_spikes)
            
            pattern = {
                "region": region,
                "spike_count": len(region_spikes),
                "firing_rate": firing_rate,
                "avg_amplitude": avg_amplitude,
                "synchrony": self._calculate_synchrony(region_spikes),
                "confidence": min(1.0, firing_rate / 50.0)  # Normalize to 0-1
            }
            patterns.append(pattern)
            
        return patterns
        
    def _calculate_synchrony(self, spikes: List[Dict[str, Any]]) -> float:
        """Calculate synchrony measure for spike train"""
        if len(spikes) < 2:
            return 0.0
            
        # Calculate inter-spike intervals
        intervals = []
        for i in range(len(spikes) - 1):
            interval = spikes[i + 1]["timestamp"] - spikes[i]["timestamp"]
            intervals.append(interval)
            
        # Synchrony is inversely related to interval variance
        if not intervals:
            return 0.0
            
        avg_interval = sum(intervals) / len(intervals)
        variance = sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)
        
        # Normalize to 0-1 scale
        synchrony = 1.0 / (1.0 + variance / 10.0)
        return synchrony
        
    def _pattern_to_digital(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Convert biological patterns to digital representation
        
        Args:
            patterns: Extracted neural patterns
            
        Returns:
            Digital signal representation
        """
        if not patterns:
            return {
                "decoded": False,
                "confidence": 0.0,
                "response_type": "none",
                "data": {}
            }
            
        # Find dominant pattern
        dominant = max(patterns, key=lambda p: p["confidence"])
        
        # Map region to response type
        response_map = {
            "pattern_recognition": "pattern_detected",
            "executive_function": "logic_result",
            "creative_synthesis": "creative_output",
            "ethical_evaluation": "ethical_assessment",
            "output_motor": "action_command"
        }
        
        response_type = response_map.get(dominant["region"], "unknown")
        
        return {
            "decoded": True,
            "confidence": dominant["confidence"],
            "response_type": response_type,
            "firing_rate": dominant["firing_rate"],
            "synchrony": dominant["synchrony"],
            "active_regions": len(patterns),
            "data": {
                "patterns": patterns,
                "dominant_region": dominant["region"]
            }
        }
        
    def get_status(self) -> Dict[str, Any]:
        """
        Get current MEA interface status
        
        Returns:
            Status dictionary
        """
        return {
            "active": self.active,
            "total_channels": self.channels,
            "active_channels": len(self.active_channels),
            "sampling_rate": self.sampling_rate,
            "total_spikes_sent": self.total_spikes_sent,
            "total_spikes_received": self.total_spikes_received,
            "packet_loss_rate": round(self.packet_loss_rate, 4),
            "input_buffer_size": len(self.input_buffer),
            "output_buffer_size": len(self.output_buffer)
        }
        
    def shutdown(self) -> bool:
        """
        Shutdown the MEA interface
        
        Returns:
            bool: True if shutdown successful
        """
        if not self.active:
            return True
            
        # Clear buffers
        self.input_buffer.clear()
        self.output_buffer.clear()
        
        self.active = False
        return True
