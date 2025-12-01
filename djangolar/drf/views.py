from typing import Any

from django.db import models
from django.db.models import Count, Q

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request as DRFRequest
from rest_framework.response import Response as DRFResponse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Course, Lesson
from .serializers import CourseListSerializer, LessonListSerializer
from .permissions import IsUserTheOwner



class CourseViewSet(ViewSet):
    """
    ViewSet for handling Course-related endpoints.

    List courses with author info and lessons count.
    GET /api/v1/education/courses/
    Query params:
        - is_active: true/false (optional)

    Create a course.
    POST /api/v1/education/courses/

    Update a course.
    PUT /api/v1/education/courses/{id}/
    PATCH /api/v1/education/courses/{id}/
    """

    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.

        Returns:
        list - List of permission instances.
        """
        if self.action in ('update', 'partial_update', 'destroy', 'activate', 'deactivate'):
            permission_classes = [IsAuthenticated, IsUserTheOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Course.objects.filter(
            deleted_at__isnull=True
        ).select_related(
            'owner'
        ).annotate(
            lessons_count=Count(
                'lessons',
                filter=Q(lessons__deleted_at__isnull=True)
            )
        )

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            is_active_bool = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active_bool)

        return queryset
    
    def list(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        List all courses with author info and lessons count.

        Parameters:
        request: DRFRequest - The request object.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing list of courses.
        """
        queryset = self.get_queryset()
        serializer: CourseListSerializer = CourseListSerializer(
            queryset,
            many=True
        )
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    def retrieve(
        self,
        request: DRFRequest,
        pk: int = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Retrieve a single course by ID with author info and lessons count.

        Parameters:
        request: DRFRequest - The request object.
        pk: int - The primary key of the course to retrieve.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing single course object.
        """
        queryset = self.get_queryset()
        course = queryset.filter(id=pk).first()

        if not course:
            return DRFResponse(
                data={"detail": "Course not found."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: CourseListSerializer = CourseListSerializer(course)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    def create(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Create a new course.

        Parameters:
        request: DRFRequest - The request object containing title and description.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing created course object.
        """
        serializer: CourseListSerializer = CourseListSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    def update(
        self,
        request: DRFRequest,
        pk: int = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Update a course by ID.

        Parameters:
        request: DRFRequest - The request object containing updated course data.
        pk: int - The primary key of the course to update.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing updated course object.
        """
        queryset = self.get_queryset()
        course = queryset.filter(id=pk).first()

        if not course:
            return DRFResponse(
                data={"detail": "Course not found."},
                status=HTTP_404_NOT_FOUND
            )

        serializer: CourseListSerializer = CourseListSerializer(
            instance=course,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    def delete(
        self,
        request: DRFRequest,
        pk: int = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Delete a course by ID.

        Parameters:
        request: DRFRequest - The request object.
        pk: int - The primary key of the course to delete.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing deleted course object.
        """
        queryset = self.get_queryset()
        course = queryset.filter(id=pk).first()

        if not course:
            return DRFResponse(
                data={"detail": "Course not found."},
                status=HTTP_404_NOT_FOUND
            )

        course.delete()

        return DRFResponse(
            data={"detail": "Course deleted successfully."},
            status=HTTP_204_NO_CONTENT
        )

    @action(
        methods=("POST",),
        detail=True,
        url_path="activate",
        url_name="activate",
        permission_classes=(IsAuthenticated, IsUserTheOwner)
    )
    def activate(
        self,
        request: DRFRequest,
        pk: int = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Activate a course by ID.
        Validates that course is inactive before activating.
        Requires user to be the owner of the course.

        Parameters:
        request: DRFRequest - The request object.
        pk: int - The primary key of the course to activate.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing the activated course object with is_active = true.
        """
        queryset = Course.objects.filter(
            deleted_at__isnull=True
        ).select_related(
            'owner'
        ).annotate(
            lessons_count=Count(
                'lessons',
                filter=Q(lessons__deleted_at__isnull=True)
            )
        )
        course = queryset.filter(id=pk).first()

        if not course:
            return DRFResponse(
                data={"detail": "Course not found."},
                status=HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, course)

        if course.is_active:
            return DRFResponse(
                data={"detail": "Course is already active."},
                status=HTTP_400_BAD_REQUEST
            )

        course.is_active = True
        course.save()

        serializer: CourseListSerializer = CourseListSerializer(course)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )


    @action(
        methods=("POST",),
        detail=True,
        url_path="deactivate",
        url_name="deactivate",
        permission_classes=(IsAuthenticated, IsUserTheOwner)
    )
    def deactivate(
        self,
        request: DRFRequest,
        pk: int = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Deactivate a course by ID.
        Validates that course is active before deactivating.
        Requires user to be the owner of the course.

        Parameters:
        request: DRFRequest - The request object.
        pk: int - The primary key of the course to deactivate.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing the deactivated course object with is_active = false.
        """
        queryset = Course.objects.filter(
            deleted_at__isnull=True
        ).select_related(
            'owner'
        ).annotate(
            lessons_count=Count(
                'lessons',
                filter=Q(lessons__deleted_at__isnull=True)
            )
        )
        course = queryset.filter(id=pk).first()

        if not course:
            return DRFResponse(
                data={"detail": "Course not found."},
                status=HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, course)

        if not course.is_active:
            return DRFResponse(
                data={"detail": "Course is already inactive."},
                status=HTTP_400_BAD_REQUEST
            )

        course.is_active = False
        course.save()

        serializer: CourseListSerializer = CourseListSerializer(course)
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )

    @action(
        methods=("GET",),
        detail=True,
        url_path="lessons",
        url_name="lessons",
        permission_classes=(IsAuthenticated,)
    )
    def lessons(
        self,
        request: DRFRequest,
        pk: int = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        List lessons for a course.
        Requires user to be authenticated.

        Parameters:
        request: DRFRequest - The request object.
        pk: int - The primary key of the course.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing list of lessons for the course.
        """
        queryset = Lesson.objects.filter(
            course_id=pk,
            deleted_at__isnull=True
        )
        lessons = queryset.all()

        serializer: LessonListSerializer = LessonListSerializer(
            lessons,
            many=True,
            context={'request': request}
        )
        return DRFResponse(
            data=serializer.data,
            status=HTTP_200_OK
        )


class LessonViewSet(ViewSet):
    """
    ViewSet for handling Lesson-related endpoints.
    """

    permission_classes=(IsAuthenticated, IsUserTheOwner)


    def create(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Create a new lesson.
        Automatically gets the first non-deleted course of the user.
        Automatically sets order to make the lesson first.

        Parameters:
        request: DRFRequest - The request object containing only title and content.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing created lesson object.
        """
        course = Course.objects.filter(
            owner=request.user,
            deleted_at__isnull=True
        ).order_by('created_at').first()

        if not course:
            return DRFResponse(
                data={"detail": "No found courses"},
                status=HTTP_400_BAD_REQUEST
            )

        min_order = Lesson.objects.filter(
            course=course,
            deleted_at__isnull=True
        ).aggregate(models.Min('order'))['order__min']

        if min_order is None:
            new_order = 1
        else:
            new_order = min_order - 1

        serializer: LessonListSerializer = LessonListSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(order=new_order, course=course)

        return DRFResponse(
            data=serializer.data,
            status=HTTP_201_CREATED
        )

    @action(
        methods=("PUT",),
        detail=True,
        url_path="move",
        url_name="move",
        permission_classes=(IsAuthenticated, IsUserTheOwner)
    )
    def move(
        self,
        request: DRFRequest,
        pk: int = None,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Move a lesson to a new position.
        Recalculates order and indentation based on new position.
        Requires user to be the owner of the course.

        Parameters:
        request: DRFRequest - The request object containing before_lesson_id.
        pk: int - The primary key of the lesson to move.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing new order value and indentation.
        """
        try:
            lesson = Lesson.objects.select_related('course__owner').get(
                id=pk,
                deleted_at__isnull=True
            )
        except Lesson.DoesNotExist:
            return DRFResponse(
                data={"detail": "Lesson not found."},
                status=HTTP_404_NOT_FOUND
            )

        if lesson.course.owner != request.user:
            return DRFResponse(
                data={"detail": "You are not the owner of this course."},
                status=HTTP_403_FORBIDDEN
            )

        before_lesson_id = request.data.get('before_lesson_id')

        course_lessons = Lesson.objects.filter(
            course=lesson.course,
            deleted_at__isnull=True
        ).exclude(id=lesson.id).order_by('order')

        if before_lesson_id is None:
            max_order = course_lessons.aggregate(models.Max('order'))['order__max']
            if max_order is None:
                new_order = 1
            else:
                new_order = max_order + 1
            new_indentation = 0
        else:
            try:
                before_lesson = Lesson.objects.get(
                    id=before_lesson_id,
                    course=lesson.course,
                    deleted_at__isnull=True
                )
            except Lesson.DoesNotExist:
                return DRFResponse(
                    data={"detail": "Target lesson not found in the same course."},
                    status=HTTP_404_NOT_FOUND
                )

            lessons_before = course_lessons.filter(
                order__lt=before_lesson.order
            ).order_by('-order').first()

            if lessons_before is None:
                new_order = before_lesson.order - 1
                new_indentation = 0
            else:
                new_order = (lessons_before.order + before_lesson.order) / 2

                if before_lesson.indentation > lessons_before.indentation:
                    new_indentation = before_lesson.indentation
                else:
                    new_indentation = before_lesson.indentation

        lesson.order = new_order
        lesson.indentation = new_indentation
        lesson.save()

        return DRFResponse(
            data={
                "order": float(lesson.order),
                "indentation": lesson.indentation
            },
            status=HTTP_200_OK
        )

    @action(
        methods=("DELETE", ),
        detail=True,
        url_path="",
        url_name="",
        permission_classes=(IsAuthenticated, IsUserTheOwner)
    )
    def delete_lesson(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Delete a lesson.
        Validates that the user is the owner of the course.

        Parameters:
        request: DRFRequest - The request object.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing deleted lesson object.
        """
        lesson = self.get_object()
        lesson.deleted_at = timezone.now()
        lesson.save()
        return DRFResponse(
            data={"detail": "Lesson deleted successfully."},
            status=HTTP_204_NO_CONTENT
        )

    @action(
        methods=("POST", ),
        detail=True,
        url_path="publish",
        url_name="publish",
        permission_classes=(IsAuthenticated, IsUserTheOwner)
    )
    def publish_lesson(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Publish a lesson.
        Validates that the user is the owner of the course.

        Parameters:
        request: DRFRequest - The request object.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing published lesson object.
        """
        lesson = self.get_object()
        lesson.is_published = True
        lesson.save()
        return DRFResponse(
            data={"detail": "Lesson published successfully."},
            status=HTTP_200_OK
        )


    @action(
        methods=("POST", ),
        detail=True,
        url_path="unpublish",
        url_name="unpublish",
        permission_classes=(IsAuthenticated, IsUserTheOwner)
    )
    def unpublish_lesson(
        self,
        request: DRFRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any]
    ) -> DRFResponse:
        """
        Unpublish a lesson.
        Validates that the user is the owner of the course.

        Parameters:
        request: DRFRequest - The request object.
        *args: tuple - Additional positional arguments.
        **kwargs: dict - Additional keyword arguments.

        Returns:
        DRFResponse - Response containing unpublished lesson object.
        """
        lesson = self.get_object()
        lesson.is_published = False
        lesson.save()
        return DRFResponse(
            data={"detail": "Lesson unpublished successfully."},
            status=HTTP_200_OK
        )
