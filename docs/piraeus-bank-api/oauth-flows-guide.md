# OAuth2 Authentication Flows - Implementation Guide

## Environment Configuration

### Sandbox Environment
- **Base URL**: `https://api.rapidlink.piraeusbank.gr/piraeusbank/production`
- **OAuth Path**: `/v3/oauth`
- **Scopes**: `sandboxapi`, `offline_access`

### Production Environment  
- **Base URL**: `https://openbank.piraeusbank.gr/identityserver/connect`
- **OAuth Path**: N/A (URLs include full path)
- **Scopes**: `winbankAccess`, `winbankAccess.info`, `winbankAccess.monetaryTransactions`, `offline_access`

## OAuth2 Flow Sequence

### Authorization Code Flow (Recommended)
1. **Authorization Request** → GET `/oauth2/authorize`
2. **User Authorization** → User logs in and consents
3. **Authorization Code** → Redirect with code parameter
4. **Token Exchange** → POST `/oauth2/token` with authorization_code grant
5. **API Calls** → Use Bearer token in Authorization header

### Grant Type Selection Guide

- **`authorization_code`**: Web applications with redirect capability
- **`client_credentials`**: Server-to-server communication (no user context)
- **`password`**: Mobile/desktop apps (deprecated, use with caution)
- **`refresh_token`**: Obtain new access token without user interaction

## Strong Customer Authentication (SCA)

### When SCA is Required
- **Pre-PSD2**: Once per session, monetary transactions only
- **Post-PSD2**: Per transaction, both monetary and non-monetary

### SCA Methods by API Version
- **PB APIs v1.1**: CHIP_OTP, SMS_OTP
- **PB APIs v1.2**: CHIP_OTP, SMS_OTP, PUSH_OTP  
- **PSD2 APIs**: All methods including TOUCH_OTP

### SCA Implementation Pattern
1. Make API call
2. If SCA required, API returns appropriate error/message
3. Validate using appropriate SCA method
4. Retry API call with validation

## Common Integration Patterns

### Token Management
```
1. Store access_token securely
2. Check expires_in and refresh before expiry
3. Use refresh_token for automatic renewal
4. Handle token revocation gracefully
```

### Error Handling
- **401 Unauthorized**: Token expired or invalid
- **403 Forbidden**: Insufficient scope or SCA required
- **400 Bad Request**: Invalid parameters or grant

### Security Best Practices
- Never store customer credentials
- Use HTTPS for all requests
- Implement proper token storage
- Handle authorization codes quickly (they expire fast)
- Use state parameter to prevent CSRF attacks