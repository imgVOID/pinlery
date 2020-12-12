from django.contrib import admin

# Register your models here.
from django.contrib import admin
from gallery.models import Board, Section, Pin, SectionDescription


# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    pass


@admin.register(SectionDescription)
class SectionDescriptionAdmin(admin.ModelAdmin):
    pass

