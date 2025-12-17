#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify image loading paths work correctly
"""
import os
import base64

def test_image_loading():
    """Test if images can be loaded from the expected path"""

    print("=" * 70)
    print("Testing Image Loading")
    print("=" * 70)

    # Expected path structure
    module_path = os.path.join('custom_addons', 'bike_shop_rental')
    img_path = os.path.join(module_path, 'static', 'img')

    print(f"\nModule path: {os.path.abspath(module_path)}")
    print(f"Image path: {os.path.abspath(img_path)}")
    print(f"Image path exists: {os.path.exists(img_path)}")

    images = [
        'city_bike.jpg',
        'mountain_bike.jpg',
        'road_bike.jpg',
        'electric_bike.jpg',
        'kids_bike.jpg',
        'default_bike.jpg',
    ]

    print("\n" + "-" * 70)
    print("Checking individual images:")
    print("-" * 70)

    for img_name in images:
        img_file_path = os.path.join(img_path, img_name)
        exists = os.path.exists(img_file_path)

        if exists:
            file_size = os.path.getsize(img_file_path)

            # Try to load and encode
            try:
                with open(img_file_path, 'rb') as f:
                    img_data = f.read()
                    encoded = base64.b64encode(img_data)
                    status = f"[OK] Size: {file_size:,} bytes, Encoded: {len(encoded):,} chars"
            except Exception as e:
                status = f"[ERROR] Failed to encode: {e}"
        else:
            status = "[MISSING] File not found"

        print(f"{img_name:25s} {status}")

    print("\n" + "=" * 70)

if __name__ == '__main__':
    test_image_loading()
