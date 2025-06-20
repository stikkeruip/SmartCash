# Piraeus Bank APIs (v1.1 & v1.2) Sandbox Reference

This document provides comprehensive information about the Sandbox environment for testing Piraeus Bank APIs (v1.1 and v1.2) without accessing real customer data.

## Overview

The Sandbox Environment simulates the bank's actual backend systems using dummy data for testing purposes. It provides isolated testing environments for third-party developers with predefined datasets and scenarios.

## Sandbox Database Architecture

### Data Isolation Features
- **Client-Specific Data**: Each application with unique `clientId` receives isolated dataset
- **Template Replication**: Basic data template replicated for each new client application
- **Data Reset Mechanism**: Available to restore original state if tests block functionality
- **Session Management**: OAuth tokens expire after 60 minutes

### User Types and Structure
- **3 Individual Users**: UserA, UserB, UserC
- **2 Corporate Users**: UserD, UserE
- **Varied Holdings**: Each user has specific accounts and cards (credit, debit, prepaid)

## Test Users and Authentication

### User Credentials
| User | Type | Username (Case Insensitive) | Password | Description |
|------|------|----------------------------|----------|-------------|
| **UserA** | INDIVIDUAL | `usera` | `123` | Individual user with 2 accounts |
| **UserB** | INDIVIDUAL | `userb` | `123` | Individual user with 2 accounts, 1 credit card |
| **UserC** | INDIVIDUAL | `userc` | `123` | Individual user with 2 accounts |
| **UserD** | CORPORATE | `userd` | `123` | Corporate user |
| **UserE** | CORPORATE | `usere` | `123` | Corporate user |

### OAuth Authentication Process
1. **Application Redirect**: Users redirected to authentication page
2. **Credential Entry**: Users enter username/password
3. **Authorization Grant**: Users grant access rights to application
4. **Bearer Token**: OAuth token generated for API access (60-minute expiration)

## API Categories and Testing Scenarios

### Customer APIs

#### GET /customer/info
- **Requirements**: Authorization Header only
- **Purpose**: Retrieve customer information
- **No additional parameters needed**

### Security APIs

#### Token Management
**Available Endpoints:**
- `POST /{TokenType}/generate`
- `POST /{TokenType}/generate/force`
- `GET /token/validate/{TokenValue}`
- `GET /{TokenType}/validate/{TokenValue}`
- `POST /token/select/{TokenType}/for/{SessionKey}`

**Required Parameters:**
- **TokenType**: `extrapin` or `otp`
- **TokenValue**: `3288000` (sandbox universal code)

#### Trusted Beneficiaries APIs

**Available Endpoints:**
- `GET /` - List current trusted beneficiaries
- `GET /list` - List staged trusted beneficiaries
- `POST /list` - Stage new trusted beneficiary
- `DELETE /list` - Clear entire staged list
- `DELETE /list/{stagedId}` - Delete specific staged entry
- `POST /validate` - Stage entries for insertion
- `POST /execute` - Execute staged changes
- `DELETE /{trustedBeneficiaryID}` - Delete active beneficiary

**Sample GET / Response:**
```json
{
  "whitelistEntries": [
    {
      "whitelistId": "VDA6RPYZ2Mp",
      "operationDescription": "Vodafone Mobile/Fixed",
      "whitelistType": 4,
      "whitelistTypeDescription": "Operation",
      "displayName": "Vodafone Mobile/Fixed",
      "updateDate": "2023-01-16T16:33:38.917"
    }
  ]
}
```

**Sample POST /list Body:**
```json
{
  "DisplayName": "Bank of Greece",
  "ProductValue": "GR1601101250000000012300695",
  "BeneficiaryBank": {
    "Name": "ΕΘΝΙΚΗ ΤΡΑΠΕΖΑ ΤΗΣ ΕΛΛΑΔΟΣ",
    "Bic": "ETHNGRAAXXX",
    "Address": "AIOLOU STR 86",
    "CountryIsoCode": "GRC",
    "City": "Athens"
  },
  "BeneficiaryName": "John Doe"
}
```

#### Approvals APIs

**Available Endpoints:**
- `GET /` - List pending transactions (own and others)
- `GET /list` - List staged approvals
- `DELETE /list` - Clear staged approvals
- `DELETE /list/{approvalKey}` - Delete specific staged approval
- `POST /list/{approvalKey}` - Add approval to staging
- `POST /validate` - Stage for approval
- `DELETE /validate` - Stage for rejection
- `POST /execute` - Execute approval/rejection

**Important Notes:**
- Cannot combine "own" and "others" transactions in staging
- All execute operations require ExtraPin: `3288000`

### Lookups APIs

#### Points of Presence
- `GET /POP/list` - All points of presence
- `GET /POP/{PointTypeName}/list` - Specific type

**Valid PointTypeName Values:**
- `none`, `atm`, `aps`, `branch`, `ebranch`, `all`

