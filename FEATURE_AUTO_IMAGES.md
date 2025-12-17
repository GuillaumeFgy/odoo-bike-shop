# Feature: Automatic Image Assignment for Bikes

## Overview

The bike rental module now automatically assigns images to bikes based on their model name or category. This feature eliminates the need to manually upload an image for every bike, while still allowing manual overrides when needed.

## How It Works

### Priority System

The system checks keywords in this order:
1. **Model name** (highest priority)
2. **Category name** (fallback)
3. **Default image** (if no match)

### Keyword Mapping

The system uses an ordered list of keywords to match bikes to images. **Order matters** - more specific keywords are checked first:

| Priority | Keywords | Image File |
|----------|----------|------------|
| 1 | e-bike, ebike, electric, électrique | electric_bike.jpg |
| 2 | mountain, mtb, vtt | mountain_bike.jpg |
| 3 | road, route | road_bike.jpg |
| 4 | kids, enfant, junior | kids_bike.jpg |
| 5 | city, ville, commuter, urban, urbain | city_bike.jpg |
| 6 | (no match) | default_bike.jpg |

### Examples

- **"City Commuter"** → `city_bike.jpg` (matches "city")
- **"Mountain X5"** → `mountain_bike.jpg` (matches "mountain")
- **"E-Bike Urban"** → `electric_bike.jpg` (matches "e-bike" before "urban")
- **"Road Pro"** → `road_bike.jpg` (matches "road")
- **"Kids 20 pouces"** → `kids_bike.jpg` (matches "kids")

## Technical Implementation

### Modified Files

1. **`models/bike.py`**
   - Added `_get_default_image_for_model()` - keyword to image mapping
   - Added `_load_default_image()` - loads images from static/img folder
   - Added `_onchange_model_assign_image()` - triggers on model/category change
   - Modified `create()` - assigns images when creating new bikes

2. **`static/img/`** (new folder)
   - Contains 6 placeholder images (400x300 px, colored backgrounds)
   - `city_bike.jpg` - Blue
   - `mountain_bike.jpg` - Green
   - `road_bike.jpg` - Red
   - `electric_bike.jpg` - Orange
   - `kids_bike.jpg` - Purple
   - `default_bike.jpg` - Gray

3. **`__manifest__.py`**
   - Version bumped from 19.0.1.0.0 to 19.0.1.1.0
   - Added feature to description

### Code Highlights

```python
@api.onchange('model', 'category_id')
def _onchange_model_assign_image(self):
    """Automatically assign image when model/category changes"""
    if self.image and self._origin.id:
        return  # Don't replace existing images

    if self.model or self.category_id:
        category_name = self.category_id.name if self.category_id else ''
        default_image = self._get_default_image_for_model(self.model, category_name)
        if default_image:
            self.image = default_image
```

## When Images Are Assigned

### Automatically
1. **Creating a new bike** via UI or API (if no image provided)
2. **Changing the model field** (if bike has no image)
3. **Changing the category** (if bike has no image)

### Manual Override
- Images are **NOT** replaced if:
  - The bike already has an image
  - User manually uploads a custom image

## Usage

### For End Users

1. **Create a new bike**:
   - Fill in the model name (e.g., "Mountain Racer")
   - Select the category (e.g., "VTT")
   - **Image is assigned automatically!**

2. **Edit existing bike**:
   - Change the model name
   - If bike has no image, new image is assigned automatically
   - If bike has an image, it stays unchanged

3. **Manual override**:
   - Click on the image field
   - Upload your custom photo
   - System won't replace it anymore

### For Administrators

1. **Replace placeholder images**:
   ```bash
   cd custom_addons/bike_shop_rental/static/img/
   # Replace the .jpg files with real bike photos
   # Keep the same filenames!
   ```

2. **Recommended image specs**:
   - Format: JPG or PNG
   - Size: 800x600 pixels (4:3 ratio)
   - File size: < 500KB for performance

3. **Add new categories**:
   - Edit `bike.py` → `_get_default_image_for_model()`
   - Add new keywords to the mapping list
   - Create corresponding image in `static/img/`

## Testing

A comprehensive test suite is available:

```bash
python custom_addons/bike_shop_rental/tests_manual/test_image_assignment.py
```

### Test Results (All Passing)
```
TEST: Model to Image Mapping
[PASS] City Commuter → city_bike.jpg
[PASS] Mountain X5 → mountain_bike.jpg
[PASS] Road Pro → road_bike.jpg
[PASS] E-Bike Urban → electric_bike.jpg
[PASS] Kids 20 pouces → kids_bike.jpg
[PASS] Unknown Model → default_bike.jpg
... and 5 more tests

TEST: Demo Bikes Image Assignment
[PASS] TREK City 2023 → city_bike.jpg
[PASS] SPECIALIZED Mountain X5 → mountain_bike.jpg
[PASS] GIANT Road Pro → road_bike.jpg
[PASS] BOSCH E-Bike Urban → electric_bike.jpg
[PASS] DECATHLON Kids 20" → kids_bike.jpg
[PASS] TREK Mountain Pro → mountain_bike.jpg

Results: 17/17 tests passed
```

## Benefits

### For Users
- ✅ **Faster data entry** - No need to upload images for every bike
- ✅ **Consistent visuals** - All bikes of same type have similar images
- ✅ **Flexibility** - Can still use custom images when needed

### For Developers
- ✅ **Clean code** - Well-documented, follows Odoo conventions
- ✅ **Extensible** - Easy to add new categories/keywords
- ✅ **Tested** - Comprehensive test coverage

### For Presentation
- ✅ **Professional appearance** - All demo bikes have images
- ✅ **Shows technical skill** - Demonstrates Odoo development best practices
- ✅ **Practical feature** - Solves a real usability problem

## Upgrade Instructions

To upgrade an existing installation:

1. **Update the module**:
   ```bash
   # In Odoo
   Apps → Bike Shop - Rental Management → Upgrade
   ```

2. **Existing bikes**:
   - Bikes without images will get them automatically when:
     - You edit the bike and save
     - You change the model or category field

3. **Bulk update** (optional):
   - Go to: Bike Shop → Location → Vélos
   - Select all bikes without images
   - Edit → Change any field → Save
   - Images will be assigned automatically

## Future Enhancements

Possible improvements for future versions:

1. **Admin configuration** - UI to manage keyword mappings
2. **Multiple images** - Support for image galleries per bike
3. **External sources** - Fetch images from manufacturer websites
4. **AI matching** - Use machine learning for better image selection
5. **Batch import** - Upload multiple images at once with auto-matching

## Support

- **Documentation**: See `static/img/README.md` for image guidelines
- **Tests**: See `tests_manual/test_image_assignment.py`
- **Issues**: Report bugs on GitHub

---

**Version**: 19.0.1.1.0
**Date**: December 17, 2025
**Status**: Production Ready ✅
