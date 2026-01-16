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
Wetware Module - Biological Computing Interface

Provides software representation and control of biological computing components:
- Brain organoid simulation/interface
- Multi-electrode array (MEA) communication
- Biological signal processing
- Wetware lifecycle management
"""

from .organoid_core import OrganoidCore
from .mea_interface import MEAInterface
from .life_support import LifeSupport

__all__ = ['OrganoidCore', 'MEAInterface', 'LifeSupport']
