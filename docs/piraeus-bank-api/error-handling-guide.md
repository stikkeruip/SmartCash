# Error Handling Guide

## Common Error Patterns

### Authentication Errors
- **api-002 (401)**: Token expired or invalid → Refresh token or re-authenticate
- **api-006 (440)**: Login timeout → Re-authenticate user
- **api-011 (401)**: SCA required → Initiate second factor authentication

### Authorization Errors  
- **api-019 (403)**: No SCA mechanism configured → User needs to set up 2FA
- **api-020 (403)**: No extrapin token → User needs SMS/mobile setup
- **api-021 (403)**: No OTP token → User needs physical OTP device

### Validation Errors
- **api-015 (412)**: Extrapin validation failed → Request new pin
- **api-022 (401)**: OTP validation failed → Retry with correct OTP
- **api-023 (403)**: Pin change needed → Guide user to change PIN

### Data Errors
- **api-003/004/005 (412)**: Date validation issues → Fix date parameters
- **api-008 (412)**: Page size too large → Reduce page size
- **api-029 (412)**: Card ID not found → Verify card exists

## Error Response Structure

```json
{
  "error": "api-002",
  "message": "Please get authorized first.",
  "status": 401,
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Retry Strategies

### Transient Errors (Retry)
- **440**: Login timeout
- **501**: Service temporarily unavailable

### Permanent Errors (Don't Retry)
- **400**: Bad request - fix parameters
- **403**: Forbidden - insufficient permissions
- **404**: Not found - resource doesn't exist
- **412**: Precondition failed - fix validation issues

## SCA Error Handling Flow

```
1. API Call → 401 (api-011) "SCA needed"
2. Check user SCA methods
3. If no methods → 403 (api-019) → Guide user to setup
4. Generate SCA token if needed
5. Validate SCA token
6. If validation fails → Handle specific error
7. Retry original API call
```