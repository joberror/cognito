"""
MongoDB connection and utilities for the Media Management Bot.
"""

import os
import logging
from typing import Optional, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class MongoDBManager:
    """MongoDB connection and database management."""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self._connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/media_bot')
        self._database_name = self._extract_database_name()

    def _extract_database_name(self) -> str:
        """Extract database name from MongoDB URI."""
        try:
            # Extract database name from URI
            if '/' in self._connection_string:
                # Get the part after the last '/' and before any '?'
                db_part = self._connection_string.split('/')[-1]
                db_name = db_part.split('?')[0]
                return db_name if db_name else 'media_bot'
            return 'media_bot'
        except:
            return 'media_bot'
    
    def connect(self) -> bool:
        """Establish connection to MongoDB."""
        try:
            logger.info("Connecting to MongoDB...")
            
            self.client = MongoClient(
                self._connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,  # 10 second connection timeout
                socketTimeoutMS=20000,   # 20 second socket timeout
                maxPoolSize=50,          # Maximum connection pool size
                retryWrites=True         # Enable retryable writes
            )
            
            # Test the connection
            self.client.admin.command('ping')
            
            # Get the database
            self.database = self.client[self._database_name]
            
            logger.info(f"Successfully connected to MongoDB database: {self._database_name}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """Get a MongoDB collection."""
        if self.database is None:
            logger.error("Database not connected")
            return None
        
        return self.database[collection_name]
    
    def create_indexes(self) -> bool:
        """Create database indexes for optimal performance."""
        try:
            if self.database is None:
                logger.error("Database not connected")
                return False
            
            logger.info("Creating MongoDB indexes...")
            
            # Users collection indexes
            users = self.database.users
            users.create_index("user_id", unique=True)
            users.create_index("username")
            users.create_index("is_admin")
            users.create_index("created_at")
            
            # Channels collection indexes
            channels = self.database.channels
            channels.create_index("channel_id", unique=True)
            channels.create_index("channel_username")
            channels.create_index("is_active")
            channels.create_index("is_monitored")
            channels.create_index("added_by")
            channels.create_index([("is_active", 1), ("is_monitored", 1)])
            
            # Media files collection indexes
            media_files = self.database.media_files
            media_files.create_index("file_id", unique=True)
            media_files.create_index("channel_id")
            media_files.create_index("file_type")
            media_files.create_index([("file_name", "text")])
            media_files.create_index("created_at")
            media_files.create_index([("channel_id", 1), ("file_type", 1)])
            media_files.create_index([("channel_id", 1), ("created_at", -1)])
            
            # Search index collection
            search_index = self.database.search_index
            search_index.create_index("file_id")
            search_index.create_index("search_terms")
            search_index.create_index([("full_text", "text")])
            
            # Bot stats collection
            bot_stats = self.database.bot_stats
            bot_stats.create_index("stat_type")
            bot_stats.create_index("timestamp")
            bot_stats.create_index([("stat_type", 1), ("timestamp", -1)])
            
            logger.info("MongoDB indexes created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating MongoDB indexes: {e}")
            return False
    
    def test_connection(self) -> Dict[str, Any]:
        """Test MongoDB connection and return status."""
        result = {
            'connected': False,
            'database_name': self._database_name,
            'collections': [],
            'error': None
        }
        
        try:
            if not self.client:
                if not self.connect():
                    result['error'] = 'Failed to establish connection'
                    return result
            
            # Test ping
            self.client.admin.command('ping')
            result['connected'] = True
            
            # Get collections
            if self.database is not None:
                result['collections'] = self.database.list_collection_names()
            
            # Get server info
            server_info = self.client.server_info()
            result['server_version'] = server_info.get('version', 'Unknown')
            
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"MongoDB connection test failed: {e}")
        
        return result
    
    def initialize_database(self) -> bool:
        """Initialize database with required collections and indexes."""
        try:
            if self.database is None:
                if not self.connect():
                    return False
            
            logger.info("Initializing MongoDB database...")
            
            # Create collections if they don't exist
            collections = ['users', 'channels', 'media_files', 'search_index', 'bot_stats']
            existing_collections = self.database.list_collection_names()
            
            for collection_name in collections:
                if collection_name not in existing_collections:
                    self.database.create_collection(collection_name)
                    logger.info(f"Created collection: {collection_name}")
            
            # Create indexes
            if not self.create_indexes():
                return False
            
            logger.info("MongoDB database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing MongoDB database: {e}")
            return False


# Global MongoDB manager instance
mongodb_manager = MongoDBManager()


def get_mongodb_connection() -> Optional[Database]:
    """Get MongoDB database connection."""
    if not mongodb_manager.database:
        if mongodb_manager.connect():
            return mongodb_manager.database
        return None
    return mongodb_manager.database


def get_collection(collection_name: str) -> Optional[Collection]:
    """Get a specific MongoDB collection."""
    return mongodb_manager.get_collection(collection_name)


def test_mongodb_connection() -> Dict[str, Any]:
    """Test MongoDB connection and return status."""
    return mongodb_manager.test_connection()


def initialize_mongodb() -> bool:
    """Initialize MongoDB database."""
    return mongodb_manager.initialize_database()
