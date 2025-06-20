# PSD2 PIS API Implementation Examples

This document provides detailed examples of monetary transfers using the PSD2 PIS API, covering three main scenarios with complete request/response flows.

## Overview

The PIS API supports three transfer scenarios:
- **Scenario #1**: Transfer between PSU's own accounts (no SCA required)
- **Scenario #2**: Transfer to third party within Piraeus Bank (SCA required)
- **Scenario #3**: Transfer to external bank - remittance (SCA required)

### Key Concepts

#### SCA Requirements
- **Own accounts**: No SCA required
- **Whitelisted beneficiaries**: No SCA required
- **Third party transfers**: SCA required
- **Inter-bank transfers**: SCA required

#### Mandatory vs Optional Steps
**Mandatory Steps:**
- Payment initiation
- Payment execution
- SCA authorization (when required)

**Optional Steps:**
- Payment information retrieval (`self` link)
- Payment status check (`status` link)
- SCA method selection (`selectAuthenticationMethod` link)
- SCA status check (`scaStatus` link)

---

## Scenario #1: Transfer Between PSU's Own Accounts

### Step 1: Initiate Payment

**No SCA required** - Response includes `execute` link for direct execution.

**Request:**
```http
POST /v3.1/payments/sepa-credit-transfers
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]

{
  "endToEndIdentification": "1111111",
  "debtorAccount": {
    "iban": "GR34********************131",
    "currency": "EUR"
  },
  "instructedAmount": {
    "currency": "EUR",
    "amount": "123.00"
  },
  "creditorAccount": {
    "iban": "GR33********************149",
    "currency": "EUR",
    "msisdn": "6979797979"
  },
  "creditorAgent": "",
  "creditorName": "G. Pap.",
  "creditorAddress": {
    "street": "",
    "buildingNumber": "",
    "city": "",
    "postalCode": "",
    "country": ""
  },
  "remittanceInformationUnstructured": "{\"comments\": \"test transfer to own account\"}"
}
```

**Response:**
```json
{
  "transactionStatus": "RCVD",
  "paymentId": "8183f925-d604-4bd1-b44f-54201848f4fc",
  "transactionFees": {
    "amount": 0
  },
  "transactionFeeIndicator": false,
  "_links": {
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "execute": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "POST"
    }
  }
}
```

### Step 2: Execute Payment

**Request:**
```http
POST [execute-link-from-previous-response]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
```

**Response:**
```json
{
  "transactionStatus": "ACCC",
  "paymentId": "8183f925-d604-4bd1-b44f-54201848f4fc",
  "transactionFees": {
    "amount": 0
  },
  "transactionFeeIndicator": false,
  "_links": {
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    }
  },
  "psuMessage": "EB17061900457354"
}
```

### Optional Steps

#### Get Payment Information
```http
GET [self-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
```

**Response:**
```json
{
  "endToEndIdentification": "1111111",
  "debtorAccount": {
    "iban": "GR3401729760005976008074131",
    "currency": "EUR"
  },
  "instructedAmount": {
    "currency": "EUR",
    "amount": 55
  },
  "creditorAccount": {
    "iban": "GR3301729760005976008074149",
    "msisdn": "6979797979",
    "currency": "EUR"
  },
  "creditorAgent": "",
  "creditorName": "G. Pap",
  "creditorAddress": {
    "streetName": "",
    "buildingNumber": "",
    "townName": "",
    "postCode": "",
    "country": ""
  },
  "remittanceInformationUnstructured": "{\"comments\": \"test transfer to own account\"}",
  "transactionStatus": "ACSC"
}
```

#### Get Payment Status
```http
GET [status-link]
```

**Response:**
```json
{
  "transactionStatus": "ACSC"
}
```

### Note: Unnecessary Authorization Attempt

If you call the authorization endpoint when not required:

**Response:**
```json
{
  "tppMessages": [
    {
      "category": "ERROR",
      "code": "SCA_METHOD_UNKNOWN",
      "text": "This payment does not require authorisation. Proceed with direct execution through 'execute' link."
    }
  ]
}
```

