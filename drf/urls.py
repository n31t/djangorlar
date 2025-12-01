from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet

app_name = 'drf'

router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix='education/courses',
    viewset=CourseViewSet,
    basename='course'
)


router.register(
    prefix='education/lessons',
    viewset=LessonViewSet,
    basename='lesson'
)

urlpatterns = router.urls