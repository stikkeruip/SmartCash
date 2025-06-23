#!/usr/bin/env python3
"""
Django management command to test Piraeus Bank OAuth flow.

Usage: python manage.py test_piraeus_oauth

This command:
1. Opens browser to Piraeus OAuth URL
2. Waits for user login (usera/123)
3. Receives callback via local server
4. Exchanges authorization code for access token
5. Prints token information to console
"""

import os
import time
import threading
import webbrowser
import urllib.parse
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

import requests
from django.core.management.base import BaseCommand
from django.conf import settings


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    """HTTP handler for OAuth callback"""
    
    def do_GET(self):
        """Handle GET request from OAuth callback"""
        try:
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)
            
            if 'code' in params:
                # Success! Got authorization code
                self.server.auth_code = params['code'][0]
                self.server.state = params.get('state', [''])[0]
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                success_html = """
                <html>
                <head><title>OAuth Success</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: green;">✅ OAuth Success!</h1>
                    <p>Authorization received. You can close this tab.</p>
                    <p>Check your console for token information.</p>
                </body>
                </html>
                """
                self.wfile.write(success_html.encode())
                
            elif 'error' in params:
                # OAuth error
                error = params['error'][0]
                error_description = params.get('error_description', [''])[0]
                self.server.oauth_error = f"{error}: {error_description}"
                
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                error_html = f"""
                <html>
                <head><title>OAuth Error</title></head>
                <body style="font-family: Arial; text-align: center; padding: 50px;">
                    <h1 style="color: red;">❌ OAuth Error</h1>
                    <p>Error: {error}</p>
                    <p>Description: {error_description}</p>
                    <p>Check your console for details.</p>
                </body>
                </html>
                """
                self.wfile.write(error_html.encode())
            else:
                # Unknown callback
                self.send_response(400)
                self.end_headers()
                
        except Exception as e:
            print(f"❌ Error handling callback: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress default HTTP server logging"""
        pass


class Command(BaseCommand):
    help = 'Test Piraeus Bank OAuth flow - opens browser and exchanges code for token'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback_port = 8000
        self.redirect_uri = f"http://localhost:{self.callback_port}/callback"
        self.server = None
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Port for local callback server (default: 8000)'
        )
        parser.add_argument(
            '--timeout',
            type=int,
            default=300,
            help='Timeout in seconds to wait for callback (default: 300)'
        )
        parser.add_argument(
            '--no-browser',
            action='store_true',
            help='Don\'t automatically open browser - just print URL'
        )
        parser.add_argument(
            '--test-api',
            action='store_true',
            help='Test API calls after getting token (create consent and get accounts)'
        )
    
    def handle(self, *args, **options):
        """Main command handler"""
        self.callback_port = options['port']
        self.redirect_uri = f"http://localhost:{self.callback_port}/callback"
        timeout = options['timeout']
        no_browser = options['no_browser']
        test_api = options['test_api']
        
        self.stdout.write("🚀 Starting Piraeus Bank OAuth Test")
        self.stdout.write(f"📍 Callback URL: {self.redirect_uri}")
        
        try:
            # Step 1: Start local server
            self.start_local_server()
            
            # Step 2: Build and open OAuth URL
            self.initiate_oauth_flow(no_browser)
            
            # Step 3: Wait for callback
            auth_code = self.wait_for_callback(timeout)
            
            if auth_code:
                # Step 4: Exchange code for token
                token_info = self.exchange_code_for_token(auth_code)
                
                # Step 5: Test API calls if requested
                if token_info and test_api:
                    access_token = token_info.get('access_token')
                    if access_token:
                        self.test_api_calls(access_token)
            else:
                self.stdout.write(self.style.ERROR("❌ No authorization code received"))
            
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("\\n⏹️  Test interrupted by user"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
        finally:
            self.cleanup()
    
    def start_local_server(self):
        """Start local HTTP server for OAuth callback"""
        try:
            self.server = socketserver.TCPServer(("", self.callback_port), CallbackHandler)
            self.server.auth_code = None
            self.server.oauth_error = None
            self.server.state = None
            
            # Run server in background thread
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            self.stdout.write(f"🌐 Local server started on port {self.callback_port}")
            
        except OSError as e:
            if "Address already in use" in str(e):
                raise Exception(f"Port {self.callback_port} is already in use. Try --port <other_port>")
            raise
    
    def initiate_oauth_flow(self, no_browser=False):
        """Build OAuth URL and open browser"""
        # Generate state for CSRF protection
        import secrets
        state = secrets.token_urlsafe(16)
        
        # Get credentials from Django settings
        client_id = getattr(settings, 'PIRAEUS_CLIENT_ID', None)
        if not client_id:
            raise Exception("PIRAEUS_CLIENT_ID not found in settings. Check your .env file.")
        
        # Build OAuth authorization URL
        base_url = "https://api.rapidlink.piraeusbank.gr/piraeusbank/production/v3/oauth/oauth2/authorize"
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'scope': 'sandboxapi offline_access',
            'redirect_uri': self.redirect_uri,
            'state': state
        }
        
        # Build URL manually to avoid over-encoding issues
        oauth_url = f"{base_url}?response_type=code&client_id={client_id}&scope=sandboxapi offline_access&redirect_uri={self.redirect_uri}&state={state}"
        
        self.stdout.write(f"🔗 OAuth URL: {oauth_url}")
        self.stdout.write("📝 Login with: usera / 123")
        
        if no_browser:
            self.stdout.write("🖱️  Please copy the URL above and open it in your browser manually")
        else:
            self.stdout.write("🌍 Opening browser for authentication...")
            # Open browser
            webbrowser.open(oauth_url)
        
        # Store state for validation
        self.expected_state = state
    
    def wait_for_callback(self, timeout):
        """Wait for OAuth callback with timeout"""
        self.stdout.write(f"⏳ Waiting for callback (timeout: {timeout}s)...")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.server.auth_code:
                self.stdout.write("✅ Authorization code received!")
                
                # Validate state if provided
                if hasattr(self, 'expected_state') and self.server.state:
                    if self.server.state != self.expected_state:
                        self.stdout.write(self.style.ERROR("❌ State mismatch - possible CSRF attack"))
                        return None
                    self.stdout.write("✅ State validated")
                
                return self.server.auth_code
            
            elif self.server.oauth_error:
                self.stdout.write(self.style.ERROR(f"❌ OAuth error: {self.server.oauth_error}"))
                return None
            
            time.sleep(1)
        
        self.stdout.write(self.style.ERROR("❌ Timeout waiting for callback"))
        return None
    
    def exchange_code_for_token(self, auth_code):
        """Exchange authorization code for access token"""
        self.stdout.write("🔄 Exchanging authorization code for access token...")
        
        # Get credentials from settings
        client_id = settings.PIRAEUS_CLIENT_ID
        client_secret = getattr(settings, 'PIRAEUS_CLIENT_SECRET', None)
        
        if not client_secret:
            raise Exception("PIRAEUS_CLIENT_SECRET not found in settings. Check your .env file.")
        
        # Token exchange endpoint
        token_url = "https://api.rapidlink.piraeusbank.gr/piraeusbank/production/v3/oauth/oauth2/token"
        
        # Prepare token request
        token_data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': self.redirect_uri
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try:
            # Make token request
            response = requests.post(token_url, data=token_data, headers=headers, timeout=30)
            
            self.stdout.write(f"📡 Token request status: {response.status_code}")
            
            if response.status_code == 200:
                token_info = response.json()
                self.display_token_info(token_info)
                return token_info
            else:
                self.stdout.write(self.style.ERROR(f"❌ Token exchange failed: {response.status_code}"))
                self.stdout.write(self.style.ERROR(f"Response: {response.text}"))
                return None
                
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"❌ Network error during token exchange: {e}"))
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error during token exchange: {e}"))
            return None
    
    def display_token_info(self, token_info):
        """Display token information in a readable format"""
        self.stdout.write(self.style.SUCCESS("\\n🎉 OAuth Token Exchange Successful!"))
        self.stdout.write("=" * 60)
        
        # Access token (truncated for display)
        access_token = token_info.get('access_token', 'N/A')
        if len(access_token) > 50:
            display_token = f"{access_token[:25]}...{access_token[-25:]}"
        else:
            display_token = access_token
        
        self.stdout.write(f"🔑 Access Token: {display_token}")
        self.stdout.write(f"🏷️  Token Type: {token_info.get('token_type', 'N/A')}")
        self.stdout.write(f"⏰ Expires In: {token_info.get('expires_in', 'N/A')} seconds")
        
        # Refresh token (if available)
        refresh_token = token_info.get('refresh_token')
        if refresh_token:
            if len(refresh_token) > 50:
                display_refresh = f"{refresh_token[:25]}...{refresh_token[-25:]}"
            else:
                display_refresh = refresh_token
            self.stdout.write(f"🔄 Refresh Token: {display_refresh}")
        
        # Additional info
        scope = token_info.get('scope')
        if scope:
            self.stdout.write(f"🎯 Scope: {scope}")
        
        self.stdout.write("=" * 60)
        
        # Full token for debugging (be careful with this in production!)
        self.stdout.write("\\n🔍 Full Token Response (for debugging):")
        self.stdout.write("-" * 40)
        for key, value in token_info.items():
            self.stdout.write(f"{key}: {value}")
        
        self.stdout.write("\\n✅ Test completed successfully!")
    
    def cleanup(self):
        """Clean up resources"""
        if self.server:
            self.stdout.write("🛑 Stopping local server...")
            self.server.shutdown()
            self.server.server_close()
    
    def test_api_calls(self, access_token):
        """Test API calls with the access token"""
        self.stdout.write("\\n🧪 Testing API Calls with Access Token")
        self.stdout.write("=" * 60)
        
        # Step 1: Create consent
        consent_id = self.create_consent(access_token)
        
        if consent_id:
            # Step 2: Get accounts (only works after consent)
            self.get_accounts(access_token, consent_id)
        
        self.stdout.write("=" * 60)
        self.stdout.write("✅ API testing completed!")
    
    def create_consent(self, access_token):
        """Create PSD2 consent for account access"""
        self.stdout.write("\\n📝 Creating PSD2 Consent...")
        
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        
        # Get client ID from settings
        client_id = settings.PIRAEUS_CLIENT_ID
        
        # Prepare headers
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Request-ID': request_id,
            'x-ibm-client-id': client_id,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Prepare consent data
        from datetime import datetime, timedelta
        valid_until = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        
        consent_data = {
            "access": {
                "accounts": [],
                "balances": [],
                "allPsd2": "allAccounts"
            },
            "recurringIndicator": True,
            "validUntil": valid_until,
            "frequencyPerDay": 255,
            "combinedServiceIndicator": False
        }
        
        consent_url = "https://api.rapidlink.piraeusbank.gr/piraeusbank/production/psd2/v3.1/consents"
        
        try:
            response = requests.post(
                consent_url,
                headers=headers,
                json=consent_data,
                cert=('certificate.crt', 'private.key'),
                timeout=30
            )
            
            self.stdout.write(f"📡 Consent creation status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                consent_response = response.json()
                consent_id = consent_response.get('consentId')
                consent_status = consent_response.get('consentStatus')
                
                self.stdout.write(self.style.SUCCESS(f"✅ Consent created successfully!"))
                self.stdout.write(f"🆔 Consent ID: {consent_id}")
                self.stdout.write(f"📊 Status: {consent_status}")
                
                # Display full response for debugging
                self.stdout.write("\\nConsent Response:")
                for key, value in consent_response.items():
                    self.stdout.write(f"  {key}: {value}")
                
                return consent_id
            else:
                self.stdout.write(self.style.ERROR(f"❌ Consent creation failed: {response.status_code}"))
                self.stdout.write(self.style.ERROR(f"Response: {response.text}"))
                return None
                
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f"❌ Certificate files not found: {e}"))
            self.stdout.write(self.style.ERROR("Make sure certificate.crt and private.key exist in the project directory"))
            return None
        except requests.exceptions.SSLError as e:
            self.stdout.write(self.style.ERROR(f"❌ SSL/Certificate error: {e}"))
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error creating consent: {e}"))
            return None
    
    def get_accounts(self, access_token, consent_id=None):
        """Get user accounts after consent is created"""
        self.stdout.write("\\n🏦 Getting User Accounts...")
        
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        
        # Get client ID from settings
        client_id = settings.PIRAEUS_CLIENT_ID
        
        # Prepare headers
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Request-ID': request_id,
            'x-ibm-client-id': client_id,
            'Accept': 'application/json'
        }
        
        # Add Consent-ID header if provided
        if consent_id:
            headers['Consent-ID'] = consent_id
        
        accounts_url = "https://api.rapidlink.piraeusbank.gr/piraeusbank/production/psd2/v3.1/accounts"
        
        try:
            response = requests.get(
                accounts_url,
                headers=headers,
                cert=('certificate.crt', 'private.key'),
                timeout=30
            )
            
            self.stdout.write(f"📡 Accounts request status: {response.status_code}")
            
            if response.status_code == 200:
                accounts_data = response.json()
                accounts = accounts_data.get('accounts', [])
                
                self.stdout.write(self.style.SUCCESS(f"✅ Retrieved {len(accounts)} account(s)!"))
                
                # Display account information
                for idx, account in enumerate(accounts):
                    self.stdout.write(f"\\n💳 Account {idx + 1}:")
                    self.stdout.write(f"  IBAN: {account.get('iban', 'N/A')}")
                    self.stdout.write(f"  Currency: {account.get('currency', 'N/A')}")
                    self.stdout.write(f"  Product: {account.get('product', 'N/A')}")
                    self.stdout.write(f"  Type: {account.get('cashAccountType', 'N/A')}")
                    self.stdout.write(f"  Name: {account.get('name', 'N/A')}")
                    self.stdout.write(f"  Resource ID: {account.get('resourceId', 'N/A')}")
                
                # Display full response for debugging
                self.stdout.write("\\nFull Accounts Response:")
                self.stdout.write(json.dumps(accounts_data, indent=2))
                
            else:
                self.stdout.write(self.style.ERROR(f"❌ Failed to get accounts: {response.status_code}"))
                self.stdout.write(self.style.ERROR(f"Response: {response.text}"))
                
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f"❌ Certificate files not found: {e}"))
            self.stdout.write(self.style.ERROR("Make sure certificate.crt and private.key exist in the project directory"))
        except requests.exceptions.SSLError as e:
            self.stdout.write(self.style.ERROR(f"❌ SSL/Certificate error: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error getting accounts: {e}"))