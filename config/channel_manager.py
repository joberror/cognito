"""
Channel management system for the Media Management Bot.
Handles dynamic channel addition/removal through the database.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from config.mongodb import get_collection

logger = logging.getLogger(__name__)


class ChannelManager:
    """Manages monitored channels dynamically through the database."""
    
    def __init__(self):
        self.channels_collection = get_collection('channels')
    
    async def add_channel(self, channel_id: int, channel_username: str = None, 
                         channel_name: str = None, added_by: int = None) -> bool:
        """Add a channel to monitoring."""
        try:
            if not self.channels_collection:
                logger.error("Channels collection not available")
                return False
            
            # Check if channel already exists
            existing = self.channels_collection.find_one({'channel_id': channel_id})
            if existing:
                # Update existing channel to active if it was inactive
                if not existing.get('is_active', True):
                    self.channels_collection.update_one(
                        {'channel_id': channel_id},
                        {
                            '$set': {
                                'is_active': True,
                                'is_monitored': True,
                                'updated_at': datetime.utcnow(),
                                'reactivated_by': added_by,
                                'reactivated_at': datetime.utcnow()
                            }
                        }
                    )
                    logger.info(f"Channel {channel_id} reactivated")
                    return True
                else:
                    logger.info(f"Channel {channel_id} already exists and is active")
                    return True
            
            # Add new channel
            channel_doc = {
                'channel_id': channel_id,
                'channel_username': channel_username,
                'channel_name': channel_name,
                'is_active': True,
                'is_monitored': True,
                'added_by': added_by,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                # Channel-specific settings
                'auto_index': True,
                'allow_duplicates': False,
                'file_types_allowed': ['video', 'audio', 'document', 'photo'],
                'max_file_size': 2147483648,  # 2GB default
            }
            
            result = self.channels_collection.insert_one(channel_doc)
            
            if result.inserted_id:
                logger.info(f"Channel {channel_id} ({channel_username}) added successfully")
                return True
            else:
                logger.error(f"Failed to add channel {channel_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding channel {channel_id}: {e}")
            return False
    
    async def remove_channel(self, channel_id: int, removed_by: int = None) -> bool:
        """Remove a channel from monitoring (soft delete)."""
        try:
            if not self.channels_collection:
                logger.error("Channels collection not available")
                return False
            
            # Soft delete - mark as inactive instead of deleting
            result = self.channels_collection.update_one(
                {'channel_id': channel_id},
                {
                    '$set': {
                        'is_active': False,
                        'is_monitored': False,
                        'removed_by': removed_by,
                        'removed_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"Channel {channel_id} removed from monitoring")
                return True
            else:
                logger.warning(f"Channel {channel_id} not found or already inactive")
                return False
                
        except Exception as e:
            logger.error(f"Error removing channel {channel_id}: {e}")
            return False
    
    async def get_active_channels(self) -> List[Dict[str, Any]]:
        """Get all active monitored channels."""
        try:
            if not self.channels_collection:
                return []
            
            channels = list(self.channels_collection.find({
                'is_active': True,
                'is_monitored': True
            }).sort('created_at', 1))
            
            return channels
            
        except Exception as e:
            logger.error(f"Error getting active channels: {e}")
            return []
    
    async def get_all_channels(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        """Get all channels (active and optionally inactive)."""
        try:
            if not self.channels_collection:
                return []
            
            query = {}
            if not include_inactive:
                query['is_active'] = True
            
            channels = list(self.channels_collection.find(query).sort('created_at', 1))
            return channels
            
        except Exception as e:
            logger.error(f"Error getting channels: {e}")
            return []
    
    async def get_channel_info(self, channel_id: int) -> Optional[Dict[str, Any]]:
        """Get information about a specific channel."""
        try:
            if not self.channels_collection:
                return None
            
            channel = self.channels_collection.find_one({'channel_id': channel_id})
            return channel
            
        except Exception as e:
            logger.error(f"Error getting channel info for {channel_id}: {e}")
            return None
    
    async def update_channel_settings(self, channel_id: int, settings: Dict[str, Any], 
                                    updated_by: int = None) -> bool:
        """Update channel-specific settings."""
        try:
            if not self.channels_collection:
                logger.error("Channels collection not available")
                return False
            
            # Add metadata to settings
            settings.update({
                'updated_at': datetime.utcnow(),
                'updated_by': updated_by
            })
            
            result = self.channels_collection.update_one(
                {'channel_id': channel_id, 'is_active': True},
                {'$set': settings}
            )
            
            if result.modified_count > 0:
                logger.info(f"Channel {channel_id} settings updated")
                return True
            else:
                logger.warning(f"Channel {channel_id} not found or no changes made")
                return False
                
        except Exception as e:
            logger.error(f"Error updating channel {channel_id} settings: {e}")
            return False
    
    async def is_channel_monitored(self, channel_id: int) -> bool:
        """Check if a channel is being monitored."""
        try:
            if not self.channels_collection:
                return False
            
            channel = self.channels_collection.find_one({
                'channel_id': channel_id,
                'is_active': True,
                'is_monitored': True
            })
            
            return channel is not None
            
        except Exception as e:
            logger.error(f"Error checking if channel {channel_id} is monitored: {e}")
            return False
    
    async def get_channel_stats(self) -> Dict[str, int]:
        """Get channel statistics."""
        try:
            if not self.channels_collection:
                return {'total': 0, 'active': 0, 'inactive': 0}
            
            total = self.channels_collection.count_documents({})
            active = self.channels_collection.count_documents({'is_active': True})
            inactive = total - active
            
            return {
                'total': total,
                'active': active,
                'inactive': inactive
            }
            
        except Exception as e:
            logger.error(f"Error getting channel stats: {e}")
            return {'total': 0, 'active': 0, 'inactive': 0}
    
    async def toggle_channel_monitoring(self, channel_id: int, enabled: bool, 
                                      updated_by: int = None) -> bool:
        """Enable or disable monitoring for a channel."""
        try:
            if not self.channels_collection:
                return False
            
            result = self.channels_collection.update_one(
                {'channel_id': channel_id, 'is_active': True},
                {
                    '$set': {
                        'is_monitored': enabled,
                        'updated_at': datetime.utcnow(),
                        'updated_by': updated_by
                    }
                }
            )
            
            if result.modified_count > 0:
                status = "enabled" if enabled else "disabled"
                logger.info(f"Channel {channel_id} monitoring {status}")
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error toggling monitoring for channel {channel_id}: {e}")
            return False


# Global channel manager instance
channel_manager = ChannelManager()


# Convenience functions
async def add_channel(channel_id: int, channel_username: str = None, 
                     channel_name: str = None, added_by: int = None) -> bool:
    """Add a channel to monitoring."""
    return await channel_manager.add_channel(channel_id, channel_username, channel_name, added_by)


async def remove_channel(channel_id: int, removed_by: int = None) -> bool:
    """Remove a channel from monitoring."""
    return await channel_manager.remove_channel(channel_id, removed_by)


async def get_active_channels() -> List[Dict[str, Any]]:
    """Get all active monitored channels."""
    return await channel_manager.get_active_channels()


async def get_all_channels(include_inactive: bool = False) -> List[Dict[str, Any]]:
    """Get all channels."""
    return await channel_manager.get_all_channels(include_inactive)


async def is_channel_monitored(channel_id: int) -> bool:
    """Check if a channel is being monitored."""
    return await channel_manager.is_channel_monitored(channel_id)


async def get_channel_info(channel_id: int) -> Optional[Dict[str, Any]]:
    """Get channel information."""
    return await channel_manager.get_channel_info(channel_id)


async def get_channel_stats() -> Dict[str, int]:
    """Get channel statistics."""
    return await channel_manager.get_channel_stats()
