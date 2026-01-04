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
Thalos Prime v1.0 - Main Package
"""

from .core import CIS, MemoryModule
from .interfaces import CLI, API
from .codegen import CodeGenerator

__version__ = '1.0'

__all__ = ['CIS', 'MemoryModule', 'CLI', 'API', 'CodeGenerator']
