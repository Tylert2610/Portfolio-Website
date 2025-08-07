#!/usr/bin/env python3
"""
Script to create sample categories for testing the blog functionality.
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Category
from slugify import slugify


def create_sample_categories():
    """Create sample categories in the database."""
    db = SessionLocal()

    try:
        # Check if categories already exist
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print(
                f"Found {existing_categories} existing categories. Skipping creation."
            )
            return

        # Sample categories
        sample_categories = [
            {
                "name": "Web Development",
                "slug": "web-development",
            },
            {
                "name": "Technology Trends",
                "slug": "technology-trends",
            },
            {
                "name": "Best Practices",
                "slug": "best-practices",
            },
            {
                "name": "Tutorials",
                "slug": "tutorials",
            },
            {
                "name": "Career Development",
                "slug": "career-development",
            },
        ]

        # Create categories
        for category_data in sample_categories:
            category = Category(**category_data)
            db.add(category)

        db.commit()
        print(f"Successfully created {len(sample_categories)} sample categories:")

        for category_data in sample_categories:
            print(f"  - {category_data['name']} ({category_data['slug']})")

    except Exception as e:
        print(f"Error creating sample categories: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_categories()
