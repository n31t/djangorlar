from decimal import Decimal
from datetime import date
from typing import Any
from contextlib import nullcontext as does_not_raise

import pytest
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from drf.models import Course, Lesson

User = get_user_model()

@pytest.fixture
def api_client() -> APIClient:
    """Create API client for making requests."""
    return APIClient()


@pytest.fixture
def user_owner(db) -> User:
    """Create a user who owns courses."""
    return User.objects.create_user(
        email="owner@test.com",
        full_name="Course Owner",
        password="TestPass123!",
        department="it",
        role="admin",
        birth_date=date(1990, 1, 1),
    )


@pytest.fixture
def user_non_owner(db) -> User:
    """Create a user who doesn't own courses."""
    return User.objects.create_user(
        email="nonowner@test.com",
        full_name="Non Owner",
        password="TestPass123!",
        department="hr",
        role="employee",
        birth_date=date(1995, 5, 15),
    )


@pytest.fixture
def owner_token(user_owner: User) -> str:
    """Generate JWT token for course owner."""
    refresh: RefreshToken = RefreshToken.for_user(user_owner)
    return str(refresh.access_token)


@pytest.fixture
def non_owner_token(user_non_owner: User) -> str:
    """Generate JWT token for non-owner."""
    refresh: RefreshToken = RefreshToken.for_user(user_non_owner)
    return str(refresh.access_token)


@pytest.fixture
def course(db, user_owner: User) -> Course:
    """Create a course owned by user_owner."""
    return Course.objects.create(
        title="Django Basics",
        description="Learn Django fundamentals",
        owner=user_owner,
        is_active=True,
    )


@pytest.fixture
def inactive_course(db, user_owner: User) -> Course:
    """Create an inactive course."""
    return Course.objects.create(
        title="Inactive Course",
        description="This course is inactive",
        owner=user_owner,
        is_active=False,
    )


@pytest.fixture
def lesson(db, course: Course) -> Lesson:
    """Create a lesson in the course."""
    return Lesson.objects.create(
        title="First Lesson",
        content="Content of first lesson",
        order=Decimal("1.00"),
        indentation=0,
        is_published=False,
        course=course,
    )


@pytest.fixture
def published_lesson(db, course: Course) -> Lesson:
    """Create a published lesson."""
    return Lesson.objects.create(
        title="Published Lesson",
        content="This is published",
        order=Decimal("2.00"),
        indentation=0,
        is_published=True,
        course=course,
    )


@pytest.mark.django_db
class TestCourseList:
    """Test GET /api/v1/education/courses/"""

    @pytest.mark.parametrize(
        argnames=["has_token", "expected_status", "expectation"],
        argvalues=[
            (True, 200, does_not_raise()),
            (False, 401, does_not_raise()),
        ]
    )
    def test_list_courses_auth(
        self,
        api_client: APIClient,
        owner_token: str,
        course: Course,
        has_token: bool,
        expected_status: int,
        expectation: Any
    ) -> None:
        """Test listing courses with and without authentication."""
        with expectation:
            if has_token:
                api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')

            response = api_client.get('/api/v1/education/courses')

            assert response.status_code == expected_status, \
                f"Expected status {expected_status}, got {response.status_code}"

            if has_token:
                assert len(response.data) >= 1, "Must return at least one course"
                assert 'author' in response.data[0], "Must include author info"
                assert 'lessons_count' in response.data[0], "Must include lessons count"

    @pytest.mark.parametrize(
        argnames=["filter_param", "expected_active"],
        argvalues=[
            ("is_active=true", True),
            ("is_active=false", False),
        ]
    )
    def test_list_courses_filter(
        self,
        api_client: APIClient,
        owner_token: str,
        course: Course,
        inactive_course: Course,
        filter_param: str,
        expected_active: bool
    ) -> None:
        """Test filtering courses by is_active parameter."""
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')
        response = api_client.get(f'/api/v1/education/courses?{filter_param}')

        assert response.status_code == 200, "Must return 200 OK"
        for course_data in response.data:
            assert course_data['is_active'] == expected_active, \
                f"All courses must have is_active={expected_active}"


@pytest.mark.django_db
class TestCourseRetrieve:
    """Test GET /api/v1/education/courses/{id}/"""

    @pytest.mark.parametrize(
        argnames=["course_exists", "expected_status"],
        argvalues=[
            (True, 200),
            (False, 404),
        ]
    )
    def test_retrieve_course(
        self,
        api_client: APIClient,
        owner_token: str,
        course: Course,
        course_exists: bool,
        expected_status: int
    ) -> None:
        """Test retrieving a course by ID."""
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')
        course_id: int = course.id if course_exists else 99999

        response = api_client.get(f'/api/v1/education/courses/{course_id}')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if course_exists:
            assert response.data['id'] == course.id, "Must return correct course ID"
            assert response.data['title'] == 'Django Basics', "Must return correct title"


