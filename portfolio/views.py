import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import F
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from .models import (
    BlogPost,
    ChatbotKnowledge,
    ContactMessage,
    JourneyItem,
    PortfolioProfile,
    PortfolioVisitorCount,
    Project,
    Skill,
)


def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    return HttpResponse(f'User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n', content_type='text/plain')


def page_not_found(request, exception):
    return render(request, 'portfolio/404.html', status=404)


def permission_denied(request, exception):
    return render(request, 'portfolio/403.html', status=403)


def server_error(request):
    return render(request, 'portfolio/500.html', status=500)


def home(request):
    profile = PortfolioProfile.objects.filter(pk=1).first()
    visitor_count, _ = PortfolioVisitorCount.objects.get_or_create(pk=1)
    if not request.session.get('portfolio_visit_counted'):
        PortfolioVisitorCount.objects.filter(pk=visitor_count.pk).update(total_visitors=F('total_visitors') + 1)
        visitor_count.refresh_from_db(fields=['total_visitors'])
        request.session['portfolio_visit_counted'] = True

    return render(request, 'portfolio/home.html', {
        'profile': profile,
        'portfolio_name': profile.name if profile else settings.PORTFOLIO_NAME,
        'portfolio_email': profile.email if profile else settings.PORTFOLIO_EMAIL,
        'portfolio_linkedin': profile.linkedin_url if profile else settings.PORTFOLIO_LINKEDIN,
        'portfolio_github': profile.github_url if profile else settings.PORTFOLIO_GITHUB,
        'portfolio_instagram': profile.instagram_url if profile else settings.PORTFOLIO_INSTAGRAM,
        'portfolio_facebook': profile.facebook_url if profile else settings.PORTFOLIO_FACEBOOK,
        'portfolio_phone': settings.PORTFOLIO_PHONE,
        'portfolio_role': profile.role if profile else 'Python Django Backend Developer',
        'visitor_count': visitor_count.total_visitors,
        'portfolio_location': profile.location if profile else settings.PORTFOLIO_LOCATION,
        'portfolio_education': profile.education if profile else settings.PORTFOLIO_EDUCATION,
        'portfolio_institution': profile.institution if profile else settings.PORTFOLIO_INSTITUTION,
        'projects': Project.objects.filter(published=True).prefetch_related('gallery'),
        'skill_groups': _skill_groups(Skill.objects.filter(visible=True)),
        'journey': JourneyItem.objects.filter(visible=True),
        'posts': BlogPost.objects.filter(published=True)[:3],
        'resume_available': bool(profile and profile.resume_file) or Path(settings.PORTFOLIO_RESUME).is_file(),
    })


def _skill_groups(skills):
    groups = {}
    for skill in skills:
        groups.setdefault(skill.get_category_display(), []).append(skill)
    return groups.items()


@require_GET
def project_detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related('gallery'), slug=slug, published=True)
    return render(request, 'portfolio/project_detail.html', {'project': project})


@require_GET
def blog_list(request):
    return render(request, 'portfolio/blog_list.html', {'posts': BlogPost.objects.filter(published=True)})


@require_GET
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, 'portfolio/blog_detail.html', {'post': post})


@require_GET
def resume_download(request):
    profile = PortfolioProfile.objects.filter(pk=1).first()
    if profile and profile.resume_file:
        return FileResponse(profile.resume_file.open('rb'), as_attachment=True, filename='Samyog-Panthee-Resume.pdf')
    resume = Path(settings.PORTFOLIO_RESUME)
    if not resume.is_file():
        return render(request, 'portfolio/resume_unavailable.html', {'profile': profile}, status=404)
    return FileResponse(resume.open('rb'), as_attachment=True, filename='Samyog-Panthee-Resume.pdf')


@require_POST
def submit_contact(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Send valid message details.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'error': 'Send valid message details.'}, status=400)

    values = [payload.get(key, '') for key in ('name', 'email', 'subject', 'message', 'channel')]
    if not all(isinstance(value, str) for value in values):
        return JsonResponse({'error': 'Message details must be text.'}, status=400)
    name, email, subject, message, channel = (value.strip() for value in values)
    if payload.get('website'):
        return JsonResponse({'message': 'Your message was received.'}, status=201)
    if not name or len(name) > 80 or not message or len(message) > 2000 or len(subject) > 160:
        return JsonResponse({'error': 'Add your name and a message under 2000 characters.'}, status=400)
    if channel not in {'contact', 'text', 'feedback'}:
        return JsonResponse({'error': 'Choose a valid message type.'}, status=400)
    if channel in {'contact', 'feedback'} and not email:
        return JsonResponse({'error': 'Add your email so Samyog can reply.'}, status=400)
    if email:
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'error': 'Enter a valid email address.'}, status=400)

    cache_key = f"portfolio-contact:{request.META.get('REMOTE_ADDR', 'unknown')}"
    message_count = cache.get(cache_key, 0)
    if message_count >= 5:
        return JsonResponse({'error': 'Too many messages. Please try again later.'}, status=429)
    if not cache.add(cache_key, 1, timeout=3600):
        cache.incr(cache_key)

    ContactMessage.objects.create(
        channel=channel,
        name=name,
        email=email,
        subject=subject,
        message=message,
    )
    return JsonResponse({'message': 'Your message was delivered to the site admin inbox.'}, status=201)


