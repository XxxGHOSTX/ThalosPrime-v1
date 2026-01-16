"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
System Validator - State Consistency and Integrity Checks

Validates system state across all subsystems:
- Data integrity checks
- Consistency validation
- Invariant enforcement
- Conflict detection and resolution
"""

from typing import Dict, List, Any, Optional
from ..exceptions import ValidationError, StateError
from ..logging import get_logger

logger = get_logger()


class SystemValidator:
    """
    Validates system state and enforces invariants
    
    Blocks startup if critical issues detected
    """
    
    def __init__(self):
        """Initialize validator"""
        self.validation_rules = []
        self.validation_history = []
        
    def add_rule(self, name: str, rule_fn, critical: bool = False) -> None:
        """
        Add validation rule
        
        Args:
            name: Rule name
            rule_fn: Function that returns (bool, str) - (valid, message)
            critical: Whether failure blocks operation
        """
        self.validation_rules.append({
            'name': name,
            'function': rule_fn,
            'critical': critical
        })
    
    def validate_system(self, system_state: Dict[str, Any]) -> bool:
        """
        Validate complete system state
        
        Args:
            system_state: Complete system state dictionary
            
        Returns:
            Valid status
            
        Raises:
            ValidationError: If critical validation fails
        """
        logger.info("Starting system validation")
        
        results = []
        critical_failures = []
        
        for rule in self.validation_rules:
            try:
                valid, message = rule['function'](system_state)
                
                result = {
                    'rule': rule['name'],
                    'valid': valid,
                    'message': message,
                    'critical': rule['critical']
                }
                results.append(result)
                
                if not valid:
                    logger.warning(f"Validation failed: {rule['name']} - {message}")
                    
                    if rule['critical']:
                        critical_failures.append(result)
                        
            except Exception as e:
                logger.exception(f"Validation error for rule {rule['name']}: {e}")
                if rule['critical']:
                    critical_failures.append({
                        'rule': rule['name'],
                        'valid': False,
                        'message': str(e),
                        'critical': True
                    })
        
        # Store validation history
        self.validation_history.append({
            'timestamp': datetime.now().isoformat(),
            'results': results,
            'passed': len(critical_failures) == 0
        })
        
        # Raise if critical failures
        if critical_failures:
            failure_messages = [f"  - {r['rule']}: {r['message']}" for r in critical_failures]
            raise ValidationError(
                f"Critical validation failures:\n" + "\n".join(failure_messages),
                details={'failures': critical_failures}
            )
        
        logger.info(f"System validation complete: {len(results)} rules checked")
        return True


from datetime import datetime
