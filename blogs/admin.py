from django.contrib import admin
from .models import Blogs, Comments

# Inline model to show comments inside Blog admin page
class BlogCommentInline(admin.TabularInline): # TabularInline is the default inline form layout & can be replaced with StackedInline for a different layout
    model = Comments
    extra = 1  # Show 1 extra blank comment inline

@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ['title', 'content']
    inlines = [BlogCommentInline]
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['comment', 'blog']