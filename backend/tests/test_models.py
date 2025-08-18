"""
Unit tests for the database models
"""

from datetime import date, datetime, timezone

import pytest
from sqlalchemy.orm import Session

from app.models import Category, Experience, Post, Project, User


class TestUserModel:
    """Test class for User model"""

    @pytest.mark.unit
    def test_user_creation(self, db_session: Session):
        """Test basic user creation"""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashedpassword",
            is_admin=False,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.is_admin == False
        assert user.is_active == True
        assert user.created_at is not None
        assert user.updated_at is None

    @pytest.mark.unit
    def test_user_admin_creation(self, db_session: Session):
        """Test admin user creation"""
        admin_user = User(
            email="admin@example.com",
            username="adminuser",
            hashed_password="hashedpassword",
            is_admin=True,
            is_active=True,
        )
        db_session.add(admin_user)
        db_session.commit()
        db_session.refresh(admin_user)

        assert admin_user.is_admin == True

    @pytest.mark.unit
    def test_user_inactive_creation(self, db_session: Session):
        """Test inactive user creation"""
        inactive_user = User(
            email="inactive@example.com",
            username="inactiveuser",
            hashed_password="hashedpassword",
            is_admin=False,
            is_active=False,
        )
        db_session.add(inactive_user)
        db_session.commit()
        db_session.refresh(inactive_user)

        assert inactive_user.is_active == False

    @pytest.mark.unit
    def test_user_timestamps(self, db_session: Session):
        """Test that timestamps are set correctly"""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashedpassword",
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Check that timestamps are set
        assert user.created_at is not None
        assert user.updated_at is None  # Only set on update

        # Update user and check that updated_at changes
        original_updated_at = user.updated_at  # Should be None initially
        user.username = "updateduser"
        db_session.commit()
        db_session.refresh(user)

        # After update, updated_at should be set
        assert user.updated_at is not None
        # The updated_at should be different from the original None value
        assert user.updated_at != original_updated_at

    @pytest.mark.unit
    def test_user_relationships(self, db_session: Session, test_user, test_post):
        """Test user relationships with posts"""
        # User should have posts relationship
        assert hasattr(test_user, "posts")
        assert test_post in test_user.posts


class TestCategoryModel:
    """Test class for Category model"""

    @pytest.mark.unit
    def test_category_creation(self, db_session: Session):
        """Test basic category creation"""
        category = Category(
            name="Test Category", slug="test-category", description="A test category"
        )
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        assert category.id is not None
        assert category.name == "Test Category"
        assert category.slug == "test-category"
        assert category.description == "A test category"

    @pytest.mark.unit
    def test_category_without_description(self, db_session: Session):
        """Test category creation without description"""
        category = Category(name="Test Category", slug="test-category")
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        assert category.description is None

    @pytest.mark.unit
    def test_category_timestamps(self, db_session: Session):
        """Test that category timestamps are set correctly"""
        category = Category(name="Test Category", slug="test-category")
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)

        assert category.created_at is not None
        assert category.updated_at is None  # Only set on update

    @pytest.mark.unit
    def test_category_relationships(
        self, db_session: Session, test_category, test_post
    ):
        """Test category relationships with posts"""
        # Category should have posts relationship
        assert hasattr(test_category, "posts")
        assert test_post in test_category.posts


