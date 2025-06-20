# PSD2 AIS API Implementation Examples

This document provides detailed examples of Account Information Service operations using the PSD2 AIS API, covering consent management and data retrieval for both AllPsd2 and Explicit consent types.

## Overview

The AIS API supports two consent types:
- **AllPsd2 Consent**: Simple consent for account/card listing (limited functionality)
- **Explicit Consent**: Detailed consent for specific accounts with full access to balances and transactions

### Key Differences

| Feature | AllPsd2 Consent | Explicit Consent |
|---------|-----------------|------------------|
| **SCA Required** | No | Yes |
| **Account Details** | Basic listing only | Full details available |
| **Balances** | Not available | Available with authorization |
| **Transactions** | Not available | Available with authorization |
| **Usage Limit** | One-time use | Recurring (based on frequencyPerDay) |

---

## Consent Management

### Create AllPsd2 Consent

**Purpose**: Quick consent for account and card listing without detailed information.

**Request:**
```http
POST /v3.1/consents
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]

{
  "access": {
    "allPsd2": "allAccounts"
  },
  "recurringIndicator": true,
  "validUntil": "2020-12-31T23:59:59.000Z",
  "frequencyPerDay": 1,
  "combinedServiceIndicator": false
}
```

**Response:**
```json
{
  "consentStatus": "valid",
  "consentId": "400ab141-b1b0-4920-bd57-9cee98ea3a2e",
  "_links": {
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/400ab141-b1b0-4920-bd57-9cee98ea3a2e",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/400ab141-b1b0-4920-bd57-9cee98ea3a2e/status",
      "verb": "GET"
    }
  }
}
```

**Note**: AllPsd2 consent is immediately valid and requires no SCA.

### Create Explicit Consent

**Purpose**: Detailed consent for specific accounts with full access permissions.

**Request:**
```http
POST /v3.1/consents
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]

{
  "access": {
    "accounts": [
      {"iban": "GR0101718220007027000224226"},
      {"iban": "GR0101718220007052999999000"},
      {"maskedPan": "430589******6006"}
    ],
    "balances": [
      {"iban": "GR0101718220007027000224226"},
      {"maskedPan": "430589******6006"}
    ],
    "transactions": [
      {"iban": "GR0101718220007027000224226"},
      {"maskedPan": "430589******6006"}
    ]
  },
  "recurringIndicator": true,
  "validUntil": "2020-12-31T23:59:59.000Z",
  "frequencyPerDay": 1,
  "combinedServiceIndicator": false
}
```

**Response:**
```json
{
  "consentStatus": "received",
  "consentId": "9881137a-b159-451b-bdf3-ad57da454885",
  "_links": {
    "startAuthorisation": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations",
      "verb": "POST"
    },
    "self": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885",
      "verb": "GET"
    },
    "status": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/status",
      "verb": "GET"
    }
  }
}
```

**Note**: Explicit consent requires SCA authorization before becoming valid.

---

## SCA Authorization (Explicit Consent Only)

### Start Authorization

**Request:**
```http
POST /v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations
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
  "authorisationId": "7617a049-c6db-42d7-ac61-8871b849c23f",
  "scaMethods": [
    {
      "authenticationType": "SMS_OTP",
      "authenticationMethodId": "2",
      "name": "ExtraPin through SMS on the declared mobile phone number"
    }
  ],
  "chosenScaMethod": {
    "authenticationType": "SMS_OTP",
    "authenticationMethodId": "2",
    "name": "SCA through SMS message to the registered mobile number, using one time pin"
  },
  "_links": {
    "selectAuthenticationMethod": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f",
      "verb": "PUT"
    },
    "authoriseTransaction": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f",
      "verb": "PUT"
    },
    "scaStatus": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f",
      "verb": "GET"
    }
  }
}
```

### Select Authentication Method (Optional)

**Request:**
```http
PUT /v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
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
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f",
      "verb": "PUT"
    },
    "scaStatus": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f",
      "verb": "GET"
    }
  },
  "scaStatus": "scaMethodSelected"
}
```

### Update PSU Authentication Data

**Request:**
```http
PUT /v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
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
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f&executionKey=795db7a3c8d74adda7645c6900e3ee99&scaAuthenticationData=3288000",
      "verb": "POST"
    }
  },
  "scaStatus": "finalised"
}
```

---

## Consent Information and Status

### Get Consent Information

