#!/usr/bin/env python3
"""
HTTPS Configuration Test Script
Tests the Django security settings and HTTPS configuration
"""

import os
import sys
import django
import requests
from django.test import TestCase
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def test_security_settings():
    """Test that all security settings are properly configured."""
    
    print("🔐 Testing Django Security Settings")
    print("=" * 50)
    
    # List of security settings to check
    security_settings = {
        'DEBUG': (False, 'Debug mode should be False in production'),
        'SECURE_SSL_REDIRECT': (True, 'Should redirect HTTP to HTTPS'),
        'SECURE_HSTS_SECONDS': (31536000, 'HSTS should be set to 1 year'),
        'SESSION_COOKIE_SECURE': (True, 'Session cookies should be secure'),
        'CSRF_COOKIE_SECURE': (True, 'CSRF cookies should be secure'),
        'X_FRAME_OPTIONS': ('DENY', 'Should deny framing'),
        'SECURE_CONTENT_TYPE_NOSNIFF': (True, 'Should prevent MIME sniffing'),
        'SECURE_BROWSER_XSS_FILTER': (True, 'Should enable XSS filter'),
    }
    
    all_passed = True
    
    for setting, (expected_value, description) in security_settings.items():
        actual_value = getattr(settings, setting, None)
        if actual_value == expected_value:
            print(f"✅ {setting}: {actual_value} - {description}")
        else:
            print(f"❌ {setting}: Expected {expected_value}, got {actual_value}")
            print(f"   {description}")
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All security settings are correctly configured!")
    else:
        print("⚠️  Some security settings need adjustment")
    
    return all_passed

def check_development_overrides():
    """Check if development overrides are in place."""
    print("\n🛠️  Checking Development Mode")
    print("=" * 50)
    
    # These settings should be False in development overrides
    dev_settings = ['SECURE_SSL_REDIRECT', 'SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE']
    
    for setting in dev_settings:
        value = getattr(settings, setting, None)
        if settings.DEBUG and value:
            print(f"⚠️  {setting} is True but DEBUG is True")
            print("   Development mode should disable secure settings")
        elif not settings.DEBUG and not value:
            print(f"⚠️  {setting} is False but DEBUG is False")
            print("   Production mode should have secure settings enabled")
        else:
            print(f"✅ {setting}: {value} (DEBUG={settings.DEBUG})")

if __name__ == '__main__':
    print("Django HTTPS Security Test")
    print("=" * 50)
    
    test_security_settings()
    check_development_overrides()
    
    print("\n📋 Summary:")
    print("- Run 'python manage.py check --deploy' for Django deployment checks")
    print("- Test manually with: curl -I http://localhost:8000")
    print("- Use SSL Labs test for production: https://www.ssllabs.com/ssltest/")
