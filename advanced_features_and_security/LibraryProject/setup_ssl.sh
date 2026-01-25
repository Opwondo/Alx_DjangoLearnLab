#!/bin/bash
# SSL/TLS Certificate Setup Script for Django Application
# This script helps set up SSL certificates for production deployment

set -e

echo "🔐 SSL/TLS Certificate Setup for Django Application"
echo "=================================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Please run as root or with sudo"
    exit 1
fi

# Install Certbot for Let's Encrypt
echo "📦 Installing Certbot..."
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    yum install -y certbot python3-certbot-nginx
elif command -v dnf &> /dev/null; then
    # Fedora
    dnf install -y certbot python3-certbot-nginx
else
    echo "❌ Unsupported package manager. Please install Certbot manually."
    exit 1
fi

echo ""
echo "📝 SSL Certificate Options:"
echo "1. Generate Let's Encrypt certificate with Certbot"
echo "2. Use existing certificate"
echo "3. Generate self-signed certificate (for testing)"
echo ""
read -p "Choose option (1-3): " ssl_option

case $ssl_option in
    1)
        # Let's Encrypt with Certbot
        read -p "Enter your domain name (e.g., yourdomain.com): " domain_name
        read -p "Enter email for SSL certificate notifications: " email
        
        echo "🎫 Obtaining SSL certificate from Let's Encrypt..."
        certbot certonly --standalone --non-interactive --agree-tos \
            --email "$email" -d "$domain_name" -d "www.$domain_name"
        
        echo "✅ Certificate obtained successfully!"
        echo "📍 Certificate location: /etc/letsencrypt/live/$domain_name/"
        ;;
    
    2)
        # Existing certificate
        read -p "Enter path to SSL certificate (.pem or .crt): " cert_path
        read -p "Enter path to private key (.key): " key_path
        
        if [ ! -f "$cert_path" ] || [ ! -f "$key_path" ]; then
            echo "❌ Certificate or key file not found!"
            exit 1
        fi
        
        # Create directory structure
        mkdir -p /etc/ssl/private /etc/ssl/certs
        cp "$cert_path" /etc/ssl/certs/
        cp "$key_path" /etc/ssl/private/
        
        echo "✅ Certificate files copied to /etc/ssl/"
        ;;
    
    3)
        # Self-signed certificate for testing
        read -p "Enter your domain name (e.g., yourdomain.com): " domain_name
        
        echo "🔧 Generating self-signed certificate (for testing only)..."
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout /etc/ssl/private/selfsigned.key \
            -out /etc/ssl/certs/selfsigned.crt \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=$domain_name"
        
        echo "⚠️  WARNING: Self-signed certificates are for testing only!"
        echo "📍 Certificate location: /etc/ssl/certs/selfsigned.crt"
        echo "📍 Key location: /etc/ssl/private/selfsigned.key"
        ;;
    
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "📋 Next Steps:"
echo "1. Update your web server (Nginx/Apache) configuration with certificate paths"
echo "2. Configure Django settings.py with HTTPS settings"
echo "3. Restart your web server"
echo "4. Test SSL configuration at: https://www.ssllabs.com/ssltest/"
echo ""
echo "✅ SSL setup completed!"