#### AllPsd2 Consent
**Request:**
```http
GET /v3.1/consents/400ab141-b1b0-4920-bd57-9cee98ea3a2e
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
  "access": {
    "allPsd2": "allAccounts"
  },
  "recurringIndicator": true,
  "validUntil": "2020-12-31T23:59:59.000Z",
  "frequencyPerDay": 1,
  "combinedServiceIndicator": false,
  "lastActionDate": "2020-10-01T07:49:53.9230191",
  "consentStatus": "valid"
}
```

#### Explicit Consent
**Request:**
```http
GET /v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885
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
  "access": {
    "accounts": [
      {"iban": "GR0101718220007027000224226"},
      {"iban": "GR0101718220007052999999000"},
      {"maskedPan": "430589******6006"}
    ],
    "balances": [
      {"iban": "GR0101718220007027000224226"},
      {"maskedPan": "430589******6006"}
    ],
    "transactions": [
      {"iban": "GR0101718220007027000224226"},
      {"maskedPan": "430589******6006"}
    ]
  },
  "recurringIndicator": true,
  "validUntil": "2020-12-31T23:59:59.000Z",
  "frequencyPerDay": 1,
  "combinedServiceIndicator": false,
  "lastActionDate": "2020-10-01T07:55:03.7450281",
  "consentStatus": "received"
}
```

### Get Consent Status

#### AllPsd2 Consent
**Request:**
```http
GET /v3.1/consents/400ab141-b1b0-4920-bd57-9cee98ea3a2e/status
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
  "consentStatus": "expired"
}
```

#### Explicit Consent
**Request:**
```http
GET /v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/status
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
  "consentStatus": "received"
}
```

### Get Authorization Status (Explicit Consent Only)

