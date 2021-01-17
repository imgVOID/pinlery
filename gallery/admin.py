from django.contrib import admin

# Register your models here.
from django.contrib import admin
from gallery.models import Board, Section, Pin, SectionDescription, Profile


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('following_count', 'follower_count')
    pass


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'user')
    pass


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'board')
    pass


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    readonly_fields = ('height', 'width', 'height_s',
                       'height_m', 'width_s', 'width_m',
                       'image_url', 'small_image_url',
                       'medium_image_url', 'section')
    pass


@admin.register(SectionDescription)
class SectionDescriptionAdmin(admin.ModelAdmin):
    pass
