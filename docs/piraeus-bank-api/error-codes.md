# Piraeus Bank API Error Codes

This document provides a comprehensive reference for error codes returned by Piraeus Bank APIs (v1.1 and v1.2).

## Error Codes by API Endpoint

### Assets/Accounts API

| Path | Error Codes |
|------|-------------|
| `/` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/{accountId}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/{accountId}/transactions` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-008 (412), api-026 (501) |
| `/{iban}/info` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |

### Assets/Cards API

| Path | Error Codes |
|------|-------------|
| `/list` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/credit/list` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/debit/list` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/prepaid/list` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/{cardId}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |
| `/{cardId}/transactions` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |
| `/credit/{cardId}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |
| `/credit/{cardId}/transactions` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |
| `/credit/{cardId}/statements` | api-027 (501) |
| `/debit/{cardId}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |
| `/debit/{cardId}/transactions` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |
| `/prepaid/{cardId}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |
| `/prepaid/{cardId}/transactions` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501), api-029 (412) |

### Customer API

| Path | Error Codes |
|------|-------------|
| `/info` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-010 (412), api-026 (501) |

### Lookups API

| Path | Error Codes |
|------|-------------|
| `/toiban/{accountnumber}` | api-001 (400) |
| `/verifyiban/{iban}` | api-001 (400) |
| `/pop/list` | api-001 (400) |
| `/pop/{pointtypename}/list` | api-001 (400), api-024 (412) |
| `/countries/list` | api-001 (400), api-002 (401) |

### Security API

| Path | Error Codes |
|------|-------------|
| `/{tokentype}/generate/force` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-014 (401), api-017 (412), api-019 (403), api-026 (501) |
| `/{tokentype}/generate` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-014 (401), api-017 (412), api-019 (403), api-026 (501) |
| `/token/validate/{tokenvalue}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-015 (412), api-017 (412), api-018 (401), api-019 (403), api-020 (403), api-021 (403), api-022 (401), api-023 (403), api-025 (412), api-026 (501) |
| `/{tokentype}/validate/{tokenvalue}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-015 (412), api-017 (412), api-018 (401), api-019 (403), api-020 (403), api-021 (403), api-022 (401), api-023 (403), api-025 (412), api-026 (501) |

### Security/Approvals API

| Path | Error Codes |
|------|-------------|
| `/` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-019 (403) |
| `/count` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-019 (403) |
| `/{approvalKey}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-019 (403) |

### Transactions API

| Path | Error Codes |
|------|-------------|
| `/payroll` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501), api-028 (412) |
| `/payroll/validate` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-016 (412), api-019 (403), api-026 (501), api-028 (412) |
| `/payroll/execute/{SessionKey}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501) |
| `/payroll/history` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501) |
| `/payroll/{PaymentCode}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/bulkPayment` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501), api-028 (412) |
| `/bulkPayment/validate` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-016 (412), api-019 (403), api-026 (501), api-028 (412) |
| `/bulkPayment/execute/{SessionKey}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501) |
| `/bulkPayment/history` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501) |
| `/bulkPayment/{PaymentCode}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/transferToIban` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501) |
| `/transferToIban/validate` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-016 (412), api-019 (403), api-026 (501) |
| `/transferToIban/execute/{SessionKey}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501) |
| `/history/{input_filter}` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501) |
| `/{input_filter}` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501) |
| `/` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501) |
| `/{paymentOrderId}/details` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/{paymentOrderId}/history` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/creditTransfer` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501) |
| `/creditTransfer/validate` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-016 (412), api-019 (403), api-026 (501) |
| `/creditTransfer/execute/{SessionKey}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-013 (404), api-016 (412), api-019 (403), api-026 (501) |
| `/bulkPayment/prepare` | api-002 (401) |

### Transactions/Payments API

| Path | Error Codes |
|------|-------------|
| `/instant/{BeneficiaryAlias}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-019 (403), api-026 (501), api-030 (412) |
| `/instant/validate/{BeneficiaryAlias}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-019 (403), api-026 (501), api-030 (412) |
| `/instant/execute/{SessionKey}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-011 (401), api-019 (403), api-026 (501), api-030 (412) |
| `/{input_filter}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/codes` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/codes/{paymentCode}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/{paymentCode}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501), api-031 (412) |
| `/{paymentCode}/validate` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501), api-031 (412) |
| `/{paymentCode}/execute/{SessionKey}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |

### Transactions/Remittances API

| Path | Error Codes |
|------|-------------|
| `/` | api-001 (400), api-002 (401), api-003 (412), api-004 (412), api-005 (412), api-006 (440), api-007 (404), api-026 (501) |
| `/history/{input_filter}` | api-002 (401), api-026 (501) |
| `/delete/{Reference}` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-013 (404), api-026 (501) |
| `/delete/{Reference}/validate` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-026 (501) |
| `/delete/{Reference}/execute` | api-001 (400), api-002 (401), api-006 (440), api-007 (404), api-013 (404), api-026 (501) |
| `/advice` | api-002 (401), api-027 (501) |
| `/confirmation` | api-002 (401), api-027 (501) |

## Error Code Definitions

| Error Code | Description | HTTP Status | HTTP Description |
|------------|-------------|-------------|------------------|
| api-001 | - | 400 | Bad Request |
| api-002 | [...]. Please get authorized first. | 401 | Unauthorized |
| api-003 | Invalid fromDate | 412 | Precondition Failed |
| api-004 | Invalid toDate | 412 | Precondition Failed |
| api-005 | toDate Smaller Than fromDate | 412 | Precondition Failed |
| api-006 | - | 440 | Login Time-Out |
| api-007 | - | 404 | Not Found |
| api-008 | Maximum page size is [...], but [...] was requested | 412 | Precondition Failed |
| api-009 | - | 400 | Bad Request |
| api-010 | - | 412 | Precondition Failed |
| api-011 | Second factor authentication needed | 401 | Unauthorized |
| api-012 | Second factor authentication, not required right now | 400 | Bad Request |
| api-013 | Path [...] not found | 404 | Not Found |
| api-014 | Otp cannot be generated from api | 400 | Bad Request |
| api-015 | Extrapin validation failed | 412 | Precondition Failed |
| api-016 | Missing mass payment/payroll payload. File upload, failed | 412 | Precondition Failed |
| api-017 | Invalid token type: [...] | 412 | Precondition Failed |
| api-018 | - | 401 | Unauthorized |
| api-019 | User does not have second factor authentication mechanism configured | 403 | Forbidden |
| api-020 | User doesnt have extrapin token type | 403 | Forbidden |
| api-021 | User doesnt have OTP token type | 403 | Forbidden |
| api-022 | OTP validation failed | 401 | Unauthorized |
| api-023 | Otp validation failed. Reason: Pin Change Needed | 403 | Forbidden |
| api-024 | Unknown point type [...] | 412 | Precondition Failed |
| api-025 | Extrapin validation failed. Error: Unknown validation result | 412 | Precondition Failed |
| api-026 | - | 501 | Not Implemented |
| api-027 | This api, is not implemented in this version | 501 | No Permission Found For Route |
| api-028 | - | 412 | Precondition Failed |
| api-029 | cardId not found | 412 | Precondition Failed |
| api-030 | Customer is not registered for instant payment (Iris24/7) | 412 | Precondition Failed |
| api-031 | Payment code [...] is not valid. | 412 | Precondition Failed |
| api-999 | [default] | 400 | Bad Request |

## Notes

- Placeholders `[...]` in error messages represent dynamic values that will be filled with actual data at runtime
- HTTP status codes follow standard REST conventions
- Error codes are consistent across API versions (v1.1 and v1.2)