def _demo_reply(message):
    normalized = message.lower()
    profile = PortfolioProfile.objects.filter(pk=1).first()
    name = profile.name if profile else settings.PORTFOLIO_NAME
    email = profile.email if profile else settings.PORTFOLIO_EMAIL
    institution = profile.institution if profile else settings.PORTFOLIO_INSTITUTION
    location = profile.location if profile else settings.PORTFOLIO_LOCATION
    if any(word in normalized for word in ('education', 'college', 'study', 'student')):
        return f'{name} is a first-year IT Engineering student at {institution} in {location}.'
    if any(word in normalized for word in ('internship', 'available', 'hire', 'opportunity')):
        return 'Samyog is open to internship, junior backend, and freelance opportunities.'
    if any(word in normalized for word in ('visitor', 'visits', 'visitors')):
        count = PortfolioVisitorCount.objects.filter(pk=1).values_list('total_visitors', flat=True).first() or 10003
        return f'This portfolio has recorded {count} unique browser sessions.'
    if any(word in normalized for word in ('project', 'work', 'built', 'website')):
        projects = ', '.join(Project.objects.filter(published=True).values_list('title', flat=True))
        return f'{name}’s projects include {projects}.' if projects else f'{name} has built an e-commerce website and the Shree Resunga Secondary School website.'
    if any(word in normalized for word in ('skill', 'stack', 'technology', 'python', 'django', 'api')):
        skills = ', '.join(Skill.objects.filter(visible=True).values_list('name', flat=True))
        return f'{name} is learning and building with {skills}.'
    replies = (
        (('experience', 'career', 'job'), (f'{name} is an early-stage IT Engineering student. His project experience is shown here without claiming employment history.')),
        (('contact', 'email'), f'Email {name} at {email}, or use the contact form and social links.'),
        (('about', 'who', 'you'), f'I’m {name}, a first-year IT Engineering student in {location}, focused on Python and Django backend development.'),
    )
    for keywords, reply in replies:
        if any(keyword in normalized for keyword in keywords):
            return reply
    for entry in ChatbotKnowledge.objects.filter(active=True):
        terms = [term.lower() for term in entry.title.split() if len(term) > 3]
        if any(term in normalized for term in terms):
            return entry.content
    return 'I can answer questions about Samyog’s education, Django projects, skills, and availability. For anything else, use the contact form.'


@require_POST
def chat(request):
    try:
        payload = json.loads(request.body)
        message = payload.get('message', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Send a valid message.'}, status=400)

    if not isinstance(message, str) or not message or len(message) > 1000:
        return JsonResponse({'error': 'Message must be between 1 and 1000 characters.'}, status=400)

    if not settings.OPENAI_API_KEY:
        return JsonResponse({'reply': _demo_reply(message), 'mode': 'demo'})

    project_context = '\n'.join(
        f'{project.title}: {project.summary}'
        for project in Project.objects.filter(published=True)
    )
    knowledge_context = '\n'.join(ChatbotKnowledge.objects.filter(active=True).values_list('content', flat=True))
    profile = PortfolioProfile.objects.filter(pk=1).first()
    name = profile.name if profile else settings.PORTFOLIO_NAME
    education = profile.education if profile else settings.PORTFOLIO_EDUCATION
    institution = profile.institution if profile else settings.PORTFOLIO_INSTITUTION
    location = profile.location if profile else settings.PORTFOLIO_LOCATION

    body = json.dumps({
        'model': settings.OPENAI_MODEL,
        'instructions': f'You are Samyog AI, the portfolio assistant for {name}. Use only verified facts in this context. Samyog studies {education} at {institution} in {location}; he is a first-year student open to internship and junior backend opportunities. His focus is Python, Django, Django REST Framework, databases, APIs, and backend security. Projects: {project_context}. Additional editable knowledge: {knowledge_context}. Never invent project features, work history, credentials, or contact details. If information is missing, say you do not know and point visitors to the contact form.',
        'input': message,
        'max_output_tokens': 180,
    }).encode('utf-8')
    request_to_ai = Request(
        'https://api.openai.com/v1/responses',
        data=body,
        headers={
            'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urlopen(request_to_ai, timeout=20) as response:
            result = json.loads(response.read())
        reply = ''.join(
            block.get('text', '')
            for item in result.get('output', [])
            for block in item.get('content', [])
            if block.get('type') == 'output_text'
        ).strip()
        if not reply:
            return JsonResponse({'error': 'The assistant could not form a reply.'}, status=502)
        return JsonResponse({'reply': reply, 'mode': 'ai'})
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return JsonResponse({'error': 'The assistant is unavailable right now. Please try again.'}, status=502)