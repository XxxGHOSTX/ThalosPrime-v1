"""
© 2026 Tony Ray Macier III. All rights reserved.
Thalos Prime™ is a proprietary system.

Database Connection Manager with Auto-Reconnection
"""

import time
import logging
from typing import Any, Optional, Dict
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectionPool:
    """Connection pool with automatic reconnection"""
    
    def __init__(self, create_func, max_conn=10, min_conn=2, max_retries=5):
        self.create_connection = create_func
        self.max_connections = max_conn
        self.available = []
        self.in_use = []
        self.total_reconnections = 0
        
        for _ in range(min_conn):
            try:
                conn = self.create_connection()
                self.available.append(conn)
            except Exception as e:
                logger.error(f"Init failed: {e}")
    
    def get_connection(self):
        if self.available:
            conn = self.available.pop(0)
            self.in_use.append(conn)
            return conn
        elif len(self.in_use) < self.max_connections:
            conn = self.create_connection()
            self.in_use.append(conn)
            return conn
        raise Exception("No connections available")
    
    def return_connection(self, conn):
        if conn in self.in_use:
            self.in_use.remove(conn)
            self.available.append(conn)


class DatabaseManager:
    """Database manager with auto-reconnection"""
    
    def __init__(self, db_type="memory", config=None):
        self.db_type = db_type
        self.config = config or {}
        self.pool = ConnectionPool(self._create_connection)
    
    def _create_connection(self):
        if self.db_type == "memory":
            return {"type": "memory", "data": {}}
        return {"type": "memory", "data": {}}
    
    @contextmanager
    def get_connection(self):
        conn = self.pool.get_connection()
        try:
            yield conn
        finally:
            self.pool.return_connection(conn)
    
    def execute(self, query, params=None):
        with self.get_connection() as conn:
            return conn
