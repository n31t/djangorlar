from rest_framework import serializers

from .models import Course, Lesson


class AuthorSerializer(serializers.Serializer):
    """Serializer for author info in course responses."""

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for listing and creating courses with author info and lessons count."""

    author = AuthorSerializer(source='owner', read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'author',
            'lessons_count',
            'is_active',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        """
        Create a new course with owner set from request.user.

        Parameters:
        validated_data: dict - The validated data from the serializer.

        Returns:
        Course - The created course instance.
        """
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)


class LessonListSerializer(serializers.ModelSerializer):
    """Serializer for listing and creating lessons."""

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'content',
            'order',
            'indentation',
            'is_published',
            'course',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'order',
            'indentation',
            'is_published',
            'course',
            'created_at',
            'updated_at',
        ]