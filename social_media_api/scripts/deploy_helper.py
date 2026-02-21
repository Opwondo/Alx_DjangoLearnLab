import os
import sys
import django

def setup_environment():
    """Setup Django environment"""
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')
    django.setup()

def check_settings():
    """Check if all required settings are configured"""
    from django.conf import settings
    
    checks = []
    
    # Check STATIC_ROOT
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        checks.append(("STATIC_ROOT", settings.STATIC_ROOT, "✅"))
    else:
        checks.append(("STATIC_ROOT", "Not set", "❌"))
    
    # Check MEDIA_ROOT
    if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
        checks.append(("MEDIA_ROOT", settings.MEDIA_ROOT, "✅"))
    else:
        checks.append(("MEDIA_ROOT", "Not set", "⚠️"))
    
    # Check DEBUG
    checks.append(("DEBUG", settings.DEBUG, "⚠️" if settings.DEBUG else "✅"))
    
    # Check ALLOWED_HOSTS
    if settings.ALLOWED_HOSTS:
        checks.append(("ALLOWED_HOSTS", settings.ALLOWED_HOSTS, "✅"))
    else:
        checks.append(("ALLOWED_HOSTS", "Empty", "❌"))
    
    # Print results
    print("\n=== Settings Check ===\n")
    for name, value, status in checks:
        print(f"{status} {name}: {value}")
    
    return all("❌" not in c[2] for c in checks)

def create_env_template():
    """Create .env template file"""
    template = """# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

# Database Settings
DB_NAME=social_media
DB_USER=social_media_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# For Render (DATABASE_URL is auto-generated)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Optional: AWS S3 Settings
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS_STORAGE_BUCKET_NAME=your-bucket-name
# AWS_S3_REGION_NAME=us-east-1
"""
    with open('.env.template', 'w') as f:
        f.write(template)
    print("\n✅ Created .env.template file")

def main():
    print("\n🚀 Deployment Helper Script")
    print("==========================\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check Django
    try:
        import django
        print(f"Django version: {django.get_version()}")
    except ImportError:
        print("❌ Django not installed")
        return
    
    # Setup environment
    setup_environment()
    
    # Check settings
    if check_settings():
        print("\n✅ All settings checks passed!")
    else:
        print("\n❌ Some settings need attention")
    
    # Create .env template
    create_env_template()
    
    print("\n📋 Next steps:")
    print("1. Copy .env.template to .env and fill in values")
    print("2. Run: python manage.py migrate")
    print("3. Run: ./scripts/collectstatic.sh")
    print("4. Test locally: python manage.py runserver")
    print("5. Deploy to Render: git push origin main")

if __name__ == "__main__":
    main()