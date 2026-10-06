import json

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage, PortfolioVisitorCount, Project


@override_settings(ALLOWED_HOSTS=['localhost'])
class PortfolioVisitorCountTests(TestCase):
    def test_default_count_is_10003(self):
        counter = PortfolioVisitorCount.objects.create()

        self.assertEqual(counter.total_visitors, 10003)

    def test_counts_each_session_once(self):
        first_visitor = Client(HTTP_HOST='localhost')

        response = first_visitor.get('/', HTTP_HOST='localhost')
        self.assertContains(response, '10004')
        first_visitor.get('/', HTTP_HOST='localhost')
        self.assertEqual(PortfolioVisitorCount.objects.get(pk=1).total_visitors, 10004)

        second_visitor = Client(HTTP_HOST='localhost')
        second_visitor.get('/', HTTP_HOST='localhost')
        self.assertEqual(PortfolioVisitorCount.objects.get(pk=1).total_visitors, 10005)


@override_settings(ALLOWED_HOSTS=['localhost'])
class PortfolioInboxTests(TestCase):
    def test_public_project_and_seo_routes_render(self):
        client = Client(HTTP_HOST='localhost')
        paths = (
            '/',
            '/projects/django-ecommerce-platform/',
            '/journal/',
            '/robots.txt',
            '/sitemap.xml',
        )

        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(client.get(path, HTTP_HOST='localhost').status_code, 200)

    def test_text_style_message_is_saved_for_admin(self):
        client = Client(enforce_csrf_checks=True)
        page = client.get('/', HTTP_HOST='localhost')
        token = client.cookies['csrftoken'].value
        response = client.post(
            reverse('submit_contact'),
            data=json.dumps({
                'channel': 'text',
                'name': 'A visitor',
                'message': 'I would like to discuss a Django project.',
                'website': '',
            }),
            content_type='application/json',
            HTTP_HOST='localhost',
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(page.status_code, 200)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ContactMessage.objects.filter(channel='text', name='A visitor').exists())
        self.assertTrue(admin.site.is_registered(ContactMessage))

        admin_user = get_user_model().objects.create_superuser(
            username='portfolio_test_admin',
            email='admin@example.com',
            password='test-only-password',
        )
        client.force_login(admin_user)
        inbox = client.get(reverse('admin:portfolio_contactmessage_changelist'), HTTP_HOST='localhost')
        self.assertContains(inbox, 'A visitor')

    def test_contact_submission_validates_email(self):
        client = Client(HTTP_HOST='localhost')
        response = client.post(
            reverse('submit_contact'),
            data=json.dumps({
                'channel': 'contact',
                'name': 'A visitor',
                'email': 'not-an-email',
                'subject': 'Hello',
                'message': 'A valid message body.',
            }),
            content_type='application/json',
            HTTP_HOST='localhost',
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(ContactMessage.objects.exists())

    def test_read_only_project_api_returns_published_projects(self):
        project = Project.objects.create(
            title='Visible API project',
            slug='visible-api-project',
            summary='Published for API testing.',
            description='A test project.',
            category='django',
            published=True,
        )

        response = Client(HTTP_HOST='localhost').get('/api/projects/visible-api-project/', HTTP_HOST='localhost')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['slug'], project.slug)