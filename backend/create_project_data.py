#!/usr/bin/env python3
"""
Script to migrate static project and experience data from frontend to database.
This script reads the static data files and inserts them into the new database tables.
"""

import sys
import os
import argparse
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import Project, Experience

# Static project data from frontend/src/data/projects.ts
STATIC_PROJECTS = [
    {
        "title": "Car Modification Planning Tool",
        "description": "Full-stack web application enabling automotive enthusiasts to manage vehicle modification projects. Features user authentication, detailed build lists, part tracking with specifications, and responsive design.",
        "image": "",
        "technologies": [
            "Python",
            "TypeScript",
            "Tailwind CSS",
            "FastAPI",
            "React",
            "PostgreSQL",
            "Docker",
        ],
        "github_url": "https://github.com/Tylert2610/CarModPicker-Frontend",
        "live_url": None,
        "featured": True,
    },
    {
        "title": "Car Modification Planning Tool - Backend",
        "description": "Python FastAPI backend providing RESTful APIs for the car modification planning tool. Features PostgreSQL database, authentication, and comprehensive API endpoints.",
        "image": "",
        "technologies": [
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Docker",
            "SQLAlchemy",
            "Pydantic",
        ],
        "github_url": "https://github.com/Tylert2610/CarModPicker-Backend",
        "live_url": None,
        "featured": False,
    },
    {
        "title": "Inventory Tracking System",
        "description": "Full-stack application for tracking lab device checkout status across multiple platforms. Built for Verkada tech support team with web, Android, and iOS support.",
        "image": "",
        "technologies": ["Dart", "Flutter", "Firebase", "Python", "Git", "NoSQL"],
        "github_url": "https://github.com/Tylert2610/WebbPulse-Inventory-Management",
        "live_url": "webbpulse.com",
        "featured": True,
    },
    {
        "title": "Portfolio Website",
        "description": "Modern, responsive portfolio website built with React and TypeScript, featuring smooth animations, dark theme, and SEO optimization.",
        "image": "",
        "technologies": ["React", "TypeScript", "Tailwind CSS", "Vite"],
        "github_url": "https://github.com/Tylert2610/Portfolio-Website",
        "live_url": None,
        "featured": True,
    },
    {
        "title": "Internal Automation Tools",
        "description": "Collection of Python scripts and tools developed for Verkada support team to automate repetitive tasks and improve efficiency.",
        "image": "",
        "technologies": ["Python", "SQL", "Bash", "Datadog", "AWS"],
        "github_url": None,
        "live_url": None,
        "featured": False,
    },
    {
        "title": "Custom Monitoring & Analytics Dashboards",
        "description": "Engineered comprehensive monitoring solutions and analytics dashboards for engineering operations teams. Built performance metrics tracking, and real-time visibility tools to streamline incident response and improve system reliability.",
        "image": "",
        "technologies": ["Datadog", "SQL", "Metabase", "AWS"],
        "github_url": None,
        "live_url": None,
        "featured": False,
    },
    {
        "title": "HelpVerkada Web Crawler",
        "description": "Python-based web crawler designed to automate data collection and analysis for Verkada support operations. Streamlines information gathering processes.",
        "image": "",
        "technologies": ["Python", "Web Scraping", "Automation", "Data Processing"],
        "github_url": "https://github.com/Tylert2610/HelpVerkadaWebCrawler",
        "live_url": None,
        "featured": False,
    },
]

# Static experience data from frontend/src/data/experience.ts
STATIC_EXPERIENCE = [
    {
        "title": "Escalations Engineer",
        "company": "Verkada",
        "location": "San Mateo, CA",
        "period": "Jul 2024 - Present",
        "start_date": "2024-07-01",
        "end_date": None,
        "description": "Leading critical incident resolution and technical troubleshooting while developing internal tools and automation solutions to improve team efficiency.",
        "technologies": [
            "Python",
            "SQL",
            "Bash",
            "Datadog",
            "AWS",
            "GCP",
            "Azure",
            "Docker",
        ],
        "achievements": [
            "Developed and deployed internal tools using Python and SQL to automate repetitive tasks",
            "Built custom monitoring solutions and dashboards to improve incident response times",
            "Collaborated with development teams to identify and resolve complex system issues",
            "Mentored junior engineers on technical troubleshooting and automation best practices",
            "Proactively identified system vulnerabilities and implemented performance optimizations",
        ],
    },
    {
        "title": "Senior Technical Support Engineer",
        "company": "Verkada",
        "location": "San Mateo, CA",
        "period": "Jul 2022 - Jul 2024",
        "start_date": "2022-07-01",
        "end_date": "2024-07-01",
        "description": "Provided technical support for enterprise customers while developing automation scripts and tools to streamline support processes.",
        "technologies": [
            "Python",
            "SQL",
            "Bash",
            "Wireshark",
            "Active Directory",
            "Salesforce",
        ],
        "achievements": [
            "Built automation scripts in Python to reduce manual troubleshooting time by 60%",
            "Developed internal tools for inventory management and device tracking",
            "Submitted detailed bug reports and collaborated with engineering teams on solutions",
            "Handled escalated accounts for Fortune 500 companies and strategic customers",
            "Created comprehensive documentation for complex technical procedures",
        ],
    },
]


def migrate_projects(db: Session):
    """Migrate static project data to database."""
    print("Migrating projects...")

    for project_data in STATIC_PROJECTS:
        # Check if project already exists
        existing_project = (
            db.query(Project).filter(Project.title == project_data["title"]).first()
        )

        if existing_project:
            print(f"Project '{project_data['title']}' already exists, skipping...")
            continue

        # Projects don't have start_date/end_date fields

        project = Project(**project_data)
        db.add(project)
        print(f"Added project: {project_data['title']}")

    db.commit()
    print(f"Successfully migrated {len(STATIC_PROJECTS)} projects")


def migrate_experience(db: Session):
    """Migrate static experience data to database."""
    print("Migrating experience entries...")

    for experience_data in STATIC_EXPERIENCE:
        # Check if experience entry already exists
        existing_experience = (
            db.query(Experience)
            .filter(
                Experience.title == experience_data["title"],
                Experience.company == experience_data["company"],
            )
            .first()
        )

        if existing_experience:
            print(f"Experience '{experience_data['title']}' at '{experience_data['company']}' already exists, skipping...")
            continue

        # Convert date strings to date objects
        if experience_data["start_date"]:
            experience_data["start_date"] = datetime.strptime(
                experience_data["start_date"], "%Y-%m-%d"
            ).date()
        if experience_data["end_date"]:
            experience_data["end_date"] = datetime.strptime(
                experience_data["end_date"], "%Y-%m-%d"
            ).date()

        experience = Experience(**experience_data)
        db.add(experience)
        print(
            f"Added experience: {experience_data['title']} at {experience_data['company']}"
        )

    db.commit()
    print(f"Successfully migrated {len(STATIC_EXPERIENCE)} experience entries")



def main(SessionLocal):
    """Main migration function."""
    print("Starting static data migration...")

    db = SessionLocal()
    try:
        # Migrate projects
        migrate_projects(db)

        # Migrate experience
        migrate_experience(db)

        print("Migration completed successfully!")

    except Exception as e:
        print(f"Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    parser = argparse.ArgumentParser(description="Migrate static project and experience data to the database.")
    parser.add_argument("--db-url", help="Override the database URL")
    args = parser.parse_args()

    SessionLocalToUse = SessionLocal
    if args.db_url:
        engine = create_engine(args.db_url, pool_pre_ping=True)
        SessionLocalToUse = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    main(SessionLocalToUse)
