# Piraeus Bank API Sandbox Reference

This document provides comprehensive information about the Sandbox environment for testing Piraeus Bank PSD2 APIs without accessing real customer data.

## Overview

The Sandbox Environment simulates the bank's actual backend systems using dummy data for testing purposes. It provides a safe environment for third-party developers to test their applications before moving to production.

## Sandbox Environment Features

### Data Isolation
- **Client-Specific Data**: Each application with a unique `clientId` receives its own isolated dataset
- **Template Replication**: A basic data template is replicated for each new client application
- **Independent Testing**: Multiple developers can test simultaneously without data conflicts

### Session Management
- **Token Expiration**: OAuth tokens expire after 60 minutes
- **Refresh Tokens**: Use refresh tokens to extend sessions without re-authentication
- **Automatic Cleanup**: Sandbox data resets periodically to maintain clean testing environment

## API Endpoints

### Base Configuration
```
Base Path: https://api.rapidlink.piraeusbank.gr/piraeusbank/production
```

### PSD2 API Paths
| Service | Path | Documentation |
|---------|------|---------------|
| **AIS v3.1** | `/psd2/ais/v3.1/*` | [AIS Product Specification](https://developer.piraeusbank.gr) |
| **PIS v3.1** | `/psd2/pis/v3.1/*` | [PIS Product Specification](https://developer.piraeusbank.gr) |

### OAuth2 Endpoints
| Endpoint | Path |
|----------|------|
| **Authorization** | `/v3.1/oauth/oauth2/authorize` |
| **Token** | `/v3.1/oauth/oauth2/token` |

## Test Users

### Login Credentials
| User | Username | Password | Description |
|------|----------|----------|-------------|
| **UserA** | `usera` | `123` | User with 2 accounts, no cards |
| **UserB** | `userb` | `123` | User with 2 accounts, 1 credit card |
| **UserC** | `userc` | `123` | User with 2 accounts, no cards |

**Note**: Usernames are case-insensitive in sandbox environment.

### Account Holdings

#### UserA
**Accounts:**
- `GR2801718220007022123123123` (Primary account)
- `GR9001718220007025111222333` (Secondary account)

**Credit Cards:** None

#### UserB  
**Accounts:**
- `GR0101718220007027000224226` (Primary account)
- `GR0101718220007052999999000` (Secondary account)

**Credit Cards:**
- `430589******6006` (Panathinaikos FC Visa Classic)

#### UserC
**Accounts:**
- `GR0101718220007027000112113` (Primary account)
- `GR1801718220007022123456789` (Secondary account)

**Credit Cards:** None

### External Bank Accounts (for Testing Remittances)
- `GR9202600260000000000299650` (Greek bank account)
- `CY22002001550000000000084100` (Cypriot bank account)

## Transaction Data Availability

### Valid Date Ranges for Transaction Queries

| User | Account/Card | Valid Transaction Period | Notes |
|------|--------------|-------------------------|-------|
| **UserA** | `GR2801718220007022123123123` | 01/12/2017 - 31/12/2017 | Primary account |
| **UserA** | `GR9001718220007025111222333` | 01/01/2018 - 31/01/2018 | Secondary account |
| **UserB** | `GR0101718220007027000224226` | 01/01/2018 - 31/01/2018 | Primary account |
| **UserB** | `GR0101718220007052999999000` | No transactions | Secondary account |
| **UserB** | `430589******6006` | 01/10/2017 - 31/12/2017 | Credit card |
| **UserC** | `GR0101718220007027000112113` | No transactions | Primary account |
| **UserC** | `GR1801718220007022123456789` | 01/01/2018 - 31/01/2018 | Secondary account |

## Sandbox-Specific Configuration

### Authentication Values

#### SCA Authentication
- **Sandbox SCA Code**: `3288000`
- **Use for all OTP scenarios**: SMS_OTP, PUSH_OTP, CHIP_OTP
- **TOUCH_OTP**: Simulated - no actual mobile app required

#### OAuth Scopes
- **Sandbox Scope**: `sandboxapi`
- **Offline Access**: `offline_access` (for refresh tokens)

### Sample OAuth Authorization URL
```
https://api.rapidlink.piraeusbank.gr/piraeusbank/production/v3.1/oauth/oauth2/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=sandboxapi+offline_access
```

## Testing Scenarios

### AIS Testing Workflow

#### AllPsd2 Consent Testing
1. **Login** with any test user (UserA, UserB, or UserC)
2. **Create AllPsd2 consent** - no SCA required
3. **Retrieve accounts** and **card-accounts** lists
4. **Limited access** - no balances or transactions available

#### Explicit Consent Testing
1. **Login** with test user
2. **Create explicit consent** for specific accounts/cards
3. **Complete SCA** using code `3288000`
4. **Access full data** - balances, transactions, account details

### PIS Testing Workflow

#### Own Account Transfer (No SCA)
1. **Login** with UserA
2. **Initiate transfer** between UserA's two accounts
3. **Direct execution** - no SCA required
4. **Check status** and completion

#### Third Party Transfer (SCA Required)
1. **Login** with UserB
2. **Initiate transfer** to UserA's account
3. **Complete SCA** using code `3288000`
4. **Execute payment** and verify completion

#### Inter-Bank Transfer (SCA + Fees)
1. **Login** with any user
2. **Initiate transfer** to external bank account
3. **Complete SCA** authentication
4. **Execute payment** with applicable fees

## Data Validation Rules

### Required Values for Valid Responses

#### Account Information
- **Use only predefined IBANs** from the test user accounts
- **Transaction date ranges** must fall within valid periods
- **Card numbers** must match the predefined masked PANs

#### Payment Information
- **Debtor accounts** must belong to authenticated user
- **Creditor accounts** can be any valid IBAN format
- **Amounts** should be reasonable (e.g., 1.00 - 10000.00 EUR)

### Error Scenarios
- **Invalid IBAN**: Use malformed IBAN to test validation
- **Invalid dates**: Use dates outside valid transaction periods
- **Invalid amounts**: Use negative or extremely large amounts
- **Invalid SCA**: Use wrong OTP code (not `3288000`)

## Certificate Requirements

### Sandbox Environment
- **No QWAC required**: Sandbox does not validate certificates
- **X-Client-Certificate header**: Can be omitted or use dummy value
- **Testing focus**: Functionality testing without certificate complexity

### Production Migration
- **QWAC certificate required**: Must obtain valid certificate for production
- **Certificate validation**: Production environment validates all certificates
- **Testing preparation**: Ensure certificate handling is implemented for production

## Rate Limiting and Quotas

### Sandbox Limits
- **No strict rate limiting**: Generous limits for testing
- **Session duration**: 60 minutes per OAuth token
- **Daily requests**: High limits suitable for development testing

### Best Practices
- **Implement proper error handling**: Test various error scenarios
- **Use refresh tokens**: Implement token refresh logic
- **Handle timeouts**: Test session expiration scenarios

## Debugging and Troubleshooting

### Common Issues

#### Authentication Problems
- **Wrong credentials**: Verify username/password combinations
- **Expired tokens**: Check token expiration and refresh
- **Invalid scope**: Ensure correct OAuth scope usage

#### Data Access Issues
- **Wrong consent type**: Use explicit consent for detailed data
- **Invalid date ranges**: Check transaction date validity
- **Missing SCA**: Complete authentication for explicit consents

#### Payment Issues
- **Invalid account references**: Use correct user account IBANs
- **SCA failures**: Use correct sandbox SCA code `3288000`
- **Amount validation**: Check payment amount formats

### Debugging Tools
- **Response headers**: Check X-Request-ID for request tracking
- **Error messages**: Analyze detailed error responses
- **Logs**: Monitor application logs for API call details

## Migration to Production

### Checklist Before Production
- [ ] **Certificate obtained**: Valid QWAC certificate installed
- [ ] **Credentials updated**: Production client ID and secret
- [ ] **URLs updated**: Switch to production endpoints
- [ ] **Error handling**: Comprehensive error handling implemented
- [ ] **Security review**: Code security audit completed
- [ ] **SCA implementation**: Real SCA handling (no hardcoded OTPs)

### Production Differences
- **Real customer data**: Actual bank customer information
- **Certificate validation**: Strict QWAC certificate requirements
- **SCA requirements**: Real two-factor authentication
- **Rate limiting**: Production rate limits apply
- **Monitoring**: Enhanced monitoring and logging required

## Support and Resources

### Sandbox Support
- **Documentation**: Complete API specifications available
- **Testing data**: Predefined datasets for comprehensive testing
- **Error simulation**: Test various error scenarios safely

### Development Best Practices
- **Version control**: Track API integration code changes
- **Testing automation**: Implement automated API testing
- **Security practices**: Follow secure coding guidelines
- **Compliance validation**: Ensure PSD2 compliance requirements

---

**Important**: Always use the sandbox environment for development and testing. Never test with production credentials or real customer data in the sandbox environment.