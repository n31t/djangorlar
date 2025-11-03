import random
from typing import List
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from tasks.models import Project, Task, UserTask

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate test data for tasks app (Projects, Tasks, and User assignments)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)'
        )
        parser.add_argument(
            '--projects',
            type=int,
            default=5,
            help='Number of projects to create (default: 5)'
        )
        parser.add_argument(
            '--tasks-per-project',
            type=int,
            default=8,
            help='Number of tasks per project (default: 8)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data'
        )

    def handle(self, *args, **options):
        users_count = options['users']
        projects_count = options['projects']
        tasks_per_project = options['tasks_per_project']
        clear_existing = options['clear']

        if clear_existing:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        try:
            with transaction.atomic():
                users = self.create_users(users_count)
                self.stdout.write(
                    self.style.SUCCESS(f'Created {len(users)} users')
                )

                projects = self.create_projects(projects_count, users)
                self.stdout.write(
                    self.style.SUCCESS(f'Created {len(projects)} projects')
                )

                tasks = self.create_tasks(projects, tasks_per_project)
                self.stdout.write(
                    self.style.SUCCESS(f'Created {len(tasks)} tasks')
                )

                assignments = self.assign_users_to_tasks(tasks, users)
                self.stdout.write(
                    self.style.SUCCESS(f'Created {len(assignments)} user-task assignments')
                )

        except Exception as e:
            raise CommandError(f'Error generating data: {e}')

        self.stdout.write(
            self.style.SUCCESS('Data generation completed successfully!')
        )

    def clear_data(self):
        UserTask.objects.all().delete()
        Task.objects.all().delete()
        Project.objects.all().delete()

    def create_users(self, count: int) -> List[User]:
        users = []
        for i in range(count):
            username = f'testuser{i+1}'
            email = f'{username}@example.com'
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='testpass123',
                    first_name=f'Test{i+1}',
                    last_name='User'
                )
            users.append(user)
        
        return users

    def create_projects(self, count: int, users: List[User]) -> List[Project]:
        projects = []
        project_names = [
            'E-commerce Platform',
            'Mobile Banking App',
            'Learning Management System',
            'Social Media Dashboard',
            'Inventory Management',
            'Customer Support Portal',
            'Analytics Dashboard',
            'Content Management System',
            'Project Management Tool',
            'Real Estate Platform'
        ]

        for i in range(count):
            name = project_names[i % len(project_names)]
            if i >= len(project_names):
                name = f'Project {i+1}'
            
            if Project.objects.filter(name=name).exists():
                project = Project.objects.get(name=name)
            else:
                author = random.choice(users)
                project = Project.objects.create(
                    name=name,
                    author=author
                )
                
                project_users = random.sample(users, random.randint(2, min(5, len(users))))
                project.users.set(project_users)
            
            projects.append(project)
        
        return projects

    def create_tasks(self, projects: List[Project], tasks_per_project: int) -> List[Task]:
        tasks = []
        task_templates = [
            ('Setup project structure', 'Initialize the basic project structure and configuration'),
            ('Design database schema', 'Create and design the database schema for the application'),
            ('Implement user authentication', 'Add user registration, login, and authentication features'),
            ('Create API endpoints', 'Develop REST API endpoints for the application'),
            ('Build user interface', 'Design and implement the user interface components'),
            ('Add data validation', 'Implement input validation and error handling'),
            ('Write unit tests', 'Create comprehensive unit tests for the application'),
            ('Setup CI/CD pipeline', 'Configure continuous integration and deployment'),
            ('Performance optimization', 'Optimize application performance and database queries'),
            ('Security implementation', 'Implement security measures and best practices'),
            ('Documentation', 'Create comprehensive documentation for the project'),
            ('Code review', 'Review and refactor code for better maintainability'),
            ('Bug fixes', 'Fix identified bugs and issues'),
            ('Feature enhancement', 'Add new features and improve existing ones'),
            ('Deployment preparation', 'Prepare the application for production deployment')
        ]

        for project in projects:
            existing_tasks = Task.objects.filter(project=project).count()
            tasks_to_create = max(0, tasks_per_project - existing_tasks)
            
            for i in range(tasks_to_create):
                template = task_templates[i % len(task_templates)]
                name = f"{template[0]} - {project.name}"
                description = template[1]
                
                status = random.choice([
                    Task.STATUS_TODO,
                    Task.STATUS_IN_PROGRESS,
                    Task.STATUS_DONE
                ])
                
                parent = None
                if random.random() < 0.3 and tasks: 
                    parent = random.choice(tasks)
                
                task = Task.objects.create(
                    name=name,
                    description=description,
                    status=status,
                    project=project,
                    parent=parent
                )
                tasks.append(task)
        
        return tasks

    def assign_users_to_tasks(self, tasks: List[Task], users: List[User]) -> List[UserTask]:
        assignments = []
        
        for task in tasks:
            num_assignees = random.randint(1, min(3, len(users)))
            assignees = random.sample(users, num_assignees)
            
            for user in assignees:
                if not UserTask.objects.filter(task=task, user=user).exists():
                    assignment = UserTask.objects.create(
                        task=task,
                        user=user
                    )
                    assignments.append(assignment)
        
        return assignments
