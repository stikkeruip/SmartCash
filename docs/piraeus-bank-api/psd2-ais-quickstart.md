# PSD2 AIS API Quick Start Guide

The PSD2 AIS (Account Information Service) API provides information related to the PSU's (Payment Service User - Bank Customer) Accounts, Credit Cards and their respective transactions.

## Overview

This API allows Third Party Providers (TPPs) to access customer account information in compliance with PSD2 regulations. The process involves enrollment, OAuth authorization, consent management, and SCA (Strong Customer Authentication).

## 1. Enrollment

### Developer Portal Registration

1. **Register/Login** to rAPIdLink Developer Portal
2. **Create Application** (e.g., "myapp001") with:
   - **Name** (Mandatory): Displayed to PSUs when granting access
   - **Description** (Optional): Brief app description
   - **OAuth Redirect URI** (Mandatory): OAuth response destination
     - Dummy URL acceptable: `https://127.0.0.1/this.is.the.redirect.url`
3. **Save Credentials**: Store `clientId` and `clientSecret` (only chance to save secret)
4. **Subscribe to PSD2 AIS Product** from API Products page

### Required Headers for All Calls
```http
X-Request-ID: [client-generated-guid]
X-IBM-Client-Id: [your-app-client-id]
```

## 2. OAuth Authorization

### Environment URLs

#### Production OAuth
- **Authorization URL**: `https://openbank.piraeusbank.gr/identityserver/connect/authorize`
- **Token URL**: `https://openbank.piraeusbank.gr/identityserver/connect/token`
- **Scopes**: `winbankAccess winbankAccess.info offline_access`
- **Optional Language**: `UI_Locales=el-GR`

#### Sandbox OAuth
- **Authorization URL**: `https://api.rapidlink.piraeusbank.gr/piraeusbank/production/v3.1/oauth/oauth2/authorize`
- **Token URL**: `https://api.rapidlink.piraeusbank.gr/piraeusbank/production/v3.1/oauth/oauth2/token`
- **Scopes**: `sandboxapi offline_access`

### Authorization Flow

#### Step 1: PSU Authorization
Build authorization URL:
```
https://[auth-url]?response_type=code&client_id=<ClientId>&redirect_uri=<RedirectUrl>&scope=<Scope>
```

**Sandbox Test Users**:
- UserA / 123
- UserB / 123  
- UserC / 123

#### Step 2: Get OAuth Token
After receiving authorization code, call:
```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

clientId=[your-client-id]
clientSecret=[your-client-secret]
grant_type=authorization_code
redirect_uri=[your-redirect-uri]
code=[authorization-code]
```

**Response**:
```json
{
  "token_type": "Bearer",
  "access_token": "AAjNS00YTQ4LWEjBl7uKgGRqn0fBJFrsz",
  "expires_in": 3600,
  "scope": "sandboxapi",
  "refresh_token": "AAIMaHP-nRIjZyLowTLnKRfsy0ZLoRFv53RoOraXg37Fltme36WwND4"
}
```

#### Step 3: Token Refresh (Production Only)
```http
POST [token-url]
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
client_Id=[your-client-id]
client_secret=[your-client-secret]
refresh_token=[previous-refresh-token]
```

## 3. Consent Management

### Step 1: Create "allPsd2" Consent
```http
POST /v3.1/consents
Authorization: Bearer [access-token]
X-Request-ID: [guid]
Consent-ID: [consent-guid]
x-ibm-client-id: [client-id]

{
  "access": {
    "accounts": [],
    "balances": [],
    "allPsd2": "allAccounts"
  },
  "recurringIndicator": true,
  "validUntil": "2019-06-30",
  "frequencyPerDay": 255,
  "combinedServiceIndicator": false
}
```

### Step 2: Retrieve Account Lists
Get accounts and card accounts (one-time calls only):
```http
GET /v3.1/accounts
GET /v3.1/card-accounts
```

### Step 3: Create Final Consent
Specify exact accounts for access:
```http
POST /v3.1/consents

{
  "access": {
    "accounts": [
      {"iban": "GR2801718220007022123123123", "currency": "EUR"}
    ],
    "balances": [
      {"iban": "GR2801718220007022123123123", "currency": "EUR"}
    ],
    "transactions": [
      {"iban": "GR2801718220007022123123123", "currency": "EUR"}
    ]
  },
  "recurringIndicator": true,
  "validUntil": "2019-08-30",
  "frequencyPerDay": 255,
  "combinedServiceIndicator": false
}
```

## 4. Strong Customer Authentication (SCA)

### Step 1: Start Authorization
```http
POST /v3.1/consents/[consent-id]/authorisations
```

**Response includes available SCA methods**:
- CHIP_OTP: Hardware token
- SMS_OTP: SMS to registered mobile
- PUSH_OTP: Mobile app notification
- TOUCH_OTP: Mobile app fingerprint

### Step 2: Select SCA Method (Optional)
```http
PUT /v3.1/consents/[consent-id]/authorisations/[auth-id]

{
  "authenticationMethodId": "2"
}
```

### Step 3: Complete SCA

#### For OTP Methods (CHIP/SMS/PUSH)
```http
PUT /v3.1/consents/[consent-id]/authorisations/[auth-id]

{
  "scaAuthenticationData": "3288000"
}
```
**Sandbox SCA Code**: `3288000`

#### For TOUCH_OTP
- PSU completes authentication in mobile banking app
- Check consent status to verify completion:
```http
GET /v3.1/consents/[consent-id]/authorisations/[auth-id]
```

## 5. Data Retrieval

Once consent is valid, access account information:

### Available Endpoints
- `/v3.1/accounts` - Account list
- `/v3.1/accounts/[account-id]` - Account details
- `/v3.1/accounts/[account-id]/balances` - Account balances
- `/v3.1/accounts/[account-id]/transactions` - Account transactions
- `/v3.1/card-accounts` - Card account list
- `/v3.1/card-accounts/[card-id]` - Card details
- `/v3.1/card-accounts/[card-id]/balances` - Card balances
- `/v3.1/card-accounts/[card-id]/transactions` - Card transactions

## Important Notes

### Data Validity
- **Access Duration**: 180 days from consent approval
- **Account/Card IDs**: Change with each new consent - must be retrieved fresh
- **Timezone**: All dates in Greece Athens Time (GMT+2/+3 with DST)

### Consent Constraints
- **"allPsd2" consent**: Limited to account/card listing (no balances), single use only
- **Final consent**: Full access to specified accounts for 180 days

### Error Handling
- Token expiration requires refresh (production) or re-authorization
- Consent expiration requires new consent process
- Failed SCA requires retry with correct authentication

## Sample Account Response
```json
{
  "accounts": [
    {
      "iban": "GR2801718220007022123123123",
      "currency": "EUR",
      "name": "ΤΑΜΙΕΥΤΗΡΙΟ 1",
      "displayName": "ΤΑΜΙΕΥΤΗΡΙΟ 1",
      "product": "SAVINGS ACC.-R-",
      "status": "enabled"
    }
  ]
}
```

## Sample Card Response
```json
{
  "card-accounts": [
    {
      "cardAccountType": "prepaid",
      "currency": "EUR",
      "pan": "5311460299913003"
    }
  ]
}
```