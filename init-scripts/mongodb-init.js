// MongoDB initialization script for Media Management Bot
// This script sets up the initial database structure and indexes

// Switch to the media_bot database
use("media_bot");

// Create collections with validation schemas
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "created_at"],
      properties: {
        user_id: {
          bsonType: "long",
          description: "Telegram user ID - required",
        },
        username: {
          bsonType: "string",
          description: "Telegram username",
        },
        first_name: {
          bsonType: "string",
          description: "User first name",
        },
        last_name: {
          bsonType: "string",
          description: "User last name",
        },
        is_admin: {
          bsonType: "bool",
          description: "Admin status - managed through bot commands",
        },
        admin_level: {
          bsonType: "string",
          enum: ["super_admin", "admin", "user"],
          description:
            "Admin level: super_admin (can manage admins), admin (can manage bot), user (regular user)",
        },
        is_banned: {
          bsonType: "bool",
          description: "Ban status",
        },
        promoted_by: {
          bsonType: "long",
          description: "User ID who promoted this user to admin",
        },
        promoted_at: {
          bsonType: "date",
          description: "When user was promoted to admin",
        },
        created_at: {
          bsonType: "date",
          description: "Creation timestamp - required",
        },
        updated_at: {
          bsonType: "date",
          description: "Last update timestamp",
        },
      },
    },
  },
});

db.createCollection("channels", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["channel_id", "created_at"],
      properties: {
        channel_id: {
          bsonType: "long",
          description: "Telegram channel ID - required",
        },
        channel_name: {
          bsonType: "string",
          description: "Channel name",
        },
        channel_username: {
          bsonType: "string",
          description: "Channel username",
        },
        is_active: {
          bsonType: "bool",
          description: "Active status",
        },
        is_monitored: {
          bsonType: "bool",
          description: "Monitoring status",
        },
        created_at: {
          bsonType: "date",
          description: "Creation timestamp - required",
        },
        updated_at: {
          bsonType: "date",
          description: "Last update timestamp",
        },
      },
    },
  },
});

db.createCollection("media_files", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: [
        "file_id",
        "file_name",
        "file_type",
        "channel_id",
        "created_at",
      ],
      properties: {
        file_id: {
          bsonType: "string",
          description: "Telegram file ID - required",
        },
        file_name: {
          bsonType: "string",
          description: "File name - required",
        },
        file_type: {
          bsonType: "string",
          description: "File type/extension - required",
        },
        file_size: {
          bsonType: "long",
          description: "File size in bytes",
        },
        mime_type: {
          bsonType: "string",
          description: "MIME type",
        },
        channel_id: {
          bsonType: "long",
          description: "Channel ID - required",
        },
        message_id: {
          bsonType: "long",
          description: "Message ID",
        },
        file_path: {
          bsonType: "string",
          description: "Local file path",
        },
        thumbnail_path: {
          bsonType: "string",
          description: "Thumbnail path",
        },
        metadata: {
          bsonType: "object",
          description: "File metadata",
        },
        indexed_at: {
          bsonType: "date",
          description: "Indexing timestamp",
        },
        created_at: {
          bsonType: "date",
          description: "Creation timestamp - required",
        },
      },
    },
  },
});

db.createCollection("search_index", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["file_id", "search_terms", "created_at"],
      properties: {
        file_id: {
          bsonType: "string",
          description: "Reference to media file - required",
        },
        search_terms: {
          bsonType: "array",
          description: "Searchable terms - required",
          items: {
            bsonType: "string",
          },
        },
        full_text: {
          bsonType: "string",
          description: "Full text for search",
        },
        created_at: {
          bsonType: "date",
          description: "Creation timestamp - required",
        },
      },
    },
  },
});

db.createCollection("bot_stats", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["stat_type", "value", "timestamp"],
      properties: {
        stat_type: {
          bsonType: "string",
          description: "Type of statistic - required",
        },
        value: {
          bsonType: "number",
          description: "Statistic value - required",
        },
        metadata: {
          bsonType: "object",
          description: "Additional metadata",
        },
        timestamp: {
          bsonType: "date",
          description: "Timestamp - required",
        },
      },
    },
  },
});

// Create indexes for better performance
print("Creating indexes...");

// Users collection indexes
db.users.createIndex({ user_id: 1 }, { unique: true });
db.users.createIndex({ username: 1 });
db.users.createIndex({ is_admin: 1 });
db.users.createIndex({ admin_level: 1 });
db.users.createIndex({ is_banned: 1 });
db.users.createIndex({ promoted_by: 1 });
db.users.createIndex({ created_at: 1 });

// Channels collection indexes
db.channels.createIndex({ channel_id: 1 }, { unique: true });
db.channels.createIndex({ channel_username: 1 });
db.channels.createIndex({ is_active: 1 });
db.channels.createIndex({ is_monitored: 1 });

// Media files collection indexes
db.media_files.createIndex({ file_id: 1 }, { unique: true });
db.media_files.createIndex({ channel_id: 1 });
db.media_files.createIndex({ file_type: 1 });
db.media_files.createIndex({ file_name: "text" });
db.media_files.createIndex({ created_at: 1 });
db.media_files.createIndex({ file_size: 1 });
db.media_files.createIndex({ mime_type: 1 });

// Compound indexes for common queries
db.media_files.createIndex({ channel_id: 1, file_type: 1 });
db.media_files.createIndex({ channel_id: 1, created_at: -1 });

// Search index collection indexes
db.search_index.createIndex({ file_id: 1 });
db.search_index.createIndex({ search_terms: 1 });
db.search_index.createIndex({ full_text: "text" });

// Bot stats collection indexes
db.bot_stats.createIndex({ stat_type: 1 });
db.bot_stats.createIndex({ timestamp: 1 });
db.bot_stats.createIndex({ stat_type: 1, timestamp: -1 });

print("Database initialization completed successfully!");
print(
  "Collections created: users, channels, media_files, search_index, bot_stats"
);
print("Indexes created for optimal performance");
