from django.db import migrations


def refine_descriptions(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    descriptions = {
        'django-ecommerce-platform': 'An e-commerce website built with Django and Python.',
        'shree-resunga-secondary-school': 'A website built for Shree Resunga Secondary School.',
        'flask-ecommerce-project': 'An e-commerce project built with Flask and Python.',
    }
    for slug, description in descriptions.items():
        Project.objects.filter(slug=slug).update(description=description)


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0004_seed_portfolio_content'),
    ]

    operations = [
        migrations.RunPython(refine_descriptions, migrations.RunPython.noop),
    ]