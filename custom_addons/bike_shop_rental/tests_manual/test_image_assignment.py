#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test manuel pour l'attribution automatique d'images aux vélos.

Ce script teste que les images sont correctement assignées selon les modèles/catégories.

Usage:
    python test_image_assignment.py

Note: Ce script est pour test manuel. Les tests automatiques devraient être dans tests/
"""

def test_model_to_image_mapping():
    """Teste le mapping des modèles vers les images"""

    test_cases = [
        # (model_name, category_name, expected_image)
        ("City Commuter", "Vélo de Ville", "city_bike.jpg"),
        ("Mountain X5", "VTT", "mountain_bike.jpg"),
        ("Road Pro", "Vélo de Route", "road_bike.jpg"),
        ("E-Bike Urban", "Vélo Électrique", "electric_bike.jpg"),
        ("Kids 20 pouces", "Vélo Enfant", "kids_bike.jpg"),
        ("Unknown Model", "Unknown Category", "default_bike.jpg"),

        # Test avec variations
        ("MTB Racer", "", "mountain_bike.jpg"),
        ("Urban Bike", "", "city_bike.jpg"),
        ("Electric Speed", "", "electric_bike.jpg"),
        ("", "VTT", "mountain_bike.jpg"),
        ("", "Route", "road_bike.jpg"),
    ]

    print("=" * 70)
    print("TEST: Model to Image Mapping")
    print("=" * 70)

    # Simuler la logique de mapping (copié depuis bike.py)
    # L'ordre est important : les plus spécifiques en premier
    image_mapping = [
        ('e-bike', 'electric_bike.jpg'),
        ('ebike', 'electric_bike.jpg'),
        ('electric', 'electric_bike.jpg'),
        ('électrique', 'electric_bike.jpg'),
        ('mountain', 'mountain_bike.jpg'),
        ('mtb', 'mountain_bike.jpg'),
        ('vtt', 'mountain_bike.jpg'),
        ('road', 'road_bike.jpg'),
        ('route', 'road_bike.jpg'),
        ('kids', 'kids_bike.jpg'),
        ('enfant', 'kids_bike.jpg'),
        ('junior', 'kids_bike.jpg'),
        ('city', 'city_bike.jpg'),
        ('ville', 'city_bike.jpg'),
        ('commuter', 'city_bike.jpg'),
        ('urbain', 'city_bike.jpg'),
        ('urban', 'city_bike.jpg'),
    ]

    def get_expected_image(model_name, category_name):
        # Cherche d'abord dans le modèle
        model_lower = (model_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in model_lower:
                return image_file

        # Sinon dans la catégorie
        category_lower = (category_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in category_lower:
                return image_file

        return 'default_bike.jpg'

    passed = 0
    failed = 0

    for model_name, category_name, expected in test_cases:
        result = get_expected_image(model_name, category_name)
        status = "[PASS]" if result == expected else "[FAIL]"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} | Model: {model_name:20s} | Category: {category_name:20s} | Expected: {expected:20s} | Got: {result:20s}")

    print("-" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)

    return failed == 0


def test_demo_bikes():
    """Teste que les vélos de démo reçoivent les bonnes images"""

    demo_bikes = [
        ("TREK City 2023", "City Commuter", "Vélo de Ville", "city_bike.jpg"),
        ("SPECIALIZED Mountain X5", "Mountain X5", "VTT", "mountain_bike.jpg"),
        ("GIANT Road Pro", "Road Pro", "Vélo de Route", "road_bike.jpg"),
        ("BOSCH E-Bike Urban", "E-Bike Urban", "Vélo Électrique", "electric_bike.jpg"),
        ("DECATHLON Kids 20\"", "Kids 20 pouces", "Vélo Enfant", "kids_bike.jpg"),
        ("TREK Mountain Pro", "Mountain Pro", "VTT", "mountain_bike.jpg"),
    ]

    print("\n" + "=" * 70)
    print("TEST: Demo Bikes Image Assignment")
    print("=" * 70)

    image_mapping = [
        ('e-bike', 'electric_bike.jpg'),
        ('ebike', 'electric_bike.jpg'),
        ('electric', 'electric_bike.jpg'),
        ('électrique', 'electric_bike.jpg'),
        ('mountain', 'mountain_bike.jpg'),
        ('mtb', 'mountain_bike.jpg'),
        ('vtt', 'mountain_bike.jpg'),
        ('road', 'road_bike.jpg'),
        ('route', 'road_bike.jpg'),
        ('kids', 'kids_bike.jpg'),
        ('enfant', 'kids_bike.jpg'),
        ('junior', 'kids_bike.jpg'),
        ('city', 'city_bike.jpg'),
        ('ville', 'city_bike.jpg'),
        ('commuter', 'city_bike.jpg'),
        ('urbain', 'city_bike.jpg'),
        ('urban', 'city_bike.jpg'),
    ]

    def get_image(model_name, category_name):
        model_lower = (model_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in model_lower:
                return image_file

        category_lower = (category_name or '').lower()
        for keyword, image_file in image_mapping:
            if keyword in category_lower:
                return image_file

        return 'default_bike.jpg'

    passed = 0
    failed = 0

    for name, model, category, expected in demo_bikes:
        result = get_image(model, category)
        status = "[PASS]" if result == expected else "[FAIL]"

        if result == expected:
            passed += 1
        else:
            failed += 1

        print(f"{status} | {name:30s} -> {expected}")

    print("-" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(demo_bikes)} tests")
    print("=" * 70)

    return failed == 0


if __name__ == '__main__':
    print("\nTesting Automatic Image Assignment for Bikes\n")

    test1_passed = test_model_to_image_mapping()
    test2_passed = test_demo_bikes()

    print("\n" + "=" * 70)
    if test1_passed and test2_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
    print("=" * 70 + "\n")
