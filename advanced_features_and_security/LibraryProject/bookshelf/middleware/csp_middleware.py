"""
Custom Content Security Policy Middleware
Protects against XSS attacks by restricting resources the browser can load.
"""
from django.utils.deprecation import MiddlewareMixin

class CSPMiddleware(MiddlewareMixin):
    """
    Simple Content Security Policy implementation.
    In production, consider using django-csp package for more features.
    """
    
    def process_response(self, request, response):
        # Only add CSP headers to HTML responses
        if response.get('Content-Type', '').startswith('text/html'):
            # Basic CSP policy - adjust based on your needs
            csp_policy = (
                "default-src 'self'; "  # Default: only from same origin
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "  # Allow inline scripts (adjust for production)
                "style-src 'self' 'unsafe-inline'; "  # Allow inline styles
                "img-src 'self' data:; "  # Allow images from self and data URIs
                "font-src 'self'; "  # Fonts from self
                "connect-src 'self'; "  # XMLHttpRequest, WebSockets
                "frame-ancestors 'none'; "  # Prevent clickjacking
                "form-action 'self'; "  # Form submissions to self only
                "base-uri 'self'; "  # Base tag URLs
            )
            
            response['Content-Security-Policy'] = csp_policy
            
            # Add other security headers
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
