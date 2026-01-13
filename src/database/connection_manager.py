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
        self.total_created = 0
        
        for _ in range(min_conn):
            try:
                conn = self.create_connection()
                self.available.append(conn)
                self.total_created += 1
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
            self.total_created += 1
            return conn
        raise Exception("No connections available")
    
    def return_connection(self, conn):
        if conn in self.in_use:
            self.in_use.remove(conn)
            self.available.append(conn)
    
    def get_statistics(self):
        return {
            "available_connections": len(self.available),
            "in_use_connections": len(self.in_use),
            "total_connections": len(self.available) + len(self.in_use),
            "max_connections": self.max_connections,
            "total_created": self.total_created,
            "total_reconnections": self.total_reconnections
        }
    
    def close_all(self):
        for conn in self.available + self.in_use:
            try:
                if hasattr(conn, 'close'):
                    conn.close()
            except:
                pass
        self.available.clear()
        self.in_use.clear()


class DatabaseManager:
    """Database manager with auto-reconnection"""
    
    def __init__(self, db_type="memory", config=None):
        self.db_type = db_type
        self.config = config or {}
        self.shared_data = {}  # Initialize shared data before pool
        self.pool = ConnectionPool(self._create_connection)
    
    def _create_connection(self):
        if self.db_type == "memory":
            # Return reference to shared data store
            return {"type": "memory", "data": self.shared_data, "connected": True}
        elif self.db_type == "file":
            return {"type": "file", "path": self.config.get("path", "data.json"), "data": self.shared_data, "connected": True}
        return {"type": "memory", "data": self.shared_data, "connected": True}
    
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
    
    def get_statistics(self):
        """Get database manager statistics"""
        stats = {
            "db_type": self.db_type,
            "config": {k: v for k, v in self.config.items() if k != 'password'}
        }
        stats["pool"] = self.pool.get_statistics()
        return stats
    
    def close(self):
        """Close all connections"""
        if self.pool:
            self.pool.close_all()
        logger.info("Database manager closed")
