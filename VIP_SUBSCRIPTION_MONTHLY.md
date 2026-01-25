# Monthly VIP Subscription System

## Overview
The bot now has a monthly VIP subscription system with automatic expiration after 30 days. Users need to renew their VIP subscription every month.

## Changes Made

### 1. Database (`database.py`)

#### Schema Updates
- Added `vip_expires_at TIMESTAMP` column to the users table
- Migration automatically adds the column to existing databases

#### New/Updated Methods

**`set_vip_status(user_id, is_vip, days=30)`**
- Now accepts a `days` parameter (default: 30 days)
- Sets VIP status with expiration date 30 days from now
- When removing VIP, clears the expiration date

**`get_vip_expiration(user_id)`**
- Returns the VIP expiration datetime for a user
- Returns None if user has no expiration (lifetime VIP or not VIP)

**`get_vip_days_remaining(user_id)`**
- Returns number of days remaining for VIP subscription
- Returns None if no expiration date set
- Returns 0 if already expired

**`check_and_expire_vips()`**
- Checks all VIP users and expires those past their expiration date
- Returns the count of expired subscriptions
- Runs automatically via background job

### 2. Bot (`bot.py`)

#### Profile Display
- Shows "VIP Member (X days remaining)" when VIP is active
- Shows "VIP Member" for old users without expiration (grandfathered)

#### VIP Command (`/vip`)
Updated to show different messages based on VIP status:

**Active VIP with days remaining:**
- Shows days remaining
- Shows "Renew VIP" button
- Lists all VIP benefits

**Expired VIP:**
- Notifies user that subscription expired
- Shows "Buy VIP" button to renew
- Lists all VIP benefits

**Lifetime VIP (grandfathered):**
- Shows "lifetime VIP status" message
- No purchase/renewal button needed

**Non-VIP users:**
- Shows all VIP benefits
- Mentions it's a monthly subscription
- Shows "Buy VIP" button

#### Payment Flow
**`successful_payment()`**
- Now sets VIP expiration to 30 days from purchase
- Updated confirmation message to mention 30-day period
- Tells users to use `/vip` to check subscription status

#### Background Task
- Added automatic daily check for expired VIP subscriptions
- Runs every 24 hours starting 10 seconds after bot starts
- Logs how many VIP subscriptions were expired

### 3. Translations (`translations.py`)

Added new translation keys:
- `vip_expires_in` - Shows remaining days
- `vip_expired` - Expired notification
- `vip_lifetime` - Lifetime VIP message

All available in English, Russian, and Armenian.

## Backward Compatibility

**Existing VIP Users:**
The system handles existing VIP users gracefully:
- Users who purchased VIP before this update have `vip_expires_at = NULL`
- These users are treated as "lifetime VIP" and never expire
- They won't see renewal prompts or expiration dates
- Future purchases will use the new 30-day expiration system

## How It Works

### Purchase Flow
1. User clicks "Buy VIP" button in `/vip` command
2. User completes Telegram Stars payment
3. Bot grants VIP status for 30 days (stores expiration date)
4. User receives confirmation with expiration info

### Renewal Flow
1. Active VIP users see "Renew VIP" button in `/vip` command
2. They can renew anytime (extends expiration by 30 days from purchase)
3. Expired users see "Buy VIP" button to reactivate

### Expiration Check
1. Background job runs every 24 hours
2. Checks all VIP users with `vip_expires_at < now()`
3. Sets `is_vip = 0` for expired users
4. Logs the count of expired subscriptions

### User Experience
- Users can check remaining days in `/profile` or `/vip`
- Users can renew before expiration
- Users are notified when expired (via `/vip` command)
- All existing features (gender selection, partner info) continue to work

## Testing

To test the monthly subscription system:

1. **New VIP Purchase:**
   ```
   /vip → Click "Buy VIP" → Complete payment
   Check profile: should show "VIP Member (30 days remaining)"
   ```

2. **Check Expiration:**
   ```
   /profile → Should show days remaining
   /vip → Should show days remaining + renewal button
   ```

3. **Manual Expiration Test:**
   In database, set `vip_expires_at` to a past date:
   ```sql
   UPDATE users SET vip_expires_at = datetime('now', '-1 day') WHERE user_id = YOUR_ID;
   ```
   Then run the bot and trigger the check or wait for the daily job.

4. **Renewal Test:**
   While VIP is active, click "Renew VIP" button in `/vip`
   Expiration should extend by 30 days from purchase time

## Configuration

- **Expiration Duration:** 30 days (hardcoded in `set_vip_status()`)
- **Check Frequency:** Every 24 hours (86400 seconds)
- **First Check:** 10 seconds after bot starts

## Notes

- VIP price remains unchanged (set in `config.py` as `VIP_PRICE_STARS`)
- Payment is one-time for 30 days (not auto-renewing subscription)
- Users must manually purchase/renew each month
- Telegram Stars currency is used (XTR)
