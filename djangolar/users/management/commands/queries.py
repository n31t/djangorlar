from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.models import (
    Q, F, BooleanField, Count, Avg, Max, Min, Sum, Value, CharField,
    Case, When, ExpressionWrapper, IntegerField, query
)
from django.db.models.functions import ExtractYear, Concat, Now
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal


CustomUser = get_user_model()


class Command(BaseCommand):
    help = 'Test all 50 CustomUser queries'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.CustomUser = CustomUser
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('Django ORM Query Tests - CustomUser Model'))
        self.run_all_queries()

    def run_all_queries(self):
        self.query_2_1()
        self.query_2_2()
        self.query_2_3()
        self.query_2_4()
        self.query_2_5()
        self.query_2_6()
        self.query_2_7()
        self.query_2_8()
        self.query_2_9()
        self.query_2_10()
        self.query_2_10()
        self.query_2_10()
        self.query_2_10()
        self.query_2_10()
        self.query_2_10()
        self.query_2_10()
        self.query_2_10()
        self.query_2_10()
        self.query_2_11()
        self.query_2_11()
        self.query_2_11()
        self.query_2_11()
        self.query_2_11()
        self.query_2_11()
        self.query_2_11()
        self.query_2_11()
        self.query_2_11()
        self.query_2_12()
        self.query_2_12()
        self.query_2_12()
        self.query_2_12()
        self.query_2_12()
        self.query_2_12()
        self.query_2_12()
        self.query_2_12()
        self.query_2_12()
        self.query_2_13()
        self.query_2_14()
        self.query_2_15()
        self.query_2_16()
        self.query_2_17()
        self.query_2_18()
        self.query_2_19()
        self.query_2_20()
        self.query_2_21()
        self.query_2_22()
        self.query_2_23()
        self.query_2_24()
        self.query_2_25()
        self.query_2_26()
        self.query_2_27()
        self.query_2_28()
        self.query_2_29()
        self.query_2_30()
        self.query_2_31()
        self.query_2_32()
        self.query_2_33()
        self.query_2_34()
        self.query_2_35()
        self.query_2_36()
        self.query_2_37()
        self.query_2_38()
        self.query_2_39()
        self.query_2_40()
        self.query_2_41()
        self.query_2_42()
        self.query_2_43()
        self.query_2_44()
        self.query_2_45()
        self.query_2_46()
        self.query_2_47()
        self.query_2_48()
        self.query_2_49()
        self.query_2_50()

    
    def query_2_1(self):
        self.stdout.write(self.style.WARNING('\n[2.1] Active Users'))
        queryset = self.CustomUser.objects.filter(is_active=True)
        self.print_results(queryset, ['email', 'full_name', 'is_active'])
    
    def query_2_2(self):
        self.stdout.write(self.style.WARNING('\n[2.2] Gmail Users'))
        queryset = self.CustomUser.objects.filter(email__endswith='@gmail.com')
        self.print_results(queryset, ['email', 'full_name'])
    
    def query_2_3(self):
        self.stdout.write(self.style.WARNING('\n[2.3] Users from Almaty'))
        queryset = self.CustomUser.objects.filter(city='Almaty')
        self.print_results(queryset, ['email', 'city', 'country'])
    
    def query_2_4(self):
        self.stdout.write(self.style.WARNING('\n[2.4] Users NOT from Almaty'))
        queryset = self.CustomUser.objects.exclude(city='Almaty')
        self.print_results(queryset, ['email', 'city'])
    
    def query_2_5(self):
        self.stdout.write(self.style.WARNING('\n[2.5] High Salary (> 500,000)'))
        queryset = self.CustomUser.objects.filter(salary__gt=500000)
        self.print_results(queryset, ['email', 'salary'])
    
    def query_2_6(self):
        self.stdout.write(self.style.WARNING('\n[2.6] IT Department + Kazakhstan'))
        queryset = self.CustomUser.objects.filter(
            department='it',
            country='Kazakhstan'
        )
        self.print_results(queryset, ['email', 'department', 'country'])
    
    def query_2_7(self):
        self.stdout.write(self.style.WARNING('\n[2.7] NULL Birth Date'))
        queryset = self.CustomUser.objects.filter(birth_date__isnull=True)
        self.print_results(queryset, ['email', 'birth_date'])
    
    def query_2_8(self):
        self.stdout.write(self.style.WARNING('\n[2.8] Name starts with "A"'))
        queryset = self.CustomUser.objects.filter(full_name__istartswith='A')
        self.print_results(queryset, ['email', 'full_name'])
    
    def query_2_9(self):
        self.stdout.write(self.style.WARNING('\n[2.9] Total Users Count'))
        count = self.CustomUser.objects.count()
        self.stdout.write(f'Total users: {count}')
    
    def query_2_10(self):
        self.stdout.write(self.style.WARNING('\n[2.10] First 20 Users (newest first)'))
        queryset = self.CustomUser.objects.order_by('-created_at')[:20]
        self.print_results(queryset, ['email', 'created_at'])
    
    def query_2_11(self):
        self.stdout.write(self.style.WARNING('\n[2.11] Distinct Cities'))
        cities = self.CustomUser.objects.values_list(
            'city', flat=True
        ).distinct()
        self.stdout.write(f'Found {cities.count()} distinct cities:')
        for city in list(cities)[:self.limit]:
            self.stdout.write(f'  - {city or "NULL"}')
    
    def query_2_12(self):
        self.stdout.write(self.style.WARNING('\n[2.12] Sales Department Count'))
        count = self.CustomUser.objects.filter(department='sales').count()
        self.stdout.write(f'Sales department users: {count}')
    
    def query_2_13(self):
        self.stdout.write(self.style.WARNING('\n[2.13] Recent Logins (Last 7 days)'))
        seven_days_ago = timezone.now() - timedelta(days=7)
        queryset = self.CustomUser.objects.filter(last_login__gte=seven_days_ago)
        self.print_results(queryset, ['email', 'last_login'])
    
    def query_2_14(self):
        self.stdout.write(self.style.WARNING('\n[2.14] Name contains "bek"'))
        queryset = self.CustomUser.objects.filter(
            Q(full_name__icontains='bek') | Q(username__icontains='bek')
        )
        self.print_results(queryset, ['email', 'full_name', 'username'])
    
    def query_2_15(self):
        self.stdout.write(self.style.WARNING('\n[2.15] Salary Range (300k - 700k)'))
        queryset = self.CustomUser.objects.filter(
            salary__gte=300000,
            salary__lte=700000
        )
        self.print_results(queryset, ['email', 'salary'])
    
    def query_2_16(self):
        self.stdout.write(self.style.WARNING('\n[2.16] IT, HR, Finance Departments'))
        queryset = self.CustomUser.objects.filter(
            department__in=['it', 'hr', 'finance']
        )
        self.print_results(queryset, ['email', 'department'])
    
    def query_2_17(self):
        self.stdout.write(self.style.WARNING('\n[2.17] Users per Department'))
        stats = self.CustomUser.objects.values('department').annotate(
            count=Count('id')
        )
        self.print_aggregated_results(stats, ['department', 'count'])
    
    def query_2_18(self):
        self.stdout.write(self.style.WARNING('\n[2.18] Users per Department (sorted)'))
        stats = self.CustomUser.objects.values('department').annotate(
            count=Count('id')
        ).order_by('-count')
        self.print_aggregated_results(stats, ['department', 'count'])
    
    def query_2_19(self):
        self.stdout.write(self.style.WARNING('\n[2.19] Top 5 Cities by User Count'))
        stats = self.CustomUser.objects.values('city').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        self.print_aggregated_results(stats, ['city', 'count'], numbered=True)
    
    def query_2_20(self):
        self.stdout.write(self.style.WARNING('\n[2.20] Never Logged In'))
        queryset = self.CustomUser.objects.filter(last_login__isnull=True)
        self.print_results(queryset, ['email', 'created_at', 'last_login'])
    
    def query_2_21(self):
        self.stdout.write(self.style.WARNING('\n[2.21] Average Salary'))
        result = self.CustomUser.objects.aggregate(avg_salary=Avg('salary'))
        avg = result['avg_salary'] or 0
        self.stdout.write(f'Average salary: {avg:,.2f}')
    
    def query_2_22(self):
        self.stdout.write(self.style.WARNING('\n[2.22] Salary Range (Max/Min)'))
        result = self.CustomUser.objects.aggregate(
            max_salary=Max('salary'),
            min_salary=Min('salary')
        )
        self.stdout.write(f'Maximum salary: {result["max_salary"] or 0:,.2f}')
        self.stdout.write(f'Minimum salary: {result["min_salary"] or 0:,.2f}')
    
    def query_2_23(self):
        self.stdout.write(self.style.WARNING('\n[2.23] Phone contains "+7"'))
        queryset = self.CustomUser.objects.filter(phone__contains='+7')
        self.print_results(queryset, ['email', 'phone'])
    
    def query_2_24(self):
        self.stdout.write(self.style.WARNING('\n[2.24] Annotate with Computed Name'))
        queryset = self.CustomUser.objects.annotate(
            computed_name=Concat(
                'username', Value(' '), 'full_name',
                output_field=CharField()
            )
        )
        self.print_results(queryset, ['email', 'username', 'full_name'], annotated=['computed_name'])
    
    def query_2_25(self):
        self.stdout.write(self.style.WARNING('\n[2.25] Annotate with Birth Year'))
        queryset = self.CustomUser.objects.annotate(
            birth_year=ExtractYear('birth_date')
        ).order_by('birth_year')
        self.print_results(queryset, ['email', 'birth_date'], annotated=['birth_year'])
    
    def query_2_26(self):
        self.stdout.write(self.style.WARNING('\n[2.26] May Birthdays'))
        queryset = self.CustomUser.objects.filter(birth_date__month=5)
        self.print_results(queryset, ['email', 'birth_date'])
    
    def query_2_27(self):
        self.stdout.write(self.style.WARNING('\n[2.27] High-Earning Managers'))
        queryset = self.CustomUser.objects.filter(
            role='manager',
            salary__gt=400000
        )
        self.print_results(queryset, ['email', 'role', 'salary'])
    
    def query_2_28(self):
        self.stdout.write(self.style.WARNING('\n[2.28] Employees OR HR Department'))
        queryset = self.CustomUser.objects.filter(
            Q(role='employee') | Q(department='hr')
        )
        self.print_results(queryset, ['email', 'role', 'department'])
    
    def query_2_29(self):
        self.stdout.write(self.style.WARNING('\n[2.29] Active Users per City'))
        stats = self.CustomUser.objects.filter(
            is_active=True
        ).values('city').annotate(
            count=Count('id')
        )
        self.print_aggregated_results(stats, ['city', 'count'])
    
    def query_2_30(self):
        self.stdout.write(self.style.WARNING('\n[2.30] 10 Earliest Users'))
        queryset = self.CustomUser.objects.order_by('created_at')[:10]
        self.print_results(queryset, ['email', 'created_at'])
    
    def query_2_31(self):
        self.stdout.write(self.style.WARNING('\n[2.31] City starts with "A" + High Salary'))
        queryset = self.CustomUser.objects.filter(
            city__istartswith='A',
            salary__gt=300000
        )
        self.print_results(queryset, ['email', 'city', 'salary'])
    
    def query_2_32(self):
        self.stdout.write(self.style.WARNING('\n[2.32] NULL or Empty Department'))
        queryset = self.CustomUser.objects.filter(
            Q(department__isnull=True) | Q(department='')
        )
        self.print_results(queryset, ['email', 'department'])
    
    def query_2_33(self):
        self.stdout.write(self.style.WARNING('\n[2.33] Stats by Country'))
        stats = self.CustomUser.objects.values('country').annotate(
            user_count=Count('id'),
            avg_salary=Avg('salary')
        )
        self.print_aggregated_results(stats, ['country', 'user_count', 'avg_salary'])
    
    def query_2_34(self):
        self.stdout.write(self.style.WARNING('\n[2.34] Staff Users (by last login)'))
        queryset = self.CustomUser.objects.filter(
            is_staff=True
        ).order_by('-last_login')
        self.print_results(queryset, ['email', 'is_staff', 'last_login'])
    
    def query_2_35(self):
        self.stdout.write(self.style.WARNING('\n[2.35] Email NOT containing "example.com"'))
        queryset = self.CustomUser.objects.exclude(
            email__contains='example.com'
        )
        self.print_results(queryset, ['email'])
    
    def query_2_36(self):
        self.stdout.write(self.style.WARNING('\n[2.36] Above Average Salary'))
        avg_sal = self.CustomUser.objects.aggregate(avg=Avg('salary'))['avg'] or 0
        self.stdout.write(f'Average salary: {avg_sal:,.2f}')
        queryset = self.CustomUser.objects.filter(salary__gt=avg_sal)
        self.print_results(queryset, ['email', 'salary'])
    
    def query_2_37(self):
        self.stdout.write(self.style.WARNING('\n[2.37] Duplicate Emails'))
        stats = self.CustomUser.objects.values('email').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        self.print_aggregated_results(stats, ['email', 'count'])
    
    def query_2_38(self):
        self.stdout.write(self.style.WARNING('\n[2.38] Users with Salary Levels'))
        queryset = self.CustomUser.objects.annotate(
            salary_level=Case(
                When(salary__lt=300000, then=Value('low')),
                When(salary__gte=300000, salary__lte=700000, then=Value('medium')),
                When(salary__gt=700000, then=Value('high')),
                default=Value('unknown'),
                output_field=CharField()
            )
        ).order_by('salary_level')
        self.print_results(queryset, ['email', 'salary'], annotated=['salary_level'])
    
    def query_2_39(self):
        self.stdout.write(self.style.WARNING('\n[2.39] Users Created This Year'))
        current_year = timezone.now().year
        queryset = self.CustomUser.objects.filter(
            created_at__year=current_year
        )
        self.print_results(queryset, ['email', 'created_at'])
    
    def query_2_40(self):
        self.stdout.write(self.style.WARNING('\n[2.40] Total Payroll per Department'))
        stats = self.CustomUser.objects.values('department').annotate(
            total_payroll=Sum('salary')
        )
        self.print_aggregated_results(stats, ['department', 'total_payroll'])
    
    def query_2_41(self):
        self.stdout.write(self.style.WARNING('\n[2.41] IT Department - Never Logged In'))
        queryset = self.CustomUser.objects.filter(
            department='it',
            last_login__isnull=True
        )
        self.print_results(queryset, ['email', 'department', 'last_login'])
    
    def query_2_42(self):
        self.stdout.write(self.style.WARNING('\n[2.42] Kazakhstan - Incomplete City'))
        queryset = self.CustomUser.objects.filter(
            country='Kazakhstan'
        ).filter(
            Q(city__isnull=True) | Q(city='')
        )
        self.print_results(queryset, ['email', 'country', 'city'])
    
    def query_2_43(self):
        self.stdout.write(self.style.WARNING('\n[2.43] Born before 1990 + Has Salary'))
        queryset = self.CustomUser.objects.filter(
            birth_date__lt=datetime(1990, 1, 1).date(),
            salary__isnull=False
        )
        self.print_results(queryset, ['email', 'birth_date', 'salary'])
    
    def query_2_44(self):
        self.stdout.write(self.style.WARNING('\n[2.44] Years Since Joined'))
        queryset = self.CustomUser.objects.annotate(
            days_since_joined=ExpressionWrapper(
                Now() - F('created_at'),
                output_field=IntegerField()
            )
        )
        self.print_results(queryset, ['email', 'created_at'], annotated=['days_since_joined'])
    
    def query_2_45(self):
        self.stdout.write(self.style.WARNING('\n[2.45] Sales + Gmail + High Salary'))
        queryset = self.CustomUser.objects.filter(
            department='sales',
            email__endswith='@gmail.com',
            salary__gt=350000
        )
        self.print_results(queryset, ['email', 'department', 'salary'])
    
    def query_2_46(self):
        self.stdout.write(self.style.WARNING('\n[2.46] Multi-level Ordering (Country, -Salary)'))
        queryset = self.CustomUser.objects.order_by('country', '-salary')
        self.print_results(queryset, ['email', 'country', 'salary'])
    
    def query_2_47(self):
        self.stdout.write(self.style.WARNING('\n[2.47] Roles with > 100 Users'))
        stats = self.CustomUser.objects.values('role').annotate(
            count=Count('id')
        ).filter(count__gt=100)
        self.print_aggregated_results(stats, ['role', 'count'])
    
    def query_2_48(self):
        self.stdout.write(self.style.WARNING('\n[2.48] Inconsistent Login Data'))
        queryset = self.CustomUser.objects.filter(
            last_login__lt=F('created_at')
        )
        self.print_results(queryset, ['email', 'created_at', 'last_login'])
    
    def query_2_49(self):
        self.stdout.write(self.style.WARNING('\n[2.49] Annotate with is_senior Flag'))
        queryset = self.CustomUser.objects.annotate(
            is_senior=Case(
                When(birth_date__lt=datetime(1985, 1, 1).date(), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )
        self.print_results(queryset, ['email', 'birth_date'], annotated=['is_senior'])
    
    def query_2_50(self):
        self.stdout.write(self.style.WARNING('\n[2.50] Departments (≥20 users) by Avg Salary'))
        stats = self.CustomUser.objects.values('department').annotate(
            user_count=Count('id'),
            avg_salary=Avg('salary')
        ).filter(
            user_count__gte=20
        ).order_by('-avg_salary')
        self.print_aggregated_results(stats, ['department', 'user_count', 'avg_salary'])
   
    
    
    def print_results(self, queryset, fields):
        for obj in queryset:
            values = []
            for field in fields:
                value = getattr(obj, field, None)
                if value is not None:
                    values.append(f'{field}={value}')
            self.stdout.write(f'  - {", ".join(values)}')
        