---

## Scenario #2: Transfer to Third Party Within Piraeus Bank

### Step 1: Initiate Payment

**SCA required** - Response includes `startAuthorisation` link.

**Request:**
```http
POST /v3.1/payments/sepa-credit-transfers
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]

{
  "endToEndIdentification": "22222222",
  "debtorAccount": {
    "iban": "GR34********************131",
    "currency": "EUR"
  },
  "instructedAmount": {
    "currency": "EUR",
    "amount": "123.00"
  },
  "creditorAccount": {
    "iban": "GR65********************000",
    "currency": "EUR",
    "msisdn": "6979797979"
  },
  "creditorAgent": "",
  "creditorName": "Al. Konst.",
  "creditorAddress": {
    "street": "",
    "buildingNumber": "",
    "city": "",
    "postalCode": "",
    "country": ""
  },
  "remittanceInformationUnstructured": "{\"comments\": \"test transfer to third party account\"}"
}
```

**Response:**
```json
{
  "transactionStatus": "RCVD",
  "paymentId": "cc1daf39-809e-4ab1-a2b9-f483bdd351ba",
  "transactionFees": {
    "amount": 0
  },
  "transactionFeeIndicator": false,
  "_links": {
    "startAuthorisation": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "POST"
    },
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    }
  }
}
```

### Step 2: Authorize Transaction

**Request:**
```http
POST [startAuthorisation-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
```

**Response:**
```json
{
  "scaStatus": "scaMethodSelected",
  "authorisationId": "a6657311-14cd-422c-8f35-1053076dbd7f",
  "scaMethods": [
    {
      "authenticationType": "TOUCH_OTP",
      "authenticationMethodId": "8",
      "name": "ExtraPin through Notification with Touch ID in winbank mobile app"
    },
    {
      "authenticationType": "SMS_OTP",
      "authenticationMethodId": "2",
      "name": "ExtraPin through SMS on the declared mobile phone number"
    }
  ],
  "chosenScaMethod": {
    "authenticationType": "TOUCH_OTP",
    "authenticationMethodId": "8",
    "name": "SCA through notification to the registered mobile application, using fingerprint functionality"
  },
  "_links": {
    "authoriseTransaction": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "PUT"
    },
    "selectAuthenticationMethod": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "PUT"
    },
    "scaStatus": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "execute": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "POST"
    }
  }
}
```

### Step 3a: Select Authentication Method (Optional)

**Request:**
```http
PUT [selectAuthenticationMethod-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]

{
  "authenticationMethodId": 2
}
```

**Response:**
```json
{
  "chosenScaMethod": {
    "authenticationType": "SMS_OTP",
    "authenticationMethodId": "2",
    "name": "SCA through SMS message to the registered mobile number, using one time pin"
  },
  "_links": {
    "authoriseTransaction": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "PUT"
    },
    "scaStatus": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    }
  },
  "scaStatus": "scaMethodSelected"
}
```

### Step 3b: Update PSU Authentication Data (Mandatory)

**Request:**
```http
PUT [authoriseTransaction-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]

{
  "scaAuthenticationData": "3288000"
}
```

**Response:**
```json
{
  "_links": {
    "execute": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "POST"
    },
    "scaStatus": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    }
  },
  "scaStatus": "finalised"
}
```

### Step 4: Execute Payment

**Request:**
```http
POST [execute-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
```

**Response:**
```json
{
  "transactionStatus": "ACCC",
  "paymentId": "cc1daf39-809e-4ab1-a2b9-f483bdd351ba",
  "transactionFees": {
    "amount": 0
  },
  "transactionFeeIndicator": false,
  "_links": {
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    }
  },
  "psuMessage": "EB17061900485673"
}
```

### Optional Step: Get SCA Status

**Request:**
```http
GET [scaStatus-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
```

**Response:**
```json
{
  "scaStatus": "finalised"
}
```

**Possible SCA Status Values:**
- `scaMethodSelected`
- `finalised`
- `failed`
- `rejected`

