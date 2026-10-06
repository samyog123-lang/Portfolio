from django.db import migrations


def seed_portfolio(apps, schema_editor):
    PortfolioProfile = apps.get_model('portfolio', 'PortfolioProfile')
    PortfolioVisitorCount = apps.get_model('portfolio', 'PortfolioVisitorCount')
    Project = apps.get_model('portfolio', 'Project')
    Skill = apps.get_model('portfolio', 'Skill')
    JourneyItem = apps.get_model('portfolio', 'JourneyItem')
    ChatbotKnowledge = apps.get_model('portfolio', 'ChatbotKnowledge')

    PortfolioProfile.objects.get_or_create(
        pk=1,
        defaults={
            'name': 'Samyog Panthee',
            'role': 'Python Django Backend Developer',
            'bio': 'First-year Information Technology Engineering student focused on Python, Django, backend engineering, and REST APIs.',
            'location': 'Nepal',
            'education': "Bachelor's in Information Technology Engineering",
            'institution': 'NCIT — Nepal College of Information Technology',
            'study_year': 'First year',
            'email': 'samyogpanthee238@gmail.com',
            'github_url': 'https://github.com/samyog123-lang',
            'linkedin_url': 'https://www.linkedin.com/in/samyog-panthee-87946442b/',
            'facebook_url': 'https://www.facebook.com/samyogpanthee238',
            'instagram_url': 'https://www.instagram.com/samyogpanthee238/',
            'profile_photo': 'profile/profile.jpg',
        },
    )
    PortfolioVisitorCount.objects.get_or_create(pk=1, defaults={'total_visitors': 10003})

    projects = [
        {
            'slug': 'django-ecommerce-platform',
            'title': 'Django E-Commerce Platform',
            'summary': 'An e-commerce website built with Django.',
            'description': 'A Django e-commerce project built by Samyog. Update this entry with the exact implemented features, repository, and live demo before publishing those details.',
            'category': 'django',
            'technologies': 'Python, Django',
            'featured': True,
            'display_order': 1,
        },
        {
            'slug': 'shree-resunga-secondary-school',
            'title': 'Shree Resunga Secondary School Website',
            'summary': 'A website built for Shree Resunga Secondary School.',
            'description': 'A school website built by Samyog. Add the exact implemented pages, repository, and live URL in Django Admin.',
            'category': 'django',
            'technologies': 'Python, Django',
            'featured': True,
            'display_order': 2,
        },
        {
            'slug': 'flask-ecommerce-project',
            'title': 'Flask E-Commerce Project',
            'summary': 'An e-commerce project built with Flask.',
            'description': 'A Flask e-commerce project. Add the exact implemented features, repository, and live demo in Django Admin.',
            'category': 'flask',
            'technologies': 'Python, Flask',
            'featured': False,
            'display_order': 3,
        },
    ]
    for project in projects:
        Project.objects.get_or_create(slug=project['slug'], defaults=project)

    skills = [
        ('Python', 'backend', 'project', 1),
        ('Django', 'backend', 'project', 2),
        ('Flask', 'backend', 'project', 3),
        ('Django REST Framework', 'backend', 'learning', 4),
        ('REST APIs', 'backend', 'learning', 5),
        ('Django ORM', 'database', 'learning', 1),
        ('SQLite', 'database', 'working', 2),
        ('PostgreSQL', 'database', 'learning', 3),
        ('HTML', 'frontend', 'project', 1),
        ('CSS', 'frontend', 'project', 2),
        ('JavaScript', 'frontend', 'learning', 3),
        ('Git', 'tools', 'learning', 1),
        ('GitHub', 'tools', 'project', 2),
        ('VS Code', 'tools', 'project', 3),
        ('Postman', 'tools', 'learning', 4),
        ('API architecture', 'learning', 'learning', 1),
        ('Backend security', 'learning', 'learning', 2),
        ('Data science and AI/ML', 'learning', 'learning', 3),
    ]
    for name, category, status, display_order in skills:
        Skill.objects.get_or_create(
            name=name,
            category=category,
            defaults={'status': status, 'display_order': display_order},
        )

    journey = [
        ('Information Technology Engineering', 'NCIT — Nepal College of Information Technology', '2026 — First year', 'Started a Bachelor\'s degree in Information Technology Engineering.'),
        ('Python development', 'Project learning', 'Building', 'Developing Python fundamentals through hands-on web projects.'),
        ('Django development', 'Project learning', 'Building', 'Built e-commerce and school website projects with Django.'),
        ('Backend engineering', 'Current focus', 'Ongoing', 'Studying databases, authentication, API design, and secure backend patterns.'),
        ('Django REST Framework', 'Current learning', 'Ongoing', 'Advancing toward API development with Django REST Framework.'),
    ]
    for display_order, (title, organization, period, description) in enumerate(journey, start=1):
        JourneyItem.objects.get_or_create(
            title=title,
            defaults={
                'organization': organization,
                'period': period,
                'description': description,
                'display_order': display_order,
            },
        )

    knowledge = [
        ('Profile', 'Samyog Panthee is a first-year Information Technology Engineering student at NCIT in Nepal. He is focused on Python and Django backend development and is open to internships and junior backend opportunities.'),
        ('Projects', 'Samyog has built a Django e-commerce website, the Shree Resunga Secondary School website, and a Flask e-commerce project. Do not invent unlisted features.'),
        ('Skills', 'Samyog is building skills in Python, Django, Flask, Django REST Framework, REST APIs, the Django ORM, databases, frontend fundamentals, and developer tools.'),
    ]
    for display_order, (title, content) in enumerate(knowledge, start=1):
        ChatbotKnowledge.objects.get_or_create(
            title=title,
            defaults={'content': content, 'display_order': display_order},
        )


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0003_portfolioprofile'),
    ]

    operations = [
        migrations.RunPython(seed_portfolio, migrations.RunPython.noop),
    ]