class TestPostModel:
    """Test class for Post model"""

    @pytest.mark.unit
    def test_post_creation(self, db_session: Session, test_user, test_category):
        """Test basic post creation"""
        post = Post(
            title="Test Post",
            slug="test-post",
            content="# Test Post\n\nThis is test content.",
            excerpt="A test post excerpt",
            read_time="5 min read",
            author_id=test_user.id,
            category_id=test_category.id,
            published_at=datetime.now(timezone.utc),
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        assert post.id is not None
        assert post.title == "Test Post"
        assert post.slug == "test-post"
        assert post.content == "# Test Post\n\nThis is test content."
        assert post.excerpt == "A test post excerpt"
        assert post.read_time == "5 min read"
        assert post.author_id == test_user.id
        assert post.category_id == test_category.id
        assert post.published_at is not None

    @pytest.mark.unit
    def test_draft_post_creation(self, db_session: Session, test_user, test_category):
        """Test draft post creation (unpublished)"""
        draft_post = Post(
            title="Draft Post",
            slug="draft-post",
            content="# Draft Post\n\nThis is draft content.",
            excerpt="A draft post excerpt",
            read_time="3 min read",
            author_id=test_user.id,
            category_id=test_category.id,
            published_at=None,  # Unpublished
        )
        db_session.add(draft_post)
        db_session.commit()
        db_session.refresh(draft_post)

        assert draft_post.published_at is None

    @pytest.mark.unit
    def test_post_relationships(
        self, db_session: Session, test_post, test_user, test_category
    ):
        """Test post relationships"""
        # Post should have author and category relationships
        assert test_post.author == test_user
        assert test_post.category == test_category

    @pytest.mark.unit
    def test_post_timestamps(self, db_session: Session, test_user, test_category):
        """Test that post timestamps are set correctly"""
        post = Post(
            title="Test Post",
            slug="test-post",
            content="Test content",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        assert post.created_at is not None
        assert post.updated_at is None  # Only set on update

    @pytest.mark.unit
    def test_post_without_optional_fields(
        self, db_session: Session, test_user, test_category
    ):
        """Test post creation without optional fields"""
        post = Post(
            title="Minimal Post",
            slug="minimal-post",
            content="Minimal content",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        assert post.excerpt is None
        assert post.read_time is None
        assert post.published_at is None


class TestProjectModel:
    """Test class for Project model"""

    @pytest.mark.unit
    def test_project_creation(self, db_session: Session):
        """Test basic project creation"""
        project = Project(
            title="Test Project",
            description="A test project description",
            technologies=["Python", "FastAPI", "React"],
            github_url="https://github.com/test/project",
            live_url="https://test-project.com",
            image="https://example.com/image.jpg",
            featured=True,
        )
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        assert project.id is not None
        assert project.title == "Test Project"
        assert project.description == "A test project description"
        assert project.technologies == ["Python", "FastAPI", "React"]
        assert project.github_url == "https://github.com/test/project"
        assert project.live_url == "https://test-project.com"
        assert project.image == "https://example.com/image.jpg"
        assert project.featured == True
        assert project.is_active == True

    @pytest.mark.unit
    def test_project_without_optional_fields(self, db_session: Session):
        """Test project creation without optional fields"""
        project = Project(title="Minimal Project", description="A minimal project")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        assert project.technologies == []
        assert project.github_url is None
        assert project.live_url is None
        assert project.image is None
        assert project.featured == False
        assert project.is_active == True

    @pytest.mark.unit
    def test_project_timestamps(self, db_session: Session):
        """Test that project timestamps are set correctly"""
        project = Project(title="Test Project", description="Test description")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        assert project.created_at is not None
        assert project.updated_at is None  # Only set on update

    @pytest.mark.unit
    def test_project_soft_delete(self, db_session: Session):
        """Test project soft delete functionality"""
        project = Project(title="Test Project", description="Test description")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        # Soft delete
        project.is_active = False
        db_session.commit()
        db_session.refresh(project)

        assert project.is_active == False


class TestExperienceModel:
    """Test class for Experience model"""

    @pytest.mark.unit
    def test_experience_creation(self, db_session: Session):
        """Test basic experience creation"""
        experience = Experience(
            title="Test Position",
            company="Test Company",
            location="Test City, Test State",
            period="Jan 2022 - Dec 2023",
            start_date=datetime(2022, 1, 1).date(),
            end_date=datetime(2023, 12, 31).date(),
            description="A test job description",
            technologies=["Python", "SQL", "AWS"],
            achievements=["Achievement 1", "Achievement 2"],
        )
        db_session.add(experience)
        db_session.commit()
        db_session.refresh(experience)

        assert experience.id is not None
        assert experience.title == "Test Position"
        assert experience.company == "Test Company"
        assert experience.location == "Test City, Test State"
        assert experience.period == "Jan 2022 - Dec 2023"
        assert experience.start_date == datetime(2022, 1, 1).date()
        assert experience.end_date == datetime(2023, 12, 31).date()
        assert experience.description == "A test job description"
        assert experience.technologies == ["Python", "SQL", "AWS"]
        assert experience.achievements == ["Achievement 1", "Achievement 2"]
        assert experience.is_active == True

    @pytest.mark.unit
    def test_current_experience_creation(self, db_session: Session):
        """Test current experience creation (no end date)"""
        current_experience = Experience(
            title="Current Position",
            company="Current Company",
            location="Current City, State",
            period="Jan 2023 - Present",
            start_date=datetime(2023, 1, 1).date(),
            description="A current position",
            technologies=["Python", "FastAPI"],
            achievements=["Current achievement"],
        )
        db_session.add(current_experience)
        db_session.commit()
        db_session.refresh(current_experience)

        assert current_experience.end_date is None
        assert current_experience.period == "Jan 2023 - Present"

    @pytest.mark.unit
    def test_experience_without_optional_fields(self, db_session: Session):
        """Test experience creation without optional fields"""
        experience = Experience(
            title="Minimal Position",
            company="Minimal Company",
            location="Minimal Location",
            period="Jan 2022 - Dec 2023",
            start_date=datetime(2022, 1, 1).date(),
            description="Minimal description",
            technologies=[],
            achievements=[],
        )
        db_session.add(experience)
        db_session.commit()
        db_session.refresh(experience)

        assert experience.end_date is None
        assert experience.is_active == True

    @pytest.mark.unit
    def test_experience_timestamps(self, db_session: Session):
        """Test that experience timestamps are set correctly"""
        experience = Experience(
            title="Test Position",
            company="Test Company",
            location="Test Location",
            period="Jan 2022 - Dec 2023",
            start_date=datetime(2022, 1, 1).date(),
            description="Test description",
            technologies=[],
            achievements=[],
        )
        db_session.add(experience)
        db_session.commit()
        db_session.refresh(experience)

        assert experience.created_at is not None
        assert experience.updated_at is None  # Only set on update

    @pytest.mark.unit
    def test_experience_soft_delete(self, db_session: Session):
        """Test experience soft delete functionality"""
        experience = Experience(
            title="Test Position",
            company="Test Company",
            location="Test Location",
            period="Jan 2022 - Dec 2023",
            start_date=datetime(2022, 1, 1).date(),
            description="Test description",
            technologies=[],
            achievements=[],
        )
        db_session.add(experience)
        db_session.commit()
        db_session.refresh(experience)

        # Soft delete
        experience.is_active = False
        db_session.commit()
        db_session.refresh(experience)

        assert experience.is_active == False


class TestModelRelationships:
    """Test class for model relationships"""

    @pytest.mark.unit
    def test_user_posts_relationship(
        self, db_session: Session, test_user, test_category, test_post
    ):
        """Test user-posts relationship"""
        # Create multiple posts for the same user
        post1 = Post(
            title="Post 1",
            slug="post-1",
            content="Content 1",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        post2 = Post(
            title="Post 2",
            slug="post-2",
            content="Content 2",
            author_id=test_user.id,
            category_id=test_category.id,
        )

        db_session.add_all([post1, post2])
        db_session.commit()

        # Check that user has both posts plus the test_post from fixture
        assert len(test_user.posts) == 3  # Including the test_post from fixture
        assert post1 in test_user.posts
        assert post2 in test_user.posts
        # Refresh to ensure relationships are loaded
        db_session.refresh(test_user)

    @pytest.mark.unit
    def test_category_posts_relationship(
        self, db_session: Session, test_user, test_category, test_post
    ):
        """Test category-posts relationship"""
        # Create multiple posts in the same category
        post1 = Post(
            title="Post 1",
            slug="post-1",
            content="Content 1",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        post2 = Post(
            title="Post 2",
            slug="post-2",
            content="Content 2",
            author_id=test_user.id,
            category_id=test_category.id,
        )

        db_session.add_all([post1, post2])
        db_session.commit()

        # Check that category has both posts plus the test_post from fixture
        assert len(test_category.posts) == 3  # Including the test_post from fixture
        assert post1 in test_category.posts
        assert post2 in test_category.posts
        # Refresh to ensure relationships are loaded
        db_session.refresh(test_category)

    @pytest.mark.unit
    def test_post_author_category_relationships(
        self, db_session: Session, test_user, test_category
    ):
        """Test post relationships with author and category"""
        post = Post(
            title="Test Post",
            slug="test-post",
            content="Test content",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        db_session.add(post)
        db_session.commit()
        db_session.refresh(post)

        # Check relationships
        assert post.author == test_user
        assert post.category == test_category
        assert post.author.email == "test@example.com"
        assert post.category.name == "Test Category"


class TestModelConstraints:
    """Test class for model constraints and validation"""

    @pytest.mark.unit
    def test_user_email_uniqueness(self, db_session: Session):
        """Test that user email must be unique"""
        user1 = User(
            email="test@example.com", username="user1", hashed_password="password"
        )
        db_session.add(user1)
        db_session.commit()

        # Try to create another user with same email
        user2 = User(
            email="test@example.com", username="user2", hashed_password="password"
        )
        db_session.add(user2)

        # Should raise an integrity error
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db_session.commit()

    @pytest.mark.unit
    def test_user_username_uniqueness(self, db_session: Session):
        """Test that user username must be unique"""
        user1 = User(
            email="user1@example.com", username="testuser", hashed_password="password"
        )
        db_session.add(user1)
        db_session.commit()

        # Try to create another user with same username
        user2 = User(
            email="user2@example.com", username="testuser", hashed_password="password"
        )
        db_session.add(user2)

        # Should raise an integrity error
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db_session.commit()

    @pytest.mark.unit
    def test_category_slug_uniqueness(self, db_session: Session):
        """Test that category slug must be unique"""
        category1 = Category(name="Test Category", slug="test-category")
        db_session.add(category1)
        db_session.commit()

        # Try to create another category with same slug
        category2 = Category(name="Another Category", slug="test-category")
        db_session.add(category2)

        # Should raise an integrity error
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db_session.commit()

    @pytest.mark.unit
    def test_post_slug_uniqueness(self, db_session: Session, test_user, test_category):
        """Test that post slug must be unique"""
        post1 = Post(
            title="Test Post",
            slug="test-post",
            content="Content",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        db_session.add(post1)
        db_session.commit()

        # Try to create another post with same slug
        post2 = Post(
            title="Another Post",
            slug="test-post",
            content="Content",
            author_id=test_user.id,
            category_id=test_category.id,
        )
        db_session.add(post2)

        # Should raise an integrity error
        with pytest.raises(Exception):  # SQLAlchemy IntegrityError
            db_session.commit()
