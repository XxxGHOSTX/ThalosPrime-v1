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
Application Programming Interface for Thalos Prime

Minimal REST surface:
- Health/status endpoint at minimum
- No persistence assumptions
- Mirrors CLI capabilities
"""

from typing import Dict, Any, Optional
import json


class API:
    """
    Application Programming Interface for Thalos Prime
    
    Principles:
    - Minimal REST surface
    - Health and status endpoints
    - No persistence assumptions
    - Mirrors CLI capabilities via CIS delegation
    """
    
    def __init__(self, cis: Optional[Any] = None):
        """
        Initialize the API
        
        Args:
            cis: CIS instance to delegate to (optional, can be set later)
        """
        self.cis = cis
        
    def set_cis(self, cis: Any) -> None:
        """
        Set the CIS instance to delegate to
        
        Args:
            cis: CIS instance
        """
        self.cis = cis
        
    def handle_request(self, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle an API request - delegates to CIS
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: Request path
            body: Optional request body
            
        Returns:
            Response dictionary with status, code, and data
        """
        # Health endpoint
        if method == 'GET' and path == '/health':
            return self._health_endpoint()
            
        # Status endpoint
        if method == 'GET' and path == '/status':
            return self._status_endpoint()
            
        # Memory endpoints
        if path.startswith('/memory'):
            return self._handle_memory_request(method, path, body)
            
        # Codegen endpoints
        if path.startswith('/codegen'):
            return self._handle_codegen_request(method, path, body)
            
        # Boot endpoint
        if method == 'POST' and path == '/boot':
            return self._boot_endpoint()
            
        # Shutdown endpoint
        if method == 'POST' and path == '/shutdown':
            return self._shutdown_endpoint()
            
        return {
            'status': 'error',
            'code': 404,
            'message': f'Endpoint not found: {method} {path}'
        }
        
    def _health_endpoint(self) -> Dict[str, Any]:
        """Health check endpoint"""
        return {
            'status': 'success',
            'code': 200,
            'data': {
                'healthy': True,
                'service': 'Thalos Prime',
                'version': '1.0'
            }
        }
        
    def _status_endpoint(self) -> Dict[str, Any]:
        """Status endpoint - delegates to CIS"""
        if not self.cis:
            return {
                'status': 'error',
                'code': 500,
                'message': 'CIS not initialized'
            }
            
        status = self.cis.status()
        return {
            'status': 'success',
            'code': 200,
            'data': status
        }
        
    def _boot_endpoint(self) -> Dict[str, Any]:
        """Boot endpoint - delegates to CIS"""
        if not self.cis:
            return {
                'status': 'error',
                'code': 500,
                'message': 'CIS not initialized'
            }
            
        result = self.cis.boot()
        return {
            'status': 'success' if result else 'error',
            'code': 200 if result else 400,
            'data': {'booted': result}
        }
        
    def _shutdown_endpoint(self) -> Dict[str, Any]:
        """Shutdown endpoint - delegates to CIS"""
        if not self.cis:
            return {
                'status': 'error',
                'code': 500,
                'message': 'CIS not initialized'
            }
            
        result = self.cis.shutdown()
        return {
            'status': 'success' if result else 'error',
            'code': 200 if result else 400,
            'data': {'shutdown': result}
        }
        
    def _handle_memory_request(self, method: str, path: str, body: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle memory-related requests - delegates to CIS memory subsystem"""
        if not self.cis:
            return {'status': 'error', 'code': 500, 'message': 'CIS not initialized'}
            
        memory = self.cis.get_memory()
        if not memory:
            return {'status': 'error', 'code': 500, 'message': 'Memory subsystem not initialized'}
            
        # POST /memory - create
        if method == 'POST' and path == '/memory':
            if not body or 'key' not in body or 'value' not in body:
                return {'status': 'error', 'code': 400, 'message': 'Missing key or value'}
            result = memory.create(body['key'], body['value'])
            return {
                'status': 'success' if result else 'error',
                'code': 200 if result else 409,
                'data': {'created': result}
            }
            
        # GET /memory/{key} - read
        if method == 'GET' and path.startswith('/memory/'):
            key = path.split('/')[-1]
            value = memory.read(key)
            if value is not None:
                return {'status': 'success', 'code': 200, 'data': {'key': key, 'value': value}}
            return {'status': 'error', 'code': 404, 'message': 'Key not found'}
            
        # PUT /memory/{key} - update
        if method == 'PUT' and path.startswith('/memory/'):
            key = path.split('/')[-1]
            if not body or 'value' not in body:
                return {'status': 'error', 'code': 400, 'message': 'Missing value'}
            result = memory.update(key, body['value'])
            return {
                'status': 'success' if result else 'error',
                'code': 200 if result else 404,
                'data': {'updated': result}
            }
            
        # DELETE /memory/{key} - delete
        if method == 'DELETE' and path.startswith('/memory/'):
            key = path.split('/')[-1]
            result = memory.delete(key)
            return {
                'status': 'success' if result else 'error',
                'code': 200 if result else 404,
                'data': {'deleted': result}
            }
            
        # GET /memory - list keys
        if method == 'GET' and path == '/memory':
            keys = memory.list_keys()
            return {'status': 'success', 'code': 200, 'data': {'keys': keys, 'count': len(keys)}}
            
        return {'status': 'error', 'code': 405, 'message': 'Method not allowed'}
        
    def _handle_codegen_request(self, method: str, path: str, body: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Handle codegen-related requests - delegates to CIS codegen subsystem"""
        if not self.cis:
            return {'status': 'error', 'code': 500, 'message': 'CIS not initialized'}
            
        codegen = self.cis.get_codegen()
        if not codegen:
            return {'status': 'error', 'code': 500, 'message': 'Codegen subsystem not initialized'}
            
        # POST /codegen/class - generate class
        if method == 'POST' and path == '/codegen/class':
            if not body or 'name' not in body:
                return {'status': 'error', 'code': 400, 'message': 'Missing class name'}
            methods = body.get('methods', ['__init__'])
            code = codegen.generate_class(body['name'], methods)
            return {'status': 'success', 'code': 200, 'data': {'code': code}}
            
        # POST /codegen/function - generate function
        if method == 'POST' and path == '/codegen/function':
            if not body or 'name' not in body:
                return {'status': 'error', 'code': 400, 'message': 'Missing function name'}
            params = body.get('parameters', [])
            code = codegen.generate_function(body['name'], params)
            return {'status': 'success', 'code': 200, 'data': {'code': code}}
            
        return {'status': 'error', 'code': 405, 'message': 'Method not allowed'}