@pytest.mark.django_db
class TestCourseCreate:
    """Test POST /api/v1/education/courses/"""

    @pytest.mark.parametrize(
        argnames=["data", "expected_status", "expectation"],
        argvalues=[
            (
                {'title': 'New Course', 'description': 'New description'},
                201,
                does_not_raise()
            ),
            (
                {'description': 'Missing title'},
                400,
                does_not_raise()
            ),
            (
                {'title': 'Missing description'},
                400,
                does_not_raise()
            ),
        ]
    )
    def test_create_course(
        self,
        api_client: APIClient,
        owner_token: str,
        data: dict[str, str],
        expected_status: int,
        expectation: Any
    ) -> None:
        """Test creating a course with different data."""
        with expectation:
            api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')
            response = api_client.post('/api/v1/education/courses', data, format='json')

            assert response.status_code == expected_status, \
                f"Expected status {expected_status}, got {response.status_code}"

            if expected_status == 201:
                assert response.data['title'] == data['title'], \
                    "Created course must have correct title"
                assert 'author' in response.data, "Must include author info"


@pytest.mark.django_db
class TestCourseUpdate:
    """Test PUT /api/v1/education/courses/{id}/"""

    @pytest.mark.parametrize(
        argnames=["is_owner", "expected_status"],
        argvalues=[
            (True, 200),
            (False, 403),
        ]
    )
    def test_update_course(
        self,
        api_client: APIClient,
        owner_token: str,
        non_owner_token: str,
        course: Course,
        is_owner: bool,
        expected_status: int
    ) -> None:
        """Test updating a course by owner and non-owner."""
        token: str = owner_token if is_owner else non_owner_token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data: dict[str, str] = {
            'title': 'Updated Title',
            'description': 'Updated description',
        }
        response = api_client.put(f'/api/v1/education/courses/{course.id}', data, format='json')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if is_owner:
            assert response.data['title'] == 'Updated Title', "Must update title correctly"


@pytest.mark.django_db
class TestCourseActivate:
    """Test POST /api/v1/education/courses/{id}/activate/"""

    @pytest.mark.parametrize(
        argnames=["is_active", "expected_status", "should_succeed"],
        argvalues=[
            (False, 200, True),
            (True, 400, False),
        ]
    )
    def test_activate_course(
        self,
        api_client: APIClient,
        owner_token: str,
        user_owner: User,
        is_active: bool,
        expected_status: int,
        should_succeed: bool
    ) -> None:
        """Test activating active and inactive courses."""
        test_course: Course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=user_owner,
            is_active=is_active,
        )

        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')
        response = api_client.post(f'/api/v1/education/courses/{test_course.id}/activate')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if should_succeed:
            assert response.data['is_active'] is True, "Course must be active after activation"
        else:
            assert 'already active' in response.data['detail'].lower(), \
                "Must indicate course is already active"


@pytest.mark.django_db
class TestCourseDeactivate:
    """Test POST /api/v1/education/courses/{id}/deactivate/"""

    @pytest.mark.parametrize(
        argnames=["is_active", "expected_status", "should_succeed"],
        argvalues=[
            (True, 200, True),
            (False, 400, False),
        ]
    )
    def test_deactivate_course(
        self,
        api_client: APIClient,
        owner_token: str,
        user_owner: User,
        is_active: bool,
        expected_status: int,
        should_succeed: bool
    ) -> None:
        """Test deactivating active and inactive courses."""
        test_course: Course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=user_owner,
            is_active=is_active,
        )

        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')
        response = api_client.post(f'/api/v1/education/courses/{test_course.id}/deactivate')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if should_succeed:
            assert response.data['is_active'] is False, \
                "Course must be inactive after deactivation"
        else:
            assert 'already inactive' in response.data['detail'].lower(), \
                "Must indicate course is already inactive"


@pytest.mark.django_db
class TestCourseLessons:
    """Test GET /api/v1/education/courses/{id}/lessons/"""

    @pytest.mark.parametrize(
        argnames=["has_lessons", "expected_count"],
        argvalues=[
            (True, 1),
            (False, 0),
        ]
    )
    def test_get_course_lessons(
        self,
        api_client: APIClient,
        owner_token: str,
        course: Course,
        inactive_course: Course,
        lesson: Lesson,
        has_lessons: bool,
        expected_count: int
    ) -> None:
        """Test getting lessons for courses with and without lessons."""
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')
        test_course: Course = course if has_lessons else inactive_course

        response = api_client.get(f'/api/v1/education/courses/{test_course.id}/lessons')

        assert response.status_code == 200, "Must return 200 OK"
        assert len(response.data) == expected_count, \
            f"Must return {expected_count} lessons"