## User Account and Card Data

### Account Holdings
| User | Accounts | Credit Cards |
|------|----------|--------------|
| **UserA** | `GR2801718220007022123123123`<br>`GR9001718220007025111222333` | None |
| **UserB** | `GR0101718220007027000224226`<br>`GR0101718220007052999999000` | `430589******6006` |
| **UserC** | `GR0101718220007027000112113`<br>`GR1801718220007022123456789` | None |

### External Bank Accounts (for testing)
- `GR9202600260000000000299650`
- `CY22002001550000000000084100`

### Transaction Data Availability
| User | Account/Card | Valid Transaction Dates |
|------|--------------|------------------------|
| **UserA** | `GR2801718220007022123123123` | 01/12/2017 - 31/12/2017 |
| **UserA** | `GR9001718220007025111222333` | 01/01/2018 - 31/01/2018 |
| **UserB** | `GR0101718220007027000224226` | 01/01/2018 - 31/01/2018 |
| **UserB** | `GR0101718220007052999999000` | No transactions |
| **UserB** | `430589******6006` | 01/10/2017 - 31/12/2017 |
| **UserC** | `GR0101718220007027000112113` | No transactions |
| **UserC** | `GR1801718220007022123456789` | 01/01/2018 - 31/01/2018 |

## Accounts & Cards APIs

### Account APIs
- `GET /accounts/` - List all accounts
- `GET /accounts/{accountId}/details` - Account details
- `GET /accounts/{accountId}/transactions/{input_filter}` - Account transactions

### Card APIs
- `GET /cards/list` - All cards
- `GET /cards/credit/list` - Credit cards only
- `GET /cards/debit/list` - Debit cards only
- `GET /cards/prepaid/list` - Prepaid cards only
- `GET /cards/{cardId}/details` - Card details
- `GET /cards/{cardId}/transactions/{input_filter}` - Card transactions

### Sample Transaction Filter
```json
{
  "fromDate": "2017-9-1",
  "toDate": "2018-1-30",
  "fromRow": "",
  "pageSize": 20,
  "lastBalance": 0.0
}
```

## Loans APIs

### Available Endpoints
- `GET /loans/` - List all loans
- `GET /loans/{loanId}/details` - Loan details
- `GET /loans/{loanId}/transactions/{input_filter}` - Loan transactions

### Loan Data
- **All users have same 3 loans**
- **2 loans have transactions**
- **Loan `GR4301720110005011022626108` has no transactions**

### Sample Loan Transaction Filter
```json
{
  "fromDate": "2017-09-01",
  "toDate": "2018-01-30",
  "fromRow": "5",
  "pageSize": 20
}
```

## Transactions APIs

### Transfer to IBAN
- `POST /TransferToIban` - Initiate transfer
- `POST /TransferToIban/Validate` - Validate transfer
- `POST /TransferToIban/Execute/{SessionKey}` - Execute transfer

### Sample Transfer Request
```json
{
  "AccountId": "string",
  "IBAN": "string",
  "Amount": 0.0,
  "Reason": "string",
  "Currency": "EUR",
  "ChargeType": "string",
  "Priority": "string",
  "ContactPhone": "306911111111",
  "BeneficiaryName": "string",
  "SepaInfo": "123456"
}
```

### Valid Transfer Destinations

#### Intra-Bank Transfers
- `GR2801718220007022123123123`
- `GR1801718220007022123456789`
- `GR9001718220007025111222333`
- `GR0101718220007027000112113`
- `GR0101718220007052999999000`

#### Remittance (External Banks)
- `GR9202600260000000000299650`
- `CY22002001550000000000084100`

### Bulk Payments (DEPRECATED)
- `POST /BulkPayment` - Upload bulk payment file
- `POST /BulkPayment/Validate` - Validate bulk payment
- `POST /BulkPayment/Execute/{SessionKey}` - Execute bulk payment
- `GET /BulkPayment/History/{input_filter}` - Payment history
- `GET /BulkPayment/{PaymentCode}/{PaymentDate}/Details` - Payment details

### Payroll Payments
- `POST /Payroll` - Upload payroll file
- `POST /Payroll/Validate` - Validate payroll
- `POST /Payroll/Execute/{SessionKey}` - Execute payroll
- `GET /Payroll/History/{input_filter}` - Payroll history
- `GET /Payroll/{PaymentCode}/Details` - Payroll details

### Sample Payroll Parameters
```json
{
  "AssetFrom": "agBqAGcAdwAxAHUAZQBpALcKtwDKV%2bLF%2bkC3Fc7p%2fLY%3d",
  "AssetType": 1,
  "ContractNumber": "3051",
  "DisketteNumber": 1,
  "NumberOfPayments": 2,
  "Description": "AAA",
  "PaymentDate": "2017-06-07T21:00:00.000Z",
  "Amount": 2.3,
  "Currency": "EUR",
  "payload": ""
}
```

