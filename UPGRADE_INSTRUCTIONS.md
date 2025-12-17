# How to Upgrade and Test Automatic Image Assignment

## Step 1: Upgrade the Module in Odoo

### Option A: Through the UI (Recommended)

1. **Start Odoo** (if not already running)
   ```bash
   # If using Docker:
   docker-compose up -d

   # If manual installation:
   ./odoo/odoo-bin -c odoo.conf
   ```

2. **Enable Developer Mode**
   - Go to **Settings**
   - Scroll down and click **"Activate the developer mode"** (at the bottom)

3. **Update Apps List**
   - Go to **Apps**
   - Click the **⋮** (three dots menu) at the top
   - Click **"Update Apps List"**
   - Click **"Update"** in the confirmation dialog

4. **Upgrade the Module**
   - In **Apps**, remove the "Apps" filter to see all modules
   - Search for: **"Bike Shop - Rental"**
   - Click the **⋮** (three dots) on the module card
   - Click **"Upgrade"**
   - Wait for the upgrade to complete (~30 seconds)

### Option B: Through Command Line

```bash
# Stop Odoo first
docker-compose down   # or Ctrl+C if running manually

# Upgrade the module
docker-compose run --rm web odoo -u bike_shop_rental -d bike_shop --stop-after-init

# Or if manual installation:
./odoo/odoo-bin -c odoo.conf -u bike_shop_rental -d bike_shop --stop-after-init

# Restart Odoo
docker-compose up -d   # or restart manually
```

## Step 2: Test the Automatic Image Assignment

### Test 1: Create a New Bike

1. Go to **Bike Shop → Location → Vélos**
2. Click **Create**
3. Fill in:
   - **Name**: Test Mountain Bike
   - **Category**: VTT (or Mountain)
   - **Model**: Mountain Test
4. **Save** the record
5. **Expected Result**: Image should appear automatically (green mountain bike)

### Test 2: Use the Manual Button

1. Open any existing bike (e.g., "TREK City 2023")
2. Click the **"Assigner Image Auto"** button in the header
3. **Expected Result**: Image should appear based on the model/category

### Test 3: Bulk Assignment

1. Go to **Bike Shop → Location → Vélos**
2. Switch to **List View** (if not already)
3. **Select multiple bikes** (checkboxes on the left)
4. Click **Action → Assigner Images Automatiques**
5. **Expected Result**: All selected bikes get appropriate images

### Test 4: Test Onchange (New Bikes Only)

1. Create a new bike
2. Start typing in the **Model** field: "City"
3. The image should update as you type/select
4. Change to "Mountain" → image should change to mountain bike
5. Change to "E-Bike" → image should change to electric bike

## Step 3: Verify Images Are Working

### Check Image Files

Run this test script to verify images are loaded:
```bash
python test_image_loading.py
```

Expected output:
```
city_bike.jpg             [OK] Size: 4,855 bytes
mountain_bike.jpg         [OK] Size: 6,190 bytes
road_bike.jpg             [OK] Size: 5,669 bytes
electric_bike.jpg         [OK] Size: 4,267 bytes
kids_bike.jpg             [OK] Size: 5,119 bytes
default_bike.jpg          [OK] Size: 3,472 bytes
```

### Check in Odoo Logs

If images aren't appearing, check Odoo logs for errors:
```bash
# Docker:
docker-compose logs -f web | grep -i "image\|bike\|error"

# Manual:
# Check the console where Odoo is running
```

## Troubleshooting

### Images Still Not Appearing?

**Problem**: Button doesn't work or images don't assign

**Solutions**:

1. **Clear Browser Cache**
   - Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

2. **Check Developer Mode is ON**
   - Settings → Make sure "Developer Mode" badge appears

3. **Restart Odoo**
   ```bash
   docker-compose restart web
   # or restart manually
   ```

4. **Check File Permissions**
   ```bash
   # Make sure images are readable
   ls -la custom_addons/bike_shop_rental/static/img/
   chmod 644 custom_addons/bike_shop_rental/static/img/*.jpg
   ```

5. **Reinstall Module** (nuclear option)
   ```bash
   # This will reset demo data!
   # Apps → Bike Shop - Rental → Uninstall
   # Then reinstall
   ```

### Onchange Not Working?

The `@api.onchange` only works when:
- Creating NEW bikes through the UI
- Manually changing the model/category field

For EXISTING bikes, use the **"Assigner Image Auto"** button instead.

### Python Errors?

If you see Python errors in logs:

1. Check imports are correct:
   ```python
   import base64
   import os
   ```

2. Verify module structure:
   ```
   bike_shop_rental/
   ├── static/
   │   └── img/
   │       ├── city_bike.jpg
   │       ├── mountain_bike.jpg
   │       └── ...
   ```

## Expected Behavior

### What SHOULD Happen

- ✅ New bikes get images automatically when created
- ✅ Button "Assigner Image Auto" assigns images to existing bikes
- ✅ Bulk action works on multiple selected bikes
- ✅ Onchange updates image when typing model name (new bikes only)
- ✅ Manual images are NOT overwritten

### What Should NOT Happen

- ❌ Existing images should NOT be replaced automatically
- ❌ Shouldn't see any Python errors in logs
- ❌ Images shouldn't disappear after saving

## Next Steps

Once images are working:

1. ✅ Test creating bikes with different models
2. ✅ Verify all demo bikes have images
3. ✅ Replace placeholder images with real photos (optional)
4. ✅ Prepare for presentation demo

## Support

If issues persist:

1. Check `test_image_loading.py` output
2. Review Odoo logs for errors
3. Verify module version is 19.0.1.1.0 (Apps → Bike Shop - Rental)
4. Take screenshot of any errors and share them

---

**Module Version**: 19.0.1.1.0
**Feature**: Automatic Image Assignment
**Status**: Testing Phase
