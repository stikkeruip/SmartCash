# PSD2 PIS API Quick Start Guide

The PSD2 PIS (Payment Initiation Service) API provides support for monetary transfers from a PSU's account towards:
- An account of the same PSU within Piraeus Bank
- An account of another PSU within Piraeus Bank  
- An account in another bank (domestic or international)

## Overview

This API allows Third Party Providers (TPPs) to initiate payments on behalf of Payment Service Users (PSUs) in compliance with PSD2 regulations. The process involves enrollment, OAuth authorization, payment initiation, authorization, and execution.

## 1. Enrollment

### Developer Portal Registration

1. **Register/Login** to rAPIdLink Developer Portal
2. **Create Application** (e.g., "myapp001") with:
   - **Name** (Mandatory): Displayed to PSUs when granting access
   - **Description** (Optional): Brief app description
   - **OAuth Redirect URI** (Mandatory): OAuth response destination
     - Dummy URL acceptable: `https://127.0.0.1/this.is.the.redirect.url`
3. **Save Credentials**: Store `clientId` and `clientSecret` (only chance to save secret)
4. **Subscribe to PSD2 PIS Product** from API Products page

### Required Headers for All Calls
```http
X-IBM-Client-Id: [your-app-client-id]
X-Request-ID: [client-generated-guid]
X-Client-Certificate: [QWAC-pem-content]
```

**Important**: PIS requires QWAC (Qualified Website Authentication Certificate) for production use.

## 2. OAuth Authorization

### Environment URLs

#### Production OAuth
- **Authorization URL**: `https://openbank.piraeusbank.gr/identityserver/connect/authorize`
- **Token URL**: `https://openbank.piraeusbank.gr/identityserver/connect/token`
- **Scopes**: `winbankAccess winbankAccess.info winbankAccess.monetaryTransactions offline_access`
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

**Token Validity**:
- **Access Token**: 3600 seconds (1 hour)
- **Refresh Token**: 90 days

#### Step 3: Token Refresh
```http
POST [token-url]
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
client_Id=[your-client-id]
client_secret=[your-client-secret]
refresh_token=[previous-refresh-token]
```

## 3. Payment Initiation Process

The PIS API follows a three-step process for payment execution:

### Payment Flow Overview
1. **Initiate Payment** - Create payment request
2. **Authorize Payment** - Complete SCA (Strong Customer Authentication)
3. **Execute Payment** - Finalize the transaction

### Payment Types Supported
- **Domestic Transfers**: Within Greece
- **SEPA Transfers**: Within SEPA zone
- **International Transfers**: Outside SEPA zone
- **Instant Payments**: Real-time transfers
- **Bulk Payments**: Multiple transfers in one request

### Required Payment Information
- **Debtor Account**: PSU's account (IBAN)
- **Creditor Account**: Beneficiary's account (IBAN)
- **Amount**: Transfer amount and currency
- **Payment Details**: Description, reference, etc.

### Sample Payment Initiation
```http
POST /v3.1/payments/sepa-credit-transfers
Authorization: Bearer [access-token]
X-Request-ID: [guid]
X-IBM-Client-Id: [client-id]
X-Client-Certificate: [qwac-content]
Content-Type: application/json

{
  "debtorAccount": {
    "iban": "GR1234567890123456789012345"
  },
  "creditorAccount": {
    "iban": "GR9876543210987654321098765"
  },
  "instructedAmount": {
    "currency": "EUR",
    "amount": "100.00"
  },
  "remittanceInformationUnstructured": "Payment description"
}
```

## 4. Strong Customer Authentication (SCA)

### SCA Methods Available
- **CHIP_OTP**: Hardware token device
- **SMS_OTP**: SMS to registered mobile number
- **PUSH_OTP**: Mobile app push notification
- **TOUCH_OTP**: Mobile app fingerprint authentication

### SCA Process
1. **Start Authorization**: Initiate SCA process
2. **Select Method**: Choose authentication method (if multiple available)
3. **Complete Authentication**: Provide OTP or complete mobile app authentication
4. **Verify Status**: Confirm authentication success