## Payments APIs

### Available Endpoints
- `GET /codes` - List payment definitions
- `GET /codes/{paymentCode}` - Specific payment definition
- `POST /single/{RFCode}/validate` - Validate RF payment
- `POST /single/{RFCode}/execute/{SessionKey}` - Execute RF payment
- `POST /{paymentCode}/validate` - Validate payment by code
- `POST /{paymentCode}/execute/{SessionKey}` - Execute payment
- `GET /{paymentOrderID}/history` - Payment history
- `GET /{paymentOrderID}/{paymentID}` - Payment details
- `PUT /{paymentOrderID}/action/{action}` - Update payment
- `GET /history/type/{type}` - Payment history by type

### Sample Payment Codes
- **6201**: EFKA Employers Contributions
- **6202**: OAEE
- **6303**: Vodafone
- **7394**: Brokins

### Sample RF Payment Request
```json
{
  "assetId": "NjVBMENEMTAtNUI2Mi00QjhELTlFMDYtMkZBOENDQUQ0ODlCMUIzNUQxRDUtMzc4",
  "assetType": "account",
  "amount": 10.5,
  "currency": "EUR",
  "scheduling": {
    "executionDate": "2023-03-03",
    "recurrence": "2",
    "recurrenceDay": "3"
  }
}
```

### Sample Generic Payment Request
```json
{
  "fields": [
    {
      "name": "AssetFrom",
      "value": "MUVBRUZBN0YtRUM4NS00QUU5LTk4RkMtOTM1MjIyMUU1MTgyRjYyMUZDNTQtM0Uw",
      "assetType": "account"
    },
    {
      "name": "SubscriberCode",
      "value": "3947749202221"
    },
    {
      "name": "AmountValue",
      "value": "1.5",
      "currency": "EUR"
    },
    {
      "name": "PayeeName",
      "value": "test"
    }
  ]
}
```

## Predefined Test Scenarios

### BulkPayment History Test Data

#### Scenario 1: 2015 Data
**Input Filter:**
```json
{
  "fromDate": "2015-02-01T00:00:00.00",
  "toDate": "2015-08-01T00:00:00.00"
}
```

**Expected Response:** 6 bulk payment records with various statuses

#### Scenario 2: 2017 Data
**Input Filter:**
```json
{
  "fromDate": "2017-01-01T00:00:00.00",
  "toDate": "2017-06-30T00:00:00.00"
}
```

**Expected Response:** 1 failed bulk payment record

### Payroll History Test Data
**Input Filter:**
```json
{
  "fromDate": "2015-02-01T00:00:00.00",
  "toDate": "2015-08-01T00:00:00.00"
}
```

**Expected Response:** 1 payroll payment record

## Important Sandbox Limitations

### File Upload Simplifications
- **No content validation**: Only filename and metadata stored
- **Unique filename requirement**: Per user and clientId
- **FileID generation**: Used for subsequent validation steps

### Fixed Response Scenarios
- **Trusted beneficiaries**: Fixed dataset, changes not persisted
- **Payment details**: Some return "details not available" message
- **RF payments**: Always reference Wind regardless of RF code

### Universal Test Values
- **ExtraPin**: Always `3288000` for all SCA scenarios
- **Token validation**: Use `3288000` for all OTP validations
- **Session timeout**: 60 minutes for all OAuth tokens

## Error Handling and Validation

### Common Error Scenarios
- **Invalid date ranges**: Outside valid transaction periods
- **Wrong account references**: Using non-existent account IDs
- **Invalid IBAN formats**: Malformed or non-whitelisted IBANs
- **Expired sessions**: OAuth token timeout after 60 minutes
- **File upload conflicts**: Duplicate filenames per user/client

### Expected Error Messages
- **No transactions**: "Η συναλλαγή σας δεν εκτελέστηκε λόγω προβλήματος στην επικοινωνία"
- **Details unavailable**: "Τα αναλυτικά στοιχεία δεν είναι διαθέσιμα"
- **Combined transaction types**: "Can't combine 'own' and 'other' type entries"

## Migration to Production

### Key Differences from Sandbox
- **Real customer data**: Actual bank customer information
- **File content validation**: Full file processing and validation
- **Persistent data changes**: All operations affect real data
- **Real SCA codes**: Actual OTP generation and validation
- **Enhanced security**: Full certificate and authentication requirements

### Production Preparation Checklist
- [ ] Replace sandbox URLs with production endpoints
- [ ] Implement real SCA handling (remove hardcoded `3288000`)
- [ ] Add proper file content validation
- [ ] Implement comprehensive error handling
- [ ] Add production certificate management
- [ ] Test with real but limited data sets
- [ ] Implement proper logging and monitoring

---

**Important**: Always use predefined test values and scenarios in sandbox environment. The sandbox provides a safe testing environment but has simplified validation and fixed datasets for testing purposes.