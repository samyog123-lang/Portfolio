from django.db import models
from django.urls import reverse


class PortfolioProfile(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=140)
    bio = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=180, blank=True)
    institution = models.CharField(max_length=180, blank=True)
    study_year = models.CharField(max_length=80, blank=True)
    email = models.EmailField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    profile_photo = models.ImageField(upload_to='profile/', blank=True)
    resume_file = models.FileField(upload_to='resume/', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'portfolio profile'
        verbose_name_plural = 'portfolio profile'

    def __str__(self):
        return self.name


class PortfolioVisitorCount(models.Model):
    total_visitors = models.PositiveBigIntegerField(default=10003)

    class Meta:
        verbose_name = 'portfolio visitor count'
        verbose_name_plural = 'portfolio visitor count'

    def __str__(self):
        return f'{self.total_visitors} portfolio visitors'


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('django', 'Django'),
        ('api', 'REST API'),
        ('python', 'Python'),
        ('flask', 'Flask'),
        ('web', 'Web application'),
    ]

    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=220)
    description = models.TextField()
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, default='django')
    thumbnail = models.ImageField(upload_to='projects/', blank=True)
    image_alt = models.CharField(max_length=180, blank=True)
    technologies = models.CharField(max_length=240, blank=True, help_text='Comma-separated technologies')
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    technical_highlights = models.TextField(blank=True, help_text='One highlight per line')
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    project_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('-featured', 'display_order', '-project_date', 'title')

    def __str__(self):
        return self.title

    @property
    def technology_list(self):
        return [technology.strip() for technology in self.technologies.split(',') if technology.strip()]

    @property
    def highlight_list(self):
        return [highlight.strip() for highlight in self.technical_highlights.splitlines() if highlight.strip()]

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='projects/gallery/')
    alt_text = models.CharField(max_length=180)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('display_order', 'pk')

    def __str__(self):
        return f'{self.project.title} image'


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('frontend', 'Frontend'),
        ('tools', 'Tools'),
        ('learning', 'Currently learning'),
    ]
    STATUS_CHOICES = [
        ('project', 'Building projects'),
        ('working', 'Working knowledge'),
        ('learning', 'Currently learning'),
    ]

    name = models.CharField(max_length=80)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='learning')
    display_order = models.PositiveSmallIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ('category', 'display_order', 'name')
        unique_together = ('name', 'category')

    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'


class JourneyItem(models.Model):
    title = models.CharField(max_length=140)
    organization = models.CharField(max_length=140, blank=True)
    period = models.CharField(max_length=40, blank=True)
    description = models.TextField()
    display_order = models.PositiveSmallIntegerField(default=0)
    visible = models.BooleanField(default=True)

    class Meta:
        ordering = ('display_order', 'pk')

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('django', 'Django'),
        ('python', 'Python'),
        ('backend', 'Backend development'),
        ('api', 'REST APIs'),
        ('learning', 'Learning journey'),
    ]

    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=260)
    content = models.TextField()
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, default='learning')
    featured_image = models.ImageField(upload_to='blog/', blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    published = models.BooleanField(default=False)
    reading_time_minutes = models.PositiveSmallIntegerField(default=3)
    tags = models.CharField(max_length=220, blank=True)

    class Meta:
        ordering = ('-published_at', '-pk')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


class ChatbotKnowledge(models.Model):
    title = models.CharField(max_length=140)
    content = models.TextField()
    active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('display_order', 'title')
        verbose_name = 'chatbot knowledge entry'

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    CHANNEL_CHOICES = [
        ('contact', 'Contact form'),
        ('text', 'Text-style message'),
        ('feedback', 'Feedback'),
    ]

    channel = models.CharField(max_length=12, choices=CHANNEL_CHOICES)
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=160, blank=True)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('is_read', '-created_at')

    def __str__(self):
        return f'{self.get_channel_display()} from {self.name}'