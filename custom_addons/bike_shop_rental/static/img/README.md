# Bike Images

This folder contains default images for bikes based on their type/category.

## Current Images

- `city_bike.jpg` - For city/urban/commuter bikes
- `mountain_bike.jpg` - For mountain/MTB/VTT bikes
- `road_bike.jpg` - For road/route bikes
- `electric_bike.jpg` - For electric/e-bikes/électrique bikes
- `kids_bike.jpg` - For kids/enfant/junior bikes
- `default_bike.jpg` - Default fallback image for unmatched types

## How It Works

The system automatically assigns images to bikes based on keywords in the **model name** or **category name**:

### Model-based Assignment (Priority 1)
When you create or edit a bike, if the model name contains certain keywords, the corresponding image is assigned:

- Model contains "mountain", "mtb", "vtt" → `mountain_bike.jpg`
- Model contains "road", "route" → `road_bike.jpg`
- Model contains "city", "ville", "commuter", "urban", "urbain" → `city_bike.jpg`
- Model contains "e-bike", "electric", "électrique", "ebike" → `electric_bike.jpg`
- Model contains "kids", "enfant", "junior" → `kids_bike.jpg`

### Category-based Assignment (Priority 2)
If no keyword is found in the model name, the system looks at the category name using the same keywords.

### Manual Override
You can always manually upload a custom image for any bike. The automatic assignment only applies when:
1. Creating a new bike without an image
2. Changing the model/category on a bike that has no image

## Replacing Placeholder Images

These are placeholder images. To use real bike photos:

1. Replace each `.jpg` file with your own images
2. Keep the same filenames
3. Recommended image specs:
   - Format: JPG or PNG
   - Size: 800x600 pixels (4:3 ratio)
   - File size: < 500KB for better performance

## Examples

**Demo Data:**
- "TREK City 2023" with model "City Commuter" → `city_bike.jpg`
- "SPECIALIZED Mountain X5" with model "Mountain X5" → `mountain_bike.jpg`
- "GIANT Road Pro" with model "Road Pro" → `road_bike.jpg`
- "BOSCH E-Bike Urban" with model "E-Bike Urban" → `electric_bike.jpg`
- "DECATHLON Kids 20"" with model "Kids 20 pouces" → `kids_bike.jpg`

## Technical Details

The image assignment is handled in the `bike.bike` model via:
- `_get_default_image_for_model()` - Maps keywords to image files
- `_load_default_image()` - Loads and encodes images as base64
- `_onchange_model_assign_image()` - Triggers on model/category change
- `create()` - Assigns images on record creation
