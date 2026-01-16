"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
System Orchestrator - Lifecycle Management and Coordination

Complete orchestration of all subsystems with:
- Lifecycle enforcement (initialize, validate, operate, reconcile, checkpoint, terminate)
- State machine with deterministic transitions
- Dependency resolution
- Health monitoring
- Auto-recovery and self-healing
- Resource optimization
"""

from typing import Dict, List, Set, Optional, Any
from enum import Enum
from datetime import datetime
from ..exceptions import (
    LifecycleError, StateError, DependencyError, 
    ReconciliationError, CheckpointError
)
from ..logging import get_logger

logger = get_logger()


class LifecycleState(Enum):
    """Lifecycle states for subsystems"""
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    VALIDATING = "validating"
    OPERATIONAL = "operational"
    RECONCILING = "reconciling"
    CHECKPOINTING = "checkpointing"
    TERMINATING = "terminating"
    TERMINATED = "terminated"
    FAILED = "failed"


class SubsystemProtocol:
    """
    Protocol that all subsystems must implement
    
    Required methods for complete lifecycle management
    """
    
    def initialize(self) -> bool:
        """Allocate resources, verify preconditions"""
        raise NotImplementedError
    
    def validate(self) -> bool:
        """Resolve discrepancies, block startup if unresolved"""
        raise NotImplementedError
    
    def operate(self) -> bool:
        """Perform declared function only"""
        raise NotImplementedError
    
    def reconcile(self) -> bool:
        """Correct internal inconsistency"""
        raise NotImplementedError
    
    def checkpoint(self) -> Dict[str, Any]:
        """Persist full deterministic state"""
        raise NotImplementedError
    
    def terminate(self) -> bool:
        """Leave system restartable and coherent"""
        raise NotImplementedError
    
    def get_state(self) -> Dict[str, Any]:
        """Get current observable state"""
        raise NotImplementedError
    
    def get_health(self) -> Dict[str, Any]:
        """Get health metrics"""
        raise NotImplementedError


class SystemOrchestrator:
    """
    Central orchestrator for all subsystems
    
    Enforces lifecycle, manages dependencies, monitors health
    """
    
    def __init__(self):
        """Initialize orchestrator"""
        self.subsystems: Dict[str, Any] = {}
        self.states: Dict[str, LifecycleState] = {}
        self.dependencies: Dict[str, Set[str]] = {}
        self.checkpoints: Dict[str, List[Dict]] = {}
        self.health_metrics: Dict[str, Dict] = {}
        
        self.orchestrator_state = LifecycleState.UNINITIALIZED
        self.recovery_attempts: Dict[str, int] = {}
        self.max_recovery_attempts = 3
        
        logger.info("Orchestrator initialized")
    
    def register_subsystem(self, name: str, subsystem: Any, 
                          depends_on: List[str] = None) -> None:
        """
        Register a subsystem with the orchestrator
        
        Args:
            name: Subsystem name
            subsystem: Subsystem instance
            depends_on: List of dependency names
        """
        if name in self.subsystems:
            raise LifecycleError(
                f"Subsystem '{name}' already registered",
                phase="registration",
                subsystem=name
            )
        
        self.subsystems[name] = subsystem
        self.states[name] = LifecycleState.UNINITIALIZED
        self.dependencies[name] = set(depends_on or [])
        self.checkpoints[name] = []
        self.recovery_attempts[name] = 0
        
        logger.info(f"Registered subsystem: {name}", 
                   extra={'dependencies': list(depends_on or [])})
    
    def initialize_all(self) -> bool:
        """
        Initialize all subsystems in dependency order
        
        Returns:
            Success status
        """
        logger.lifecycle("initialize_all", "orchestrator", "starting")
        
        # Resolve initialization order
        order = self._resolve_dependencies()
        
        for name in order:
            if not self._initialize_subsystem(name):
                logger.error(f"Failed to initialize subsystem: {name}")
                self.orchestrator_state = LifecycleState.FAILED
                return False
        
        self.orchestrator_state = LifecycleState.OPERATIONAL
        logger.lifecycle("initialize_all", "orchestrator", "complete")
        return True
    
    def validate_all(self) -> bool:
        """
        Validate all subsystems
        
        Returns:
            Success status
        """
        logger.lifecycle("validate_all", "orchestrator", "starting")
        
        for name, subsystem in self.subsystems.items():
            try:
                self._transition_state(name, LifecycleState.VALIDATING)
                
                if not subsystem.validate():
                    raise LifecycleError(
                        f"Validation failed for subsystem: {name}",
                        phase="validate",
                        subsystem=name
                    )
                
                self._transition_state(name, LifecycleState.OPERATIONAL)
                logger.lifecycle("validate", name, "success")
                
            except Exception as e:
                logger.exception(f"Validation error for {name}: {e}")
                self.states[name] = LifecycleState.FAILED
                return False
        
        logger.lifecycle("validate_all", "orchestrator", "complete")
        return True
    
    def operate_subsystem(self, name: str) -> bool:
        """Execute subsystem operation"""
        if name not in self.subsystems:
            raise DependencyError(f"Unknown subsystem: {name}")
        
        if self.states[name] != LifecycleState.OPERATIONAL:
            raise StateError(
                f"Subsystem '{name}' not operational",
                current_state=self.states[name].value,
                expected_state=LifecycleState.OPERATIONAL.value
            )
        
        try:
            return self.subsystems[name].operate()
        except Exception as e:
            logger.exception(f"Operation error for {name}: {e}")
            self._handle_failure(name)
            return False
    
    def reconcile_subsystem(self, name: str) -> bool:
        """Reconcile subsystem state"""
        if name not in self.subsystems:
            raise DependencyError(f"Unknown subsystem: {name}")
        
        try:
            self._transition_state(name, LifecycleState.RECONCILING)
            
            if not self.subsystems[name].reconcile():
                raise ReconciliationError(
                    f"Reconciliation failed for subsystem: {name}"
                )
            
            self._transition_state(name, LifecycleState.OPERATIONAL)
            logger.lifecycle("reconcile", name, "success")
            return True
            
        except Exception as e:
            logger.exception(f"Reconciliation error for {name}: {e}")
            self.states[name] = LifecycleState.FAILED
            return False
    
    def checkpoint_subsystem(self, name: str) -> bool:
        """Create checkpoint for subsystem"""
        if name not in self.subsystems:
            raise DependencyError(f"Unknown subsystem: {name}")
        
        try:
            self._transition_state(name, LifecycleState.CHECKPOINTING)
            
            checkpoint_data = self.subsystems[name].checkpoint()
            checkpoint_data['timestamp'] = datetime.now().isoformat()
            checkpoint_data['state'] = self.states[name].value
            
            self.checkpoints[name].append(checkpoint_data)
            
            # Keep only last 10 checkpoints
            if len(self.checkpoints[name]) > 10:
                self.checkpoints[name] = self.checkpoints[name][-10:]
            
            self._transition_state(name, LifecycleState.OPERATIONAL)
            logger.lifecycle("checkpoint", name, "success")
            return True
            
        except Exception as e:
            logger.exception(f"Checkpoint error for {name}: {e}")
            return False
    
    def checkpoint_all(self) -> bool:
        """Create checkpoints for all subsystems"""
        logger.lifecycle("checkpoint_all", "orchestrator", "starting")
        
        success = True
        for name in self.subsystems:
            if not self.checkpoint_subsystem(name):
                logger.error(f"Failed to checkpoint subsystem: {name}")
                success = False
        
        logger.lifecycle("checkpoint_all", "orchestrator", "complete")
        return success
    
    def terminate_all(self) -> bool:
        """Terminate all subsystems in reverse dependency order"""
        logger.lifecycle("terminate_all", "orchestrator", "starting")
        
        # Reverse of initialization order
        order = list(reversed(self._resolve_dependencies()))
        
        success = True
        for name in order:
            try:
                self._transition_state(name, LifecycleState.TERMINATING)
                
                if not self.subsystems[name].terminate():
                    logger.error(f"Failed to terminate subsystem: {name}")
                    success = False
                else:
                    self._transition_state(name, LifecycleState.TERMINATED)
                    logger.lifecycle("terminate", name, "success")
                    
            except Exception as e:
                logger.exception(f"Termination error for {name}: {e}")
                success = False
        
        self.orchestrator_state = LifecycleState.TERMINATED
        logger.lifecycle("terminate_all", "orchestrator", "complete")
        return success
    
    def get_system_state(self) -> Dict[str, Any]:
        """Get complete system state"""
        return {
            'orchestrator_state': self.orchestrator_state.value,
            'subsystems': {
                name: {
                    'state': self.states[name].value,
                    'health': self.health_metrics.get(name, {}),
                    'checkpoints': len(self.checkpoints[name]),
                    'recovery_attempts': self.recovery_attempts[name]
                }
                for name in self.subsystems
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def monitor_health(self) -> Dict[str, Dict]:
        """Monitor health of all subsystems"""
        for name, subsystem in self.subsystems.items():
            try:
                health = subsystem.get_health()
                self.health_metrics[name] = health
                
                # Check for critical issues
                if health.get('status') == 'critical':
                    logger.warning(f"Critical health for {name}: {health}")
                    self._handle_failure(name)
                    
            except Exception as e:
                logger.exception(f"Health check error for {name}: {e}")
                self.health_metrics[name] = {'status': 'error', 'error': str(e)}
        
        return self.health_metrics
    
    def _initialize_subsystem(self, name: str) -> bool:
        """Initialize single subsystem"""
        try:
            # Check dependencies
            for dep in self.dependencies[name]:
                if self.states.get(dep) != LifecycleState.OPERATIONAL:
                    raise DependencyError(
                        f"Dependency '{dep}' not operational for '{name}'"
                    )
            
            self._transition_state(name, LifecycleState.INITIALIZING)
            
            if not self.subsystems[name].initialize():
                raise LifecycleError(
                    f"Initialization failed for subsystem: {name}",
                    phase="initialize",
                    subsystem=name
                )
            
            self._transition_state(name, LifecycleState.OPERATIONAL)
            logger.lifecycle("initialize", name, "success")
            return True
            
        except Exception as e:
            logger.exception(f"Initialization error for {name}: {e}")
            self.states[name] = LifecycleState.FAILED
            return False
    
    def _resolve_dependencies(self) -> List[str]:
        """Resolve subsystem dependencies to initialization order"""
        # Topological sort
        result = []
        visited = set()
        temp_mark = set()
        
        def visit(name):
            if name in temp_mark:
                raise DependencyError(f"Circular dependency detected involving '{name}'")
            if name in visited:
                return
            
            temp_mark.add(name)
            
            for dep in self.dependencies.get(name, []):
                if dep in self.subsystems:
                    visit(dep)
            
            temp_mark.remove(name)
            visited.add(name)
            result.append(name)
        
        for name in self.subsystems:
            if name not in visited:
                visit(name)
        
        return result
    
    def _transition_state(self, name: str, new_state: LifecycleState) -> None:
        """Transition subsystem to new state"""
        old_state = self.states[name]
        self.states[name] = new_state
        
        logger.state_transition(name, old_state.value, new_state.value)
    
    def _handle_failure(self, name: str) -> None:
        """Handle subsystem failure with auto-recovery"""
        self.states[name] = LifecycleState.FAILED
        self.recovery_attempts[name] += 1
        
        if self.recovery_attempts[name] <= self.max_recovery_attempts:
            logger.warning(
                f"Attempting recovery for {name} (attempt {self.recovery_attempts[name]})"
            )
            
            # Try to reconcile first
            if self.reconcile_subsystem(name):
                logger.info(f"Successfully recovered {name} through reconciliation")
                self.recovery_attempts[name] = 0
                return
            
            # Try to reinitialize
            if self._initialize_subsystem(name):
                logger.info(f"Successfully recovered {name} through reinitialization")
                self.recovery_attempts[name] = 0
                return
        
        logger.critical(
            f"Failed to recover subsystem {name} after {self.recovery_attempts[name]} attempts"
        )
