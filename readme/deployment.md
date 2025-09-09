# Deployment Guide

This guide covers different deployment options for the Media Management Bot.

## Quick Start

### Option 1: Automated Setup
```bash
# Clone and setup
git clone <repository-url>
cd cognito
make quickstart
```

### Option 2: Manual Setup
```bash
# 1. Setup environment
python scripts/setup.py

# 2. Install dependencies
pip install -r requirements.txt

# 3. Validate configuration
python scripts/validate_config.py

# 4. Run the bot
python bot.py
```

## Local Development

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup Steps
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cognito
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Validate and run**
   ```bash
   python scripts/validate_config.py
   python bot.py
   ```

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Quick Docker Setup
```bash
# 1. Setup environment for Docker
cp .env.example .env.docker
# Edit .env.docker with your configuration

# 2. Start all services
docker-compose up -d

# 3. View logs
docker-compose logs -f bot
```

### Docker Services
The docker-compose.yml includes:
- **bot**: Main bot application
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **elasticsearch**: Search engine
- **prometheus**: Metrics collection (optional)
- **grafana**: Monitoring dashboard (optional)

### Docker Commands
```bash
# Build images
make docker-build

# Start services
make docker-up

# Stop services
make docker-down

# View logs
make docker-logs

# Shell access
make docker-shell
```

## Production Deployment

### Server Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB recommended)
- **Storage**: 50GB+ (depends on media files)
- **OS**: Ubuntu 20.04+ or similar

### Production Setup

1. **Server Preparation**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Deploy Application**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd cognito
   
   # Setup production environment
   cp .env.example .env.docker
   # Configure .env.docker for production
   
   # Deploy
   make prod-deploy
   ```

3. **Configure Reverse Proxy (Optional)**
   ```nginx
   # /etc/nginx/sites-available/media-bot
   server {
       listen 80;
       server_name your-domain.com;
       
       location /webhook {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /metrics {
           proxy_pass http://localhost:8000;
           # Add authentication if needed
       }
   }
   ```

## Cloud Deployment

### AWS Deployment

1. **EC2 Instance**
   - Launch Ubuntu 20.04 instance
   - Configure security groups (ports 22, 80, 443)
   - Follow production setup steps

2. **RDS Database** (Optional)
   ```env
   DATABASE_TYPE=postgresql
   POSTGRES_HOST=your-rds-endpoint
   POSTGRES_DB=media_bot
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   ```

3. **ElastiCache Redis** (Optional)
   ```env
   REDIS_HOST=your-elasticache-endpoint
   REDIS_PORT=6379
   ```

### DigitalOcean Deployment

1. **Droplet Setup**
   ```bash
   # Create droplet with Docker pre-installed
   # Follow production setup steps
   ```

2. **Managed Database** (Optional)
   ```env
   DATABASE_TYPE=postgresql
   DATABASE_URL=your-managed-database-url
   ```

### Heroku Deployment

1. **Prepare for Heroku**
   ```bash
   # Create Procfile
   echo "web: python bot.py" > Procfile
   
   # Create runtime.txt
   echo "python-3.10.0" > runtime.txt
   ```

2. **Deploy**
   ```bash
   heroku create your-app-name
   heroku config:set BOT_TOKEN=your_token
   heroku config:set DATABASE_URL=your_database_url
   git push heroku main
   ```

## Coolify Deployment

Coolify is mentioned in the project scope for easier deployment.

1. **Setup Coolify**
   - Install Coolify on your server
   - Connect your Git repository

2. **Configure Environment**
   - Set environment variables in Coolify dashboard
   - Configure build and deployment settings

3. **Deploy**
   - Coolify will handle the deployment automatically

## Monitoring Setup

### Enable Monitoring Stack
```bash
# Start with monitoring
docker-compose --profile monitoring up -d

# Access dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

### Configure Alerts
1. **Prometheus Alerts**
   - Configure alerting rules
   - Set up notification channels

2. **Grafana Dashboards**
   - Import bot-specific dashboards
   - Configure data sources

## Backup Strategy

### Automated Backups
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups
docker-compose exec -T postgres pg_dump -U postgres media_bot > backups/db_$DATE.sql
tar -czf backups/media_$DATE.tar.gz data/media/
EOF

chmod +x backup.sh

# Add to crontab
echo "0 2 * * * /path/to/backup.sh" | crontab -
```

### Restore from Backup
```bash
# Restore database
docker-compose exec -T postgres psql -U postgres media_bot < backups/db_backup.sql

# Restore media files
tar -xzf backups/media_backup.tar.gz
```

## SSL/TLS Configuration

### Let's Encrypt with Nginx
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Performance Optimization

### Database Optimization
- Use connection pooling
- Configure appropriate indexes
- Regular maintenance tasks

### Redis Configuration
- Configure memory limits
- Set appropriate eviction policies
- Monitor memory usage

### Bot Optimization
- Enable rate limiting
- Configure appropriate timeouts
- Monitor resource usage

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check bot token
   - Verify network connectivity
   - Check logs for errors

2. **Database connection failed**
   - Verify database credentials
   - Check database server status
   - Review connection string

3. **Out of memory**
   - Increase server memory
   - Optimize media processing
   - Configure swap space

### Log Analysis
```bash
# View bot logs
make logs

# Docker logs
docker-compose logs -f bot

# System logs
sudo journalctl -u docker
```

## Security Considerations

1. **Environment Variables**
   - Never commit sensitive data
   - Use secure password generation
   - Rotate credentials regularly

2. **Network Security**
   - Configure firewall rules
   - Use VPN for database access
   - Enable fail2ban

3. **Application Security**
   - Keep dependencies updated
   - Enable rate limiting
   - Monitor for suspicious activity

## Scaling

### Horizontal Scaling
- Use load balancer
- Deploy multiple bot instances
- Shared database and cache

### Vertical Scaling
- Increase server resources
- Optimize database performance
- Use SSD storage

## Maintenance

### Regular Tasks
- Update dependencies
- Monitor disk space
- Review logs
- Backup verification
- Security updates

### Health Checks
```bash
# Automated health check
make health

# Manual verification
python scripts/validate_config.py
```