---

## Scenario #3: Remittance (Inter-Bank Transfer)

### Step 1: Initiate Payment

**Note**: Transaction fees apply for inter-bank transfers.

**Request:**
```http
POST /v3.1/payments/sepa-credit-transfers
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]

{
  "endToEndIdentification": "333333",
  "debtorAccount": {
    "iban": "GR34********************131",
    "currency": "EUR"
  },
  "instructedAmount": {
    "currency": "EUR",
    "amount": "123.00"
  },
  "creditorAccount": {
    "iban": "CY04********************4100",
    "currency": "EUR",
    "msisdn": "003545789252"
  },
  "creditorAgent": "",
  "creditorName": "N. Nikolaou",
  "creditorAddress": {
    "street": "",
    "buildingNumber": "",
    "city": "",
    "postalCode": "",
    "country": ""
  },
  "remittanceInformationUnstructured": "{\"comments\": \"test remittance\"}"
}
```

**Response:**
```json
{
  "transactionStatus": "RCVD",
  "paymentId": "5eadb71c-269a-41c0-a384-4be859247dbf",
  "transactionFees": {
    "amount": 0.30
  },
  "transactionFeeIndicator": true,
  "_links": {
    "startAuthorisation": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "POST"
    },
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    }
  }
}
```

### Step 2: Authorize Transaction

**Request:**
```http
POST [startAuthorisation-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
```

**Response:**
```json
{
  "scaStatus": "scaMethodSelected",
  "authorisationId": "b500f88c-aca8-4ecc-b2cf-1550edb6f7c7",
  "scaMethods": [
    {
      "authenticationType": "TOUCH_OTP",
      "authenticationMethodId": "8",
      "name": "ExtraPin through Notification with Touch ID in winbank mobile app"
    },
    {
      "authenticationType": "SMS_OTP",
      "authenticationMethodId": "2",
      "name": "ExtraPin through SMS on the declared mobile phone number"
    }
  ],
  "chosenScaMethod": {
    "authenticationType": "TOUCH_OTP",
    "authenticationMethodId": "8",
    "name": "SCA through notification to the registered mobile application, using fingerprint functionality"
  },
  "_links": {
    "authoriseTransaction": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "PUT"
    },
    "selectAuthenticationMethod": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "PUT"
    },
    "scaStatus": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "execute": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "POST"
    }
  }
}
```

### Step 3: TOUCH_OTP Authentication

**For TOUCH_OTP**, no authentication data update is required. The PSU completes authentication via mobile app.

**Monitor SCA status** until it shows "received" or "finalised":

```http
GET [scaStatus-link]
```

### Step 4: Execute Payment

**Request:**
```http
POST [execute-link]
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
```

**Response:**
```json
{
  "transactionStatus": "ACSC",
  "paymentId": "5eadb71c-269a-41c0-a384-4be859247dbf",
  "transactionFees": {
    "amount": 0.30
  },
  "transactionFeeIndicator": true,
  "_links": {
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/...",
      "verb": "GET"
    }
  },
  "psuMessage": "F928TO0000007186"
}
```

---

## Important Implementation Notes

### Transaction Status Values
- **RCVD**: Received
- **ACCC**: Accepted Customer Credit Transfer
- **ACSC**: Accepted Settlement Completed

### SCA Authentication Types
- **CHIP_OTP**: Hardware token device
- **SMS_OTP**: SMS to registered mobile
- **PUSH_OTP**: Push notification to mobile app
- **TOUCH_OTP**: Fingerprint authentication in mobile app

### Mandatory Fields for Remittances
- `creditorName`: Required for inter-bank transfers
- `remittanceInformationUnstructured.comments`: Required for inter-bank transfers

### Transaction Fees
- **Own account transfers**: No fees
- **Intra-bank transfers**: No fees
- **Inter-bank transfers**: Fees may apply (shown in response)

### Error Handling
Always check response status and handle errors appropriately. Failed SCA attempts or invalid data will result in error responses with detailed messages.