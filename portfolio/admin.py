from django.contrib import admin

from .models import (
	BlogPost,
	ChatbotKnowledge,
	ContactMessage,
	JourneyItem,
	PortfolioVisitorCount,
	Project,
	ProjectImage,
	PortfolioProfile,
	Skill,
)


class ProjectImageInline(admin.TabularInline):
	model = ProjectImage
	extra = 0


@admin.register(PortfolioProfile)
class PortfolioProfileAdmin(admin.ModelAdmin):
	list_display = ('name', 'role', 'email', 'updated_at')
	readonly_fields = ('updated_at',)

	def has_add_permission(self, request):
		return not PortfolioProfile.objects.exists()

	def has_delete_permission(self, request, obj=None):
		return False


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'featured', 'published', 'display_order')
	list_filter = ('category', 'featured', 'published')
	search_fields = ('title', 'summary', 'description', 'technologies')
	prepopulated_fields = {'slug': ('title',)}
	inlines = (ProjectImageInline,)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'status', 'visible', 'display_order')
	list_filter = ('category', 'status', 'visible')
	search_fields = ('name',)


@admin.register(JourneyItem)
class JourneyItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'organization', 'period', 'visible', 'display_order')
	list_filter = ('visible',)
	search_fields = ('title', 'organization', 'description')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'published', 'published_at')
	list_filter = ('category', 'published')
	search_fields = ('title', 'excerpt', 'content', 'tags')
	prepopulated_fields = {'slug': ('title',)}
	date_hierarchy = 'published_at'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'channel', 'subject', 'created_at', 'is_read')
	list_filter = ('channel', 'is_read', 'created_at')
	search_fields = ('name', 'email', 'subject', 'message')
	readonly_fields = ('created_at',)
	list_editable = ('is_read',)


@admin.register(ChatbotKnowledge)
class ChatbotKnowledgeAdmin(admin.ModelAdmin):
	list_display = ('title', 'active', 'display_order')
	list_filter = ('active',)
	search_fields = ('title', 'content')


@admin.register(PortfolioVisitorCount)
class PortfolioVisitorCountAdmin(admin.ModelAdmin):
	list_display = ('total_visitors',)

	def has_add_permission(self, request):
		return not PortfolioVisitorCount.objects.exists()

	def has_delete_permission(self, request, obj=None):
		return False