"""
Search management system for the Media Management Bot.
Supports multiple search backends: MongoDB Text Search, Whoosh, and Elasticsearch.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
from config.mongodb import get_collection

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class MongoDBTextSearch:
    """MongoDB text search implementation (free, uses existing MongoDB)."""
    
    def __init__(self):
        self.collection = get_collection('media_files')
        self.search_collection = get_collection('search_index')
    
    async def index_document(self, doc_id: str, title: str, content: str, metadata: Dict = None):
        """Index a document for search."""
        try:
            if not self.search_collection:
                return False
            
            # Create search document
            search_doc = {
                'file_id': doc_id,
                'title': title,
                'content': content,
                'search_text': f"{title} {content}",
                'metadata': metadata or {},
                'indexed_at': datetime.utcnow()
            }
            
            # Upsert document
            self.search_collection.update_one(
                {'file_id': doc_id},
                {'$set': search_doc},
                upsert=True
            )
            return True
            
        except Exception as e:
            logger.error(f"MongoDB text search indexing error: {e}")
            return False
    
    async def search(self, query: str, limit: int = 50) -> List[Dict]:
        """Search documents using MongoDB text search."""
        try:
            if not self.search_collection:
                return []
            
            # MongoDB text search
            results = list(self.search_collection.find(
                {'$text': {'$search': query}},
                {'score': {'$meta': 'textScore'}}
            ).sort([('score', {'$meta': 'textScore'})]).limit(limit))
            
            return results
            
        except Exception as e:
            logger.error(f"MongoDB text search error: {e}")
            return []
    
    async def delete_document(self, doc_id: str) -> bool:
        """Delete document from search index."""
        try:
            if not self.search_collection:
                return False
            
            result = self.search_collection.delete_one({'file_id': doc_id})
            return result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"MongoDB delete error: {e}")
            return False


class WhooshSearch:
    """Whoosh file-based search implementation (good for free hosting)."""
    
    def __init__(self):
        self.index_path = os.getenv('WHOOSH_INDEX_PATH', './data/search_index')
        self.index = None
        self._init_index()
    
    def _init_index(self):
        """Initialize Whoosh index."""
        try:
            from whoosh.index import create_index, open_dir, exists_in
            from whoosh.fields import Schema, TEXT, ID, DATETIME
            from whoosh.analysis import StemmingAnalyzer
            import os
            
            # Create index directory
            os.makedirs(self.index_path, exist_ok=True)
            
            # Define schema
            schema = Schema(
                file_id=ID(stored=True, unique=True),
                title=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                content=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                metadata=TEXT(stored=True),
                indexed_at=DATETIME(stored=True)
            )
            
            # Create or open index
            if exists_in(self.index_path):
                self.index = open_dir(self.index_path)
            else:
                self.index = create_index(schema, self.index_path)
            
            logger.info("Whoosh search index initialized")
            
        except ImportError:
            logger.warning("Whoosh not installed, search functionality limited")
        except Exception as e:
            logger.error(f"Whoosh initialization error: {e}")
    
    async def index_document(self, doc_id: str, title: str, content: str, metadata: Dict = None):
        """Index a document for search."""
        try:
            if not self.index:
                return False
            
            from whoosh.writing import AsyncWriter
            import json
            
            writer = AsyncWriter(self.index)
            writer.update_document(
                file_id=doc_id,
                title=title,
                content=content,
                metadata=json.dumps(metadata or {}),
                indexed_at=datetime.utcnow()
            )
            writer.commit()
            return True
            
        except Exception as e:
            logger.error(f"Whoosh indexing error: {e}")
            return False
    
    async def search(self, query: str, limit: int = 50) -> List[Dict]:
        """Search documents using Whoosh."""
        try:
            if not self.index:
                return []
            
            from whoosh.qparser import MultifieldParser
            import json
            
            with self.index.searcher() as searcher:
                parser = MultifieldParser(['title', 'content'], self.index.schema)
                parsed_query = parser.parse(query)
                results = searcher.search(parsed_query, limit=limit)
                
                return [
                    {
                        'file_id': hit['file_id'],
                        'title': hit['title'],
                        'content': hit['content'],
                        'metadata': json.loads(hit['metadata']) if hit['metadata'] else {},
                        'score': hit.score
                    }
                    for hit in results
                ]
                
        except Exception as e:
            logger.error(f"Whoosh search error: {e}")
            return []
    
    async def delete_document(self, doc_id: str) -> bool:
        """Delete document from search index."""
        try:
            if not self.index:
                return False
            
            writer = self.index.writer()
            writer.delete_by_term('file_id', doc_id)
            writer.commit()
            return True
            
        except Exception as e:
            logger.error(f"Whoosh delete error: {e}")
            return False


class SearchManager:
    """Unified search manager supporting multiple backends."""
    
    def __init__(self):
        self.search_engine = os.getenv('SEARCH_ENGINE', 'mongodb_text').lower()
        self.backend = None
        self._init_backend()
    
    def _init_backend(self):
        """Initialize the selected search backend."""
        if self.search_engine == 'mongodb_text':
            self.backend = MongoDBTextSearch()
            logger.info("Using MongoDB text search")
        elif self.search_engine == 'whoosh':
            self.backend = WhooshSearch()
            logger.info("Using Whoosh file-based search")
        elif self.search_engine == 'elasticsearch':
            # Only initialize if explicitly enabled
            if os.getenv('ELASTICSEARCH_ENABLED', 'false').lower() == 'true':
                try:
                    from .elasticsearch_search import ElasticsearchSearch
                    self.backend = ElasticsearchSearch()
                    logger.info("Using Elasticsearch")
                except ImportError:
                    logger.warning("Elasticsearch not available, falling back to MongoDB text search")
                    self.backend = MongoDBTextSearch()
            else:
                logger.info("Elasticsearch disabled, using MongoDB text search")
                self.backend = MongoDBTextSearch()
        else:
            logger.warning(f"Unknown search engine: {self.search_engine}, using MongoDB text search")
            self.backend = MongoDBTextSearch()
    
    async def index_media_file(self, file_id: str, file_name: str, file_type: str, 
                              metadata: Dict = None) -> bool:
        """Index a media file for search."""
        try:
            # Create searchable content
            content_parts = [file_name, file_type]
            
            if metadata:
                # Add metadata to searchable content
                if 'description' in metadata:
                    content_parts.append(metadata['description'])
                if 'tags' in metadata:
                    content_parts.extend(metadata.get('tags', []))
                if 'channel_name' in metadata:
                    content_parts.append(metadata['channel_name'])
            
            content = ' '.join(filter(None, content_parts))
            
            return await self.backend.index_document(
                doc_id=file_id,
                title=file_name,
                content=content,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error indexing media file {file_id}: {e}")
            return False
    
    async def search_media(self, query: str, limit: int = 50) -> List[Dict]:
        """Search for media files."""
        try:
            return await self.backend.search(query, limit)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    async def delete_media(self, file_id: str) -> bool:
        """Remove media file from search index."""
        try:
            return await self.backend.delete_document(file_id)
        except Exception as e:
            logger.error(f"Error deleting media {file_id}: {e}")
            return False
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search engine statistics."""
        return {
            'search_engine': self.search_engine,
            'backend_type': type(self.backend).__name__,
            'available': self.backend is not None
        }


# Global search manager instance
search_manager = SearchManager()


# Convenience functions
async def index_media_file(file_id: str, file_name: str, file_type: str, metadata: Dict = None) -> bool:
    """Index a media file for search."""
    return await search_manager.index_media_file(file_id, file_name, file_type, metadata)


async def search_media(query: str, limit: int = 50) -> List[Dict]:
    """Search for media files."""
    return await search_manager.search_media(query, limit)


async def delete_media_from_search(file_id: str) -> bool:
    """Remove media file from search index."""
    return await search_manager.delete_media(file_id)


def get_search_stats() -> Dict[str, Any]:
    """Get search engine statistics."""
    return search_manager.get_search_stats()
