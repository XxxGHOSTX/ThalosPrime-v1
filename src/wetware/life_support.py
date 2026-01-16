"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Life Support System - Biological Homeostasis Management

Maintains biological viability of wetware components:
- Nutrient flow (glucose/oxygen delivery)
- Waste removal (lactate scrubbing)
- Temperature regulation
- pH balance
- Microfluidic perfusion control
"""

from typing import Dict, Any, Optional
import time


class LifeSupport:
    """
    Life Support System for Wetware Core
    
    Ensures biological viability through:
    - Nutrient delivery
    - Waste removal
    - Environmental regulation
    - Health monitoring
    """
    
    def __init__(self):
        self.active = False
        self.status = "dormant"
        
        # Environmental parameters
        self.temperature = 37.0  # °C (body temperature)
        self.ph_level = 7.4  # Physiological pH
        self.oxygen_level = 95.0  # % saturation
        self.glucose_level = 5.0  # mM
        
        # Flow rates (µL/min)
        self.perfusion_rate = 50.0
        self.waste_removal_rate = 45.0
        
        # Nutrient levels
        self.nutrient_reservoir = 100.0  # % full
        self.waste_reservoir = 0.0  # % full
        
        # Monitoring
        self.last_check_time = time.time()
        self.health_alerts = []
        
        # Operational limits
        self.temp_min = 36.5
        self.temp_max = 37.5
        self.ph_min = 7.2
        self.ph_max = 7.6
        self.oxygen_min = 90.0
        self.glucose_min = 3.0
        self.glucose_max = 7.0
        
    def initialize(self) -> bool:
        """
        Initialize life support systems
        
        Returns:
            bool: True if initialization successful
        """
        if self.active:
            return True
        
        # Check initial conditions
        if not self._check_environmental_safety():
            return False
        
        # Start perfusion
        self.active = True
        self.status = "operational"
        self.last_check_time = time.time()
        
        return True
    
    def _check_environmental_safety(self) -> bool:
        """Check if environmental parameters are within safe ranges"""
        checks = [
            self.temp_min <= self.temperature <= self.temp_max,
            self.ph_min <= self.ph_level <= self.ph_max,
            self.oxygen_level >= self.oxygen_min,
            self.glucose_min <= self.glucose_level <= self.glucose_max
        ]
        return all(checks)
    
    def update(self, dt: float = 1.0) -> Dict[str, Any]:
        """
        Update life support systems
        
        Args:
            dt: Time step in seconds
            
        Returns:
            Status update dictionary
        """
        if not self.active:
            return {"status": "dormant"}
        
        # Deplete nutrients
        nutrient_consumption_rate = 0.1  # % per second
        self.nutrient_reservoir -= nutrient_consumption_rate * dt
        
        # Accumulate waste
        waste_production_rate = 0.08  # % per second
        self.waste_reservoir += waste_production_rate * dt
        
        # Regulate glucose (consumption by neurons)
        self.glucose_level -= 0.01 * dt
        
        # Oxygen consumption
        self.oxygen_level -= 0.05 * dt
        
        # Natural pH drift
        self.ph_level += (7.4 - self.ph_level) * 0.01 * dt  # Homeostatic correction
        
        # Temperature regulation
        self.temperature += (37.0 - self.temperature) * 0.05 * dt
        
        # Replenish if needed
        self._auto_replenish()
        
        # Check for alerts
        self._check_alerts()
        
        return self.get_status()
    
    def _auto_replenish(self) -> None:
        """Automatically replenish nutrients and remove waste"""
        # Refill nutrients if low
        if self.nutrient_reservoir < 20.0:
            self.nutrient_reservoir = min(100.0, self.nutrient_reservoir + self.perfusion_rate * 0.1)
            self.glucose_level = min(self.glucose_max, self.glucose_level + 0.1)
            self.oxygen_level = min(100.0, self.oxygen_level + 0.5)
        
        # Remove waste if high
        if self.waste_reservoir > 80.0:
            self.waste_reservoir = max(0.0, self.waste_reservoir - self.waste_removal_rate * 0.1)
    
    def _check_alerts(self) -> None:
        """Check for health alerts"""
        self.health_alerts.clear()
        
        if self.temperature < self.temp_min:
            self.health_alerts.append("HYPOTHERMIA_RISK")
        elif self.temperature > self.temp_max:
            self.health_alerts.append("HYPERTHERMIA_RISK")
        
        if self.ph_level < self.ph_min:
            self.health_alerts.append("ACIDOSIS")
        elif self.ph_level > self.ph_max:
            self.health_alerts.append("ALKALOSIS")
        
        if self.oxygen_level < self.oxygen_min:
            self.health_alerts.append("HYPOXIA")
        
        if self.glucose_level < self.glucose_min:
            self.health_alerts.append("HYPOGLYCEMIA")
        elif self.glucose_level > self.glucose_max:
            self.health_alerts.append("HYPERGLYCEMIA")
        
        if self.nutrient_reservoir < 10.0:
            self.health_alerts.append("NUTRIENT_DEPLETION")
        
        if self.waste_reservoir > 90.0:
            self.health_alerts.append("WASTE_ACCUMULATION")
        
        # Update status
        if self.health_alerts:
            self.status = "warning"
        else:
            self.status = "optimal"
    
    def deliver_nutrient_boost(self, amount: float = 20.0) -> bool:
        """
        Manually deliver nutrient boost
        
        Args:
            amount: Amount to deliver (%)
            
        Returns:
            bool: True if successful
        """
        if not self.active:
            return False
        
        self.nutrient_reservoir = min(100.0, self.nutrient_reservoir + amount)
        self.glucose_level = min(self.glucose_max, self.glucose_level + 1.0)
        self.oxygen_level = min(100.0, self.oxygen_level + 5.0)
        
        return True
    
    def emergency_flush(self) -> bool:
        """
        Emergency waste removal
        
        Returns:
            bool: True if successful
        """
        if not self.active:
            return False
        
        self.waste_reservoir = 0.0
        self.ph_level = 7.4
        
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current life support status
        
        Returns:
            Status dictionary
        """
        return {
            "active": self.active,
            "status": self.status,
            "temperature": round(self.temperature, 2),
            "ph_level": round(self.ph_level, 2),
            "oxygen_saturation": round(self.oxygen_level, 1),
            "glucose_level": round(self.glucose_level, 2),
            "nutrient_reservoir": round(self.nutrient_reservoir, 1),
            "waste_reservoir": round(self.waste_reservoir, 1),
            "perfusion_rate": self.perfusion_rate,
            "health_alerts": self.health_alerts,
            "safety_status": "SAFE" if self._check_environmental_safety() else "CRITICAL"
        }
    
    def get_viability_score(self) -> float:
        """
        Calculate overall biological viability score
        
        Returns:
            Viability score (0.0 to 1.0)
        """
        if not self.active:
            return 0.0
        
        # Calculate individual component scores
        temp_score = 1.0 if self.temp_min <= self.temperature <= self.temp_max else 0.5
        ph_score = 1.0 if self.ph_min <= self.ph_level <= self.ph_max else 0.5
        oxygen_score = self.oxygen_level / 100.0
        glucose_score = 1.0 if self.glucose_min <= self.glucose_level <= self.glucose_max else 0.5
        nutrient_score = self.nutrient_reservoir / 100.0
        waste_score = 1.0 - (self.waste_reservoir / 100.0)
        
        # Weighted average
        weights = [0.2, 0.2, 0.2, 0.15, 0.15, 0.1]
        scores = [temp_score, ph_score, oxygen_score, glucose_score, nutrient_score, waste_score]
        
        viability = sum(w * s for w, s in zip(weights, scores))
        return viability
    
    def shutdown(self) -> bool:
        """
        Gracefully shutdown life support
        
        Returns:
            bool: True if shutdown successful
        """
        if not self.active:
            return True
        
        # Gradual shutdown to prevent shock
        self.perfusion_rate *= 0.5
        time.sleep(0.1)
        
        self.active = False
        self.status = "dormant"
        
        return True
