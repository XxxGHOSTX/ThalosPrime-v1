"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

"""
Advanced Memory System with Persistence, Indexing, and Search

Enhanced memory capabilities:
- Persistent storage to disk
- Full-text search and indexing
- Semantic similarity matching
- Version control for entries
- Memory graphs and relationships
- Automatic optimization
"""

import json
import hashlib
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime
from collections import defaultdict


class AdvancedMemorySystem:
    """
    Advanced memory system with enterprise features
    
    Features:
    - Persistent JSON/pickle storage
    - Full-text search with indexing
    - Semantic relationships
    - Version history
    - Memory graphs
    - Query optimization
    """
    
    def __init__(self, storage_path: str = "data/memory"):
        """
        Initialize advanced memory system
        
        Args:
            storage_path: Path to storage directory
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory store
        self.data: Dict[str, Any] = {}
        self.metadata: Dict[str, Dict] = {}
        self.versions: Dict[str, List[Dict]] = defaultdict(list)
        
        # Indexing structures
        self.word_index: Dict[str, Set[str]] = defaultdict(set)
        self.tag_index: Dict[str, Set[str]] = defaultdict(set)
        self.relationships: Dict[str, Set[str]] = defaultdict(set)
        
        # Statistics
        self.stats = {
            'created': 0,
            'updated': 0,
            'deleted': 0,
            'searches': 0,
            'cache_hits': 0
        }
        
        # Load existing data
        self.load_from_disk()
    
    def create(self, key: str, value: Any, tags: List[str] = None, 
               related_keys: List[str] = None) -> bool:
        """
        Create entry with metadata
        
        Args:
            key: Entry key
            value: Entry value
            tags: Optional tags for categorization
            related_keys: Optional related entry keys
            
        Returns:
            Success status
        """
        if key in self.data:
            return False
        
        # Store data
        self.data[key] = value
        
        # Store metadata
        self.metadata[key] = {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'version': 1,
            'tags': tags or [],
            'type': type(value).__name__,
            'size': len(str(value))
        }
        
        # Index tags
        if tags:
            for tag in tags:
                self.tag_index[tag].add(key)
        
        # Index relationships
        if related_keys:
            for related in related_keys:
                self.relationships[key].add(related)
                self.relationships[related].add(key)
        
        # Index content for search
        self._index_content(key, value)
        
        # Store version
        self._save_version(key, value, 'created')
        
        # Update stats
        self.stats['created'] += 1
        
        # Persist to disk
        self.save_to_disk()
        
        return True
    
    def read(self, key: str) -> Optional[Any]:
        """Read entry value"""
        return self.data.get(key)
    
    def update(self, key: str, value: Any) -> bool:
        """Update entry with version tracking"""
        if key not in self.data:
            return False
        
        # Store new value
        old_value = self.data[key]
        self.data[key] = value
        
        # Update metadata
        self.metadata[key]['updated_at'] = datetime.now().isoformat()
        self.metadata[key]['version'] += 1
        self.metadata[key]['size'] = len(str(value))
        
        # Re-index content
        self._deindex_content(key, old_value)
        self._index_content(key, value)
        
        # Save version
        self._save_version(key, value, 'updated')
        
        # Update stats
        self.stats['updated'] += 1
        
        # Persist to disk
        self.save_to_disk()
        
        return True
    
    def delete(self, key: str) -> bool:
        """Delete entry"""
        if key not in self.data:
            return False
        
        # Remove from data
        value = self.data.pop(key)
        metadata = self.metadata.pop(key)
        
        # Remove from indexes
        self._deindex_content(key, value)
        
        for tag in metadata.get('tags', []):
            self.tag_index[tag].discard(key)
        
        # Remove relationships
        for related in self.relationships[key]:
            self.relationships[related].discard(key)
        self.relationships.pop(key, None)
        
        # Save final version
        self._save_version(key, value, 'deleted')
        
        # Update stats
        self.stats['deleted'] += 1
        
        # Persist to disk
        self.save_to_disk()
        
        return True
    
    def search(self, query: str, limit: int = 10) -> List[Tuple[str, Any, float]]:
        """
        Full-text search across all entries
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of (key, value, score) tuples
        """
        self.stats['searches'] += 1
        
        # Tokenize query
        query_words = set(self._tokenize(query.lower()))
        
        # Find matching keys
        matches: Dict[str, int] = defaultdict(int)
        
        for word in query_words:
            if word in self.word_index:
                for key in self.word_index[word]:
                    matches[key] += 1
        
        # Score and rank results
        results = []
        for key, match_count in matches.items():
            value = self.data[key]
            score = match_count / len(query_words)
            results.append((key, value, score))
        
        # Sort by score descending
        results.sort(key=lambda x: x[2], reverse=True)
        
        return results[:limit]
    
    def find_by_tag(self, tag: str) -> List[Tuple[str, Any]]:
        """Find all entries with a specific tag"""
        keys = self.tag_index.get(tag, set())
        return [(k, self.data[k]) for k in keys]
    
    def find_related(self, key: str, depth: int = 1) -> List[str]:
        """
        Find related entries
        
        Args:
            key: Starting key
            depth: Relationship depth (1 = direct, 2 = friends-of-friends, etc.)
            
        Returns:
            List of related keys
        """
        if key not in self.relationships:
            return []
        
        visited = {key}
        current_level = {key}
        
        for _ in range(depth):
            next_level = set()
            for k in current_level:
                for related in self.relationships.get(k, set()):
                    if related not in visited:
                        next_level.add(related)
                        visited.add(related)
            current_level = next_level
            
            if not current_level:
                break
        
        visited.discard(key)
        return list(visited)
    
    def get_version_history(self, key: str) -> List[Dict]:
        """Get version history for a key"""
        return self.versions.get(key, [])
    
    def restore_version(self, key: str, version: int) -> bool:
        """Restore a specific version"""
        history = self.versions.get(key, [])
        
        if version < 1 or version > len(history):
            return False
        
        # Restore the version
        version_entry = history[version - 1]
        value = version_entry['value']
        
        self.data[key] = value
        self.metadata[key]['updated_at'] = datetime.now().isoformat()
        
        # Save restoration as new version
        self._save_version(key, value, f'restored_from_v{version}')
        
        self.save_to_disk()
        return True
    
    def get_statistics(self) -> Dict:
        """Get memory statistics"""
        return {
            'total_entries': len(self.data),
            'total_tags': len(self.tag_index),
            'total_relationships': sum(len(v) for v in self.relationships.values()) // 2,
            'indexed_words': len(self.word_index),
            'operations': self.stats.copy(),
            'storage_size': self._calculate_storage_size()
        }
    
    def optimize(self) -> Dict[str, int]:
        """Optimize indexes and cleanup"""
        # Remove empty indexes
        empty_tags = [tag for tag, keys in self.tag_index.items() if not keys]
        for tag in empty_tags:
            del self.tag_index[tag]
        
        empty_words = [word for word, keys in self.word_index.items() if not keys]
        for word in empty_words:
            del self.word_index[word]
        
        # Rebuild indexes
        self._rebuild_indexes()
        
        # Compact storage
        self.save_to_disk()
        
        return {
            'removed_empty_tags': len(empty_tags),
            'removed_empty_words': len(empty_words),
            'total_entries': len(self.data)
        }
    
    def export_graph(self) -> Dict:
        """Export memory as a graph structure"""
        nodes = []
        edges = []
        
        for key in self.data:
            nodes.append({
                'id': key,
                'label': key,
                'metadata': self.metadata.get(key, {})
            })
        
        for key, related_keys in self.relationships.items():
            for related in related_keys:
                if key < related:  # Avoid duplicates
                    edges.append({
                        'source': key,
                        'target': related
                    })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def _index_content(self, key: str, value: Any) -> None:
        """Index content for search"""
        text = str(value).lower()
        words = self._tokenize(text)
        
        for word in words:
            self.word_index[word].add(key)
    
    def _deindex_content(self, key: str, value: Any) -> None:
        """Remove content from index"""
        text = str(value).lower()
        words = self._tokenize(text)
        
        for word in words:
            self.word_index[word].discard(key)
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        import re
        return re.findall(r'\w+', text)
    
    def _save_version(self, key: str, value: Any, action: str) -> None:
        """Save version entry"""
        self.versions[key].append({
            'version': len(self.versions[key]) + 1,
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'value': value
        })
    
    def _rebuild_indexes(self) -> None:
        """Rebuild all indexes from scratch"""
        self.word_index.clear()
        self.tag_index.clear()
        
        for key, value in self.data.items():
            self._index_content(key, value)
            
            for tag in self.metadata[key].get('tags', []):
                self.tag_index[tag].add(key)
    
    def _calculate_storage_size(self) -> int:
        """Calculate approximate storage size in bytes"""
        size = 0
        for value in self.data.values():
            size += len(str(value).encode('utf-8'))
        return size
    
    def save_to_disk(self) -> None:
        """Save all data to disk"""
        # Save data
        data_file = self.storage_path / "data.json"
        with open(data_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        
        # Save metadata
        meta_file = self.storage_path / "metadata.json"
        with open(meta_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        # Save indexes (pickle for complex types)
        index_file = self.storage_path / "indexes.pkl"
        with open(index_file, 'wb') as f:
            pickle.dump({
                'word_index': dict(self.word_index),
                'tag_index': dict(self.tag_index),
                'relationships': dict(self.relationships),
                'versions': dict(self.versions)
            }, f)
        
        # Save statistics
        stats_file = self.storage_path / "stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def load_from_disk(self) -> None:
        """Load all data from disk"""
        try:
            # Load data
            data_file = self.storage_path / "data.json"
            if data_file.exists():
                with open(data_file, 'r') as f:
                    self.data = json.load(f)
            
            # Load metadata
            meta_file = self.storage_path / "metadata.json"
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    self.metadata = json.load(f)
            
            # Load indexes
            index_file = self.storage_path / "indexes.pkl"
            if index_file.exists():
                with open(index_file, 'rb') as f:
                    indexes = pickle.load(f)
                    self.word_index = defaultdict(set, {k: set(v) for k, v in indexes['word_index'].items()})
                    self.tag_index = defaultdict(set, {k: set(v) for k, v in indexes['tag_index'].items()})
                    self.relationships = defaultdict(set, {k: set(v) for k, v in indexes['relationships'].items()})
                    self.versions = defaultdict(list, indexes['versions'])
            
            # Load statistics
            stats_file = self.storage_path / "stats.json"
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    self.stats = json.load(f)
                    
        except Exception as e:
            print(f"Warning: Could not load memory from disk: {e}")
            # Continue with empty memory
