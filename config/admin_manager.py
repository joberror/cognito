"""
Admin management system for the Media Management Bot.
Handles dynamic admin promotion/demotion through the database.
"""

import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from config.mongodb import get_collection

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class AdminManager:
    """Manages admin users dynamically through the database."""
    
    def __init__(self):
        self.users_collection = get_collection('users')
        self.super_admin_id = int(os.getenv('SUPER_ADMIN_ID', 0))
    
    async def is_super_admin(self, user_id: int) -> bool:
        """Check if user is the super admin."""
        return user_id == self.super_admin_id
    
    async def is_admin(self, user_id: int) -> bool:
        """Check if user is an admin (any level)."""
        if user_id == self.super_admin_id:
            return True
        
        if not self.users_collection:
            return False
        
        user = self.users_collection.find_one({'user_id': user_id})
        if user:
            return user.get('is_admin', False) or user.get('admin_level') in ['admin', 'super_admin']
        
        return False
    
    async def get_admin_level(self, user_id: int) -> str:
        """Get user's admin level."""
        if user_id == self.super_admin_id:
            return 'super_admin'
        
        if not self.users_collection:
            return 'user'
        
        user = self.users_collection.find_one({'user_id': user_id})
        if user:
            return user.get('admin_level', 'user')
        
        return 'user'
    
    async def promote_admin(self, user_id: int, promoted_by: int, admin_level: str = 'admin') -> bool:
        """Promote a user to admin."""
        try:
            if not self.users_collection:
                logger.error("Users collection not available")
                return False
            
            # Only super admin can promote others
            if not await self.is_super_admin(promoted_by):
                logger.warning(f"User {promoted_by} attempted to promote {user_id} but is not super admin")
                return False
            
            # Validate admin level
            if admin_level not in ['admin', 'super_admin']:
                admin_level = 'admin'
            
            # Update or create user record
            result = self.users_collection.update_one(
                {'user_id': user_id},
                {
                    '$set': {
                        'is_admin': True,
                        'admin_level': admin_level,
                        'promoted_by': promoted_by,
                        'promoted_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    },
                    '$setOnInsert': {
                        'created_at': datetime.utcnow()
                    }
                },
                upsert=True
            )
            
            logger.info(f"User {user_id} promoted to {admin_level} by {promoted_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error promoting user {user_id}: {e}")
            return False
    
    async def demote_admin(self, user_id: int, demoted_by: int) -> bool:
        """Demote an admin to regular user."""
        try:
            if not self.users_collection:
                logger.error("Users collection not available")
                return False
            
            # Only super admin can demote others
            if not await self.is_super_admin(demoted_by):
                logger.warning(f"User {demoted_by} attempted to demote {user_id} but is not super admin")
                return False
            
            # Cannot demote super admin
            if user_id == self.super_admin_id:
                logger.warning(f"Attempt to demote super admin {user_id}")
                return False
            
            # Update user record
            result = self.users_collection.update_one(
                {'user_id': user_id},
                {
                    '$set': {
                        'is_admin': False,
                        'admin_level': 'user',
                        'updated_at': datetime.utcnow()
                    },
                    '$unset': {
                        'promoted_by': '',
                        'promoted_at': ''
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"User {user_id} demoted by {demoted_by}")
                return True
            else:
                logger.warning(f"User {user_id} not found or already not admin")
                return False
            
        except Exception as e:
            logger.error(f"Error demoting user {user_id}: {e}")
            return False
    
    async def get_all_admins(self) -> List[Dict[str, Any]]:
        """Get all admin users."""
        try:
            if not self.users_collection:
                return []
            
            admins = list(self.users_collection.find({
                '$or': [
                    {'is_admin': True},
                    {'admin_level': {'$in': ['admin', 'super_admin']}}
                ]
            }))
            
            # Add super admin if not in database
            super_admin_in_db = any(admin['user_id'] == self.super_admin_id for admin in admins)
            if not super_admin_in_db and self.super_admin_id:
                admins.append({
                    'user_id': self.super_admin_id,
                    'admin_level': 'super_admin',
                    'is_admin': True,
                    'username': 'Super Admin',
                    'created_at': datetime.utcnow()
                })
            
            return admins
            
        except Exception as e:
            logger.error(f"Error getting admin list: {e}")
            return []
    
    async def initialize_super_admin(self) -> bool:
        """Initialize super admin in database if not exists."""
        try:
            if not self.users_collection or not self.super_admin_id:
                return False
            
            # Check if super admin exists
            existing = self.users_collection.find_one({'user_id': self.super_admin_id})
            
            if not existing:
                # Create super admin record
                self.users_collection.insert_one({
                    'user_id': self.super_admin_id,
                    'is_admin': True,
                    'admin_level': 'super_admin',
                    'username': 'Super Admin',
                    'first_name': 'Super',
                    'last_name': 'Admin',
                    'is_banned': False,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                logger.info(f"Super admin {self.super_admin_id} initialized in database")
            else:
                # Update existing record to ensure super admin status
                self.users_collection.update_one(
                    {'user_id': self.super_admin_id},
                    {
                        '$set': {
                            'is_admin': True,
                            'admin_level': 'super_admin',
                            'updated_at': datetime.utcnow()
                        }
                    }
                )
                logger.info(f"Super admin {self.super_admin_id} status updated")
            
            return True
            
        except Exception as e:
            logger.error(f"Error initializing super admin: {e}")
            return False
    
    async def can_manage_admins(self, user_id: int) -> bool:
        """Check if user can manage other admins (only super admin)."""
        return await self.is_super_admin(user_id)
    
    async def can_use_admin_commands(self, user_id: int) -> bool:
        """Check if user can use admin commands."""
        return await self.is_admin(user_id)


# Global admin manager instance
admin_manager = AdminManager()


# Convenience functions
async def is_admin(user_id: int) -> bool:
    """Check if user is an admin."""
    return await admin_manager.is_admin(user_id)


async def is_super_admin(user_id: int) -> bool:
    """Check if user is the super admin."""
    return await admin_manager.is_super_admin(user_id)


async def promote_admin(user_id: int, promoted_by: int, admin_level: str = 'admin') -> bool:
    """Promote a user to admin."""
    return await admin_manager.promote_admin(user_id, promoted_by, admin_level)


async def demote_admin(user_id: int, demoted_by: int) -> bool:
    """Demote an admin to regular user."""
    return await admin_manager.demote_admin(user_id, demoted_by)


async def get_all_admins() -> List[Dict[str, Any]]:
    """Get all admin users."""
    return await admin_manager.get_all_admins()


async def initialize_super_admin() -> bool:
    """Initialize super admin in database."""
    return await admin_manager.initialize_super_admin()