@pytest.mark.django_db
class TestLessonCreate:
    """Test POST /api/v1/education/lessons"""

    @pytest.mark.parametrize(
        argnames=["has_course", "data", "expected_status"],
        argvalues=[
            (
                True,
                {'title': 'New Lesson', 'content': 'New content'},
                201
            ),
            (
                False,
                {'title': 'New Lesson', 'content': 'New content'},
                400
            ),
            (
                True,
                {'content': 'Missing title'},
                400
            ),
        ]
    )
    def test_create_lesson(
        self,
        api_client: APIClient,
        owner_token: str,
        non_owner_token: str,
        course: Course,
        has_course: bool,
        data: dict[str, str],
        expected_status: int
    ) -> None:
        """Test creating a lesson with different scenarios."""
        token: str = owner_token if has_course else non_owner_token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.post('/api/v1/education/lessons', data, format='json')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if expected_status == 201:
            assert response.data['title'] == data['title'], "Must have correct title"
            assert response.data['course'] == course.id, "Must be in correct course"
            assert 'order' in response.data, "Must include order field"
        elif not has_course and expected_status == 400:
            assert 'No found courses' in response.data['detail'], \
                "Must indicate no courses found"


@pytest.mark.django_db
class TestLessonMove:
    """Test PUT /api/v1/education/lessons/{id}/move"""

    @pytest.mark.parametrize(
        argnames=["is_owner", "before_lesson_id", "expected_status"],
        argvalues=[
            (True, "valid", 200),
            (True, None, 200),
            (False, None, 403),
        ]
    )
    def test_move_lesson(
        self,
        api_client: APIClient,
        owner_token: str,
        non_owner_token: str,
        lesson: Lesson,
        published_lesson: Lesson,
        is_owner: bool,
        before_lesson_id: str | None,
        expected_status: int
    ) -> None:
        """Test moving a lesson to different positions."""
        token: str = owner_token if is_owner else non_owner_token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        if before_lesson_id == "valid":
            data: dict[str, int | None] = {'before_lesson_id': published_lesson.id}
        else:
            data: dict[str, int | None] = {'before_lesson_id': None}

        response = api_client.put(
            f'/api/v1/education/lessons/{lesson.id}/move',
            data,
            format='json'
        )

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if expected_status == 200:
            assert 'order' in response.data, "Must return order"
            assert 'indentation' in response.data, "Must return indentation"
            if before_lesson_id is None:
                assert response.data['indentation'] == 0, \
                    "Moving to last should have indentation 0"


@pytest.mark.django_db
class TestLessonPublish:
    """Test POST /api/v1/education/lessons/{id}/publish"""

    @pytest.mark.parametrize(
        argnames=["is_owner", "expected_status"],
        argvalues=[
            (True, 200),
            (False, 403),
        ]
    )
    def test_publish_lesson(
        self,
        api_client: APIClient,
        owner_token: str,
        non_owner_token: str,
        lesson: Lesson,
        is_owner: bool,
        expected_status: int
    ) -> None:
        """Test publishing a lesson by owner and non-owner."""
        token: str = owner_token if is_owner else non_owner_token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.post(f'/api/v1/education/lessons/{lesson.id}/publish')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if is_owner:
            assert 'published successfully' in response.data['detail'].lower(), \
                "Must indicate successful publishing"


@pytest.mark.django_db
class TestLessonUnpublish:
    """Test POST /api/v1/education/lessons/{id}/unpublish"""

    @pytest.mark.parametrize(
        argnames=["lesson_exists", "expected_status"],
        argvalues=[
            (True, 200),
            (False, 404),
        ]
    )
    def test_unpublish_lesson(
        self,
        api_client: APIClient,
        owner_token: str,
        published_lesson: Lesson,
        lesson_exists: bool,
        expected_status: int
    ) -> None:
        """Test unpublishing existing and non-existing lessons."""
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {owner_token}')
        lesson_id: int = published_lesson.id if lesson_exists else 99999

        response = api_client.post(f'/api/v1/education/lessons/{lesson_id}/unpublish')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"

        if lesson_exists:
            assert 'unpublished successfully' in response.data['detail'].lower(), \
                "Must indicate successful unpublishing"


@pytest.mark.django_db
class TestLessonDelete:
    """Test DELETE /api/v1/education/lessons/{id}/"""

    @pytest.mark.parametrize(
        argnames=["is_owner", "expected_status"],
        argvalues=[
            (True, 204),
            (False, 403),
        ]
    )
    def test_delete_lesson(
        self,
        api_client: APIClient,
        owner_token: str,
        non_owner_token: str,
        lesson: Lesson,
        is_owner: bool,
        expected_status: int
    ) -> None:
        """Test deleting a lesson by owner and non-owner."""
        token: str = owner_token if is_owner else non_owner_token
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = api_client.delete(f'/api/v1/education/lessons/{lesson.id}')

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"