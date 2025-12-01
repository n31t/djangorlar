from math import fabs
from faker import Faker
import random
from typing import List
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import faker

from tasks.models import Project, Task, UserTask

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate test data for users app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10_000,
            help='Number of users to generate'
        )

    def handle(self, *args, **options):
        count = options['count']

        try:
            users = self.create_users(count)
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(users)} users')
            )

        except Exception as e:
            print(f'Error generating data: {e}')

        self.stdout.write(
            self.style.SUCCESS('Data generation completed successfully!')
        )


    def create_users(self, count: int):
        fake = Faker()

        for batching in range(0, count, 1000):
            batch_users = []

            for i in range(batching, batching + 1000):
                username = fake.user_name()
                email = fake.unique.email()
                password = fake.password()
                first_name = fake.first_name()
                date_of_birth = fake.date_of_birth()
                city = fake.city()
                country = fake.country()
                department = fake.random_element(elements=('IT', 'HR', 'Sales'))
                role = fake.random_element(elements=('admin', 'manager', 'employee'))
                salary = fake.random_number(digits = 5)
                phone = fake.phone_number()

                
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                else:
                    user = User(
                        username=username,
                        email=email,
                        password=password,
                        full_name=first_name,
                        phone=phone,
                        birth_date=date_of_birth,
                        city=city,
                        country=country,
                        department=department,
                        role=role,
                        salary = salary
                    )
                    batch_users.append(user)
                    print(f'Created user: {user}')
            User.objects.bulk_create(batch_users)