**Request:**
```http
GET /v3.1/consents/9881137a-b159-451b-bdf3-ad57da454885/authorisations/7617a049-c6db-42d7-ac61-8871b849c23f
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

---

## Account Information Retrieval

### Get Accounts

#### AllPsd2 Consent (Basic Listing)
**Request:**
```http
GET /v3.1/accounts
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 400ab141-b1b0-4920-bd57-9cee98ea3a2e
```

**Response:**
```json
{
  "accounts": [
    {
      "iban": "GR0101718220007027000224226",
      "currency": "EUR",
      "status": "enabled"
    },
    {
      "iban": "GR0101718220007052999999000",
      "currency": "EUR",
      "status": "enabled"
    }
  ]
}
```

#### Explicit Consent (Detailed Information)
**Request:**
```http
GET /v3.1/accounts
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "accounts": [
    {
      "resourceId": "5684704b-88d9-4e91-97c8-9e9435686730",
      "iban": "GR0101718220007027000224226",
      "bban": "7027-000224-226",
      "currency": "EUR",
      "name": "ΛΟΓΑΡΙΑΣΜΟΣ ΠΕΙΡΑΙΩΣ",
      "displayName": "ΛΟΓΑΡΙΑΣΜΟΣ ΠΕΙΡΑΙΩΣ",
      "product": "ΤΑΜΙΕΥΤΗΡΙΟ -Κ-",
      "status": "enabled",
      "_links": {
        "balances": {
          "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730/balances",
          "verb": "GET"
        },
        "transactions": {
          "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730/transactions",
          "verb": "GET"
        }
      }
    },
    {
      "resourceId": "647603f8-6a25-46ff-ac7d-3b2dfadbbc5d",
      "iban": "GR0101718220007052999999000",
      "bban": "7052-999999-000",
      "currency": "EUR",
      "name": "ΑΠΟΤΑΜΙΕΥΤΙΚΟΣ WELCOME",
      "displayName": "ΑΠΟΤΑΜΙΕΥΤΙΚΟΣ WELCOME",
      "product": "ΑΠΟΤΑΜΙΕΥΤΙΚΟΣ WELCOME",
      "status": "enabled",
      "_links": {}
    }
  ]
}
```

### Get Account Details (Explicit Consent Only)

**Request:**
```http
GET /v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "resourceId": "5684704b-88d9-4e91-97c8-9e9435686730",
  "iban": "GR0101718220007027000224226",
  "currency": "EUR",
  "name": "Διαζευκτικός",
  "displayName": "ΛΟΓΑΡΙΑΣΜΟΣ ΠΕΙΡΑΙΩΣ",
  "ownerName": "Παπαδόπουλος, Ιωάννης, ΝΙΚΟΛΑΟΥ, AΒ987654",
  "product": "ΤΑΜΙΕΥΤΗΡΙΟ -Κ-",
  "status": "enabled",
  "_links": {
    "balances": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730/balances",
      "verb": "GET"
    },
    "transactions": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730/transactions",
      "verb": "GET"
    }
  }
}
```

### Get Account Balances (Explicit Consent Only)

**Request:**
```http
GET /v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730/balances
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "account": {
    "iban": "GR0101718220007027000224226",
    "currency": "EUR"
  },
  "balances": [
    {
      "balanceAmount": {
        "currency": "EUR",
        "amount": 13587.32
      },
      "balanceType": "authorised"
    },
    {
      "balanceAmount": {
        "currency": "EUR",
        "amount": 13587.32
      },
      "balanceType": "interimAvailable"
    }
  ]
}
```

### Get Account Transactions (Explicit Consent Only)

**Request:**
```http
GET /v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730/transactions?bookingStatus=booked&dateFrom=2018-01-01&dateTo=2018-12-31
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "account": {
    "iban": "GR0101718220007027000224226"
  },
  "transactions": {
    "booked": [
      {
        "transactionId": "11801287665@APS 0000002",
        "endToEndId": "2115102638458796",
        "bookingDate": "2018-01-02T00:00:00",
        "valueDate": "2018-01-02T00:00:00",
        "transactionAmount": {
          "currency": "EUR",
          "amount": 300
        },
        "additionalInformation": "APS-ΚΑΤΑΘ.ΜΕΤΡΗΤΩΝ\nEASYPAY KIOSK 211501",
        "purposeCode": "BKDF",
        "proprietaryBankTransactionCode": "572"
      },
      {
        "transactionId": "11801183542IIB010021457",
        "endToEndId": "IB10118505948769",
        "bookingDate": "2018-01-03T00:00:00",
        "valueDate": "2018-01-03T00:00:00",
        "transactionAmount": {
          "currency": "EUR",
          "amount": -150
        },
        "additionalInformation": "ΠΛΗΡΩΜΗ ΠΙΣΤΩΤΙΚΗΣ ΚΑΡΤΑΣ\n430589******6006",
        "purposeCode": "BKDF",
        "proprietaryBankTransactionCode": "040"
      }
    ],
    "_links": {
      "account": {
        "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/accounts/5684704b-88d9-4e91-97c8-9e9435686730",
        "verb": "GET"
      }
    }
  }
}
```

---

## Card Account Information

### Get Card Accounts

#### AllPsd2 Consent (Basic Listing)
**Request:**
```http
GET /v3.1/card-accounts
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 400ab141-b1b0-4920-bd57-9cee98ea3a2e
```

**Response:**
```json
{
  "cardAccounts": [
    {
      "maskedPan": "430589******6006",
      "currency": "EUR",
      "status": "enabled"
    }
  ]
}
```

#### Explicit Consent (Detailed Information)
**Request:**
```http
GET /v3.1/card-accounts
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "cardAccounts": [
    {
      "resourceId": "39bf0e8d-41be-4233-a1d3-38dda5662a49",
      "maskedPan": "430589******6006",
      "currency": "EUR",
      "name": "Primary",
      "displayName": "Panathinaikos FC Visa Classic",
      "product": "Panathinaikos FC Visa Classic",
      "status": "enabled",
      "creditLimit": {
        "currency": "EUR",
        "amount": 6000
      },
      "balances": [
        {
          "balanceAmount": {
            "currency": "EUR",
            "amount": 1023.22
          },
          "balanceType": "closingBooked",
          "referenceDate": "2017-10-30T00:00:00"
        },
        {
          "balanceAmount": {
            "amount": 6000
          },
          "balanceType": "authorised",
          "referenceDate": "2020-10-15T09:51:42.8067491+03:00"
        },
        {
          "balanceAmount": {
            "currency": "EUR",
            "amount": 4500.78
          },
          "balanceType": "interimAvailable",
          "referenceDate": "2020-10-15T09:51:42.8067519+03:00"
        },
        {
          "balanceAmount": {
            "currency": "EUR",
            "amount": 1048.76
          },
          "balanceType": "interimBooked",
          "referenceDate": "2020-10-15T09:51:42.8067527+03:00"
        }
      ],
      "_links": {
        "balances": {
          "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49/balances",
          "verb": "GET"
        },
        "transactions": {
          "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49/transactions",
          "verb": "GET"
        }
      }
    }
  ]
}
```

### Get Card Account Details (Explicit Consent Only)

**Request:**
```http
GET /v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "resourceId": "39bf0e8d-41be-4233-a1d3-38dda5662a49",
  "maskedPan": "430589******6006",
  "currency": "EUR",
  "name": "Primary",
  "displayName": "Panathinaikos FC Visa Classic",
  "ownerName": "ΓΕΩΡΓΙΟΣ ΓΕΩΡΓΙΟΥ",
  "product": "Panathinaikos FC Visa Classic",
  "status": "enabled",
  "creditLimit": {
    "currency": "EUR",
    "amount": 6000
  },
  "_links": {
    "balances": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49/balances",
      "verb": "GET"
    },
    "transactions": {
      "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49/transactions",
      "verb": "GET"
    }
  }
}
```

### Get Card Account Balances (Explicit Consent Only)

**Request:**
```http
GET /v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49/balances
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "cardAccount": {
    "maskedPan": "430589******6006",
    "currency": "EUR"
  },
  "balances": [
    {
      "balanceAmount": {
        "amount": 1023.22
      },
      "balanceType": "closingBooked"
    },
    {
      "balanceAmount": {
        "amount": 4500.78
      },
      "balanceType": "interimAvailable"
    },
    {
      "balanceAmount": {
        "currency": "EUR",
        "amount": 1048.76
      },
      "balanceType": "interimBooked"
    },
    {
      "balanceAmount": {
        "amount": 6000
      },
      "balanceType": "authorised"
    }
  ]
}
```

### Get Card Account Transactions (Explicit Consent Only)

**Request:**
```http
GET /v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49/transactions?bookingStatus=booked&dateFrom=2020-01-01&dateTo=2020-10-15
Authorization: Bearer [OAUTH_ACCESS_TOKEN]
Content-Type: application/json
PSU-IP-Address: [PSU_IP_ADDRESS]
X-Client-Certificate: [QWAC_PEM_CONTENT]
X-IBM-Client-ID: [CLIENT_ID]
X-Request-ID: [GUID]
Consent-ID: 9881137a-b159-451b-bdf3-ad57da454885
```

**Response:**
```json
{
  "cardAccount": {
    "maskedPan": "430589******6006"
  },
  "cardTransactions": {
    "booked": [
      {
        "cardTransactionId": "2",
        "transactionDate": "2020-10-15T00:00:00",
        "bookingDate": "2020-10-15T00:00:00",
        "transactionAmount": {
          "currency": "EUR",
          "amount": -85.35
        },
        "transactionDetails": "ΠΛΗΡΩΜΗ-ΕΥΧΑΡΙΣΤΟΥΜΕ",
        "proprietaryBankTransactionCode": "WIN"
      },
      {
        "cardTransactionId": "1",
        "transactionDate": "2020-10-10T00:00:00",
        "bookingDate": "2020-10-11T00:00:00",
        "transactionAmount": {
          "currency": "EUR",
          "amount": 70
        },
        "transactionDetails": "ΑΓΟΡΑ -ARGYRIOU NIKOLAOS    ATHENS     GR",
        "proprietaryBankTransactionCode": "POS"
      }
    ],
    "pending": [],
    "_links": {
      "cardAccount": {
        "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49",
        "verb": "GET"
      },
      "next": {
        "href": "https://api.rapidlink.piraeusbank.gr/pireausbank/production/psd2/v3.1/card-accounts/39bf0e8d-41be-4233-a1d3-38dda5662a49/transactions?bookingStatus=booked&dateFrom=2020-01-01&dateTo=2020-10-15&entryReferenceFrom=Ym9va2VkIG9sZAkwCTEzMjQ3MjE4Nzc5NjA2MDE0NQ==",
        "verb": "GET"
      }
    }
  }
}
```

---

## Important Implementation Notes

### Consent Status Values
- **valid**: Consent is active and ready for use
- **received**: Consent created but requires SCA
- **expired**: Consent has passed its validUntil date
- **rejected**: Consent was denied by PSU
- **revoked**: Consent was cancelled by PSU
- **terminated**: Consent was terminated by bank

### Balance Types
- **closingBooked**: Balance at end of previous day
- **interimAvailable**: Currently available balance
- **interimBooked**: Current booked balance
- **authorised**: Credit limit or authorized overdraft

### Transaction Query Parameters
- **bookingStatus**: `booked`, `pending`, or `both`
- **dateFrom**: Start date (YYYY-MM-DD format)
- **dateTo**: End date (YYYY-MM-DD format)
- **entryReferenceFrom**: Pagination parameter

### Resource IDs
- Account and card `resourceId` values change with each new consent
- Always retrieve fresh resource IDs after consent creation
- Use resource IDs for detailed balance and transaction requests

### Sandbox Testing
- **SCA Code**: Use `3288000` for all sandbox SCA authentication
- **Test Users**: UserA, UserB, UserC with password `123`
- **Certificates**: Not required in sandbox environment