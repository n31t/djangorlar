from faker import Faker
from decimal import Decimal
from typing import List

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

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
            self.stdout.write(
                self.style.ERROR(f'Error generating data: {e}')
            )
            raise CommandError(f'Error generating data: {e}')
        
        self.stdout.write(
            self.style.SUCCESS('Data generation completed successfully!')
        )

    def create_users(self, count: int) -> List:
        """Create users in batches"""
        fake = Faker()
        created_users = []
        batch_size = 1000
        
        for batch_start in range(0, count, batch_size):
            batch_end = min(batch_start + batch_size, count)
            batch_users = []
            
            with transaction.atomic():
                for _ in range(batch_start, batch_end):
                    username = fake.user_name()
                    email = fake.unique.email()
                    password = fake.password(length=12)  # Ensure password meets validation
                    full_name = fake.name()
                    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
                    city = fake.city()
                    country = fake.country()
                    department = fake.random_element(elements=('IT', 'HR', 'Sales'))
                    role = fake.random_element(elements=('admin', 'manager', 'employee'))
                    salary = Decimal(fake.random_number(digits=5))
                    phone = fake.phone_number()
                    
                    # Check if email already exists (email is unique)
                    if User.objects.filter(email=email).exists():
                        continue
                    
                    # Use create_user to properly hash password
                    try:
                        user = User.objects.create_user(
                            email=email,
                            full_name=full_name,
                            password=password,
                            username=username,
                            phone=phone,
                            birth_date=birth_date,
                            city=city,
                            country=country,
                            department=department,
                            role=role,
                            salary=salary
                        )
                        batch_users.append(user)
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'Failed to create user {email}: {e}')
                        )
                        continue
                
                created_users.extend(batch_users)
                self.stdout.write(
                    self.style.SUCCESS(f'Created batch: {len(batch_users)} users (total: {len(created_users)})')
                )
        
        return created_users