### Sample SCA Flow
```http
POST /v3.1/payments/[payment-id]/authorisations
Authorization: Bearer [access-token]
X-Request-ID: [guid]
```

**Response**:
```json
{
  "scaStatus": "scaMethodSelected",
  "authorisationId": "auth-123",
  "scaMethods": [
    {
      "authenticationType": "SMS_OTP",
      "authenticationMethodId": "2",
      "name": "SMS to registered mobile"
    }
  ],
  "chosenScaMethod": {
    "authenticationType": "SMS_OTP",
    "authenticationMethodId": "2"
  }
}
```

## 5. Payment Execution

### Execute Payment
After successful SCA, complete the payment:
```http
PUT /v3.1/payments/[payment-id]/authorisations/[auth-id]
Authorization: Bearer [access-token]
X-Request-ID: [guid]

{
  "scaAuthenticationData": "[otp-code]"
}
```

### Payment Status Check
Monitor payment status:
```http
GET /v3.1/payments/[payment-id]/status
Authorization: Bearer [access-token]
X-Request-ID: [guid]
```

**Status Values**:
- `RCVD`: Received
- `PDNG`: Pending
- `ACTC`: Accepted
- `RJCT`: Rejected
- `ACSC`: Accepted Settlement Completed

## 6. Available Payment Products

### Standard Payment Types
- `/v3.1/payments/sepa-credit-transfers` - SEPA transfers
- `/v3.1/payments/cross-border-credit-transfers` - International transfers
- `/v3.1/payments/target-2-payments` - TARGET2 payments

### Bulk Payments
- `/v3.1/bulk-payments/sepa-credit-transfers` - Bulk SEPA transfers
- `/v3.1/bulk-payments/cross-border-credit-transfers` - Bulk international transfers

### Instant Payments
- `/v3.1/payments/sepa-instant-credit-transfers` - SEPA instant transfers

## 7. Error Handling

### Common Error Scenarios
- **Invalid Account**: IBAN validation failed
- **Insufficient Funds**: Account balance too low
- **SCA Failure**: Authentication failed or expired
- **Payment Rejected**: Bank business rules violation

### Error Response Format
```json
{
  "tppMessages": [
    {
      "category": "ERROR",
      "code": "PAYMENT_FAILED",
      "text": "Payment execution failed"
    }
  ]
}
```

## 8. Certificate Requirements

### Production Environment
- **QWAC Certificate**: Required for production API calls
- **Certificate Format**: PEM format in X-Client-Certificate header
- **Certificate Validation**: Bank validates certificate authenticity

### Sandbox Environment
- **No Certificate Required**: Sandbox does not require QWAC
- **Testing Purpose**: Use sandbox for development and testing

## Important Notes

### Payment Limits
- **Daily Limits**: Per PSU daily transaction limits apply
- **Amount Limits**: Maximum per-transaction amounts may apply
- **Frequency Limits**: Number of transactions per day may be limited

### Compliance Requirements
- **PSD2 Compliance**: All regulations must be followed
- **SCA Requirements**: Strong authentication for all payments
- **Data Protection**: GDPR compliance required

### Best Practices
- **Timeout Handling**: Implement proper timeout mechanisms
- **Status Monitoring**: Regular payment status checks
- **Error Recovery**: Graceful handling of failed payments
- **Certificate Management**: Proper QWAC certificate lifecycle management

## Sample Complete Flow

### 1. Payment Initiation
```http
POST /v3.1/payments/sepa-credit-transfers
[headers and payment data]
```

### 2. Start Authorization
```http
POST /v3.1/payments/payment-123/authorisations
```

### 3. Complete SCA
```http
PUT /v3.1/payments/payment-123/authorisations/auth-456
{"scaAuthenticationData": "123456"}
```

### 4. Check Status
```http
GET /v3.1/payments/payment-123/status
```

### 5. Get Payment Details
```http
GET /v3.1/payments/payment-123
```

---

**Note**: For detailed implementation examples, refer to the "PIS Examples" section in the complete API documentation.