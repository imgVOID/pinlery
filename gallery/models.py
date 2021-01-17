from django.db import models
import uuid
from django.db.models import signals
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# Create your models here.
class Profile(models.Model):
    id_pinterest = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    username = models.CharField(
        max_length=25,
        default='pinterest',
        blank=False
    )
    full_name = models.CharField(
        max_length=40,
        default='',
        blank=True
    )
    listed_website_url = models.CharField(
        max_length=40,
        default="",
        blank=True
    )
    image_url = models.CharField(
        max_length=200,
        default='',
        blank=True
    )
    follower_count = models.IntegerField(
        default=0
    )
    following_count = models.IntegerField(
        default=0
    )
    active = models.BooleanField(
        blank=False,
        default=False,
        editable=True
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        from pinlery.init_api import Pinterest

        profile = Pinterest().get_user_overview(username=self.username)
        self.follower_count = profile['follower_count']
        self.following_count = profile['following_count']
        self.listed_website_url = str(profile['listed_website_url'])
        self.image_url = profile['image_medium_url']
        self.full_name = '{} {}'.format(profile['first_name'], profile['last_name'])
        self.id_pinterest = int(profile['id'])
        super().save(*args, **kwargs)


class Board(models.Model):
    id_pinterest = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=200
    )
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=200,
    )
    user = models.ForeignKey(
        to=Profile,
        on_delete=models.CASCADE,
        default=''
    )
    active = models.BooleanField(
        blank=False,
        default=False
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value)
        super().save(*args, **kwargs)


class Section(models.Model):
    id_pinterest = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=200
    )
    slug = models.SlugField(
        default='',
        max_length=200,
    )
    active = models.BooleanField(
        blank=False,
        default=False
    )
    board = models.ForeignKey(
        to=Board,
        on_delete=models.CASCADE
    )

    def title_custom_split(self):
        return self.title.replace('[ ', '').split(' ] ')

#    def slug_custom_split(self):
#        return self.title.replace('[ ', '').split(' ] ')[0].replace(' ', '-').lower()

    def save(self, *args, **kwargs):
        value = self.title.replace('[ ', '').split(' ] ')[0]
        self.slug = slugify(value)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} | {}".format(
            self.board.title,
            self.title
        )


class Pin(models.Model):
    id_pinterest = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=200,
        default=""
    )
    description = models.CharField(
        max_length=200,
        default=""
    )
    section = models.ForeignKey(
        to=Section,
        on_delete=models.CASCADE
    )
    image_url = models.CharField(
        max_length=200,
        default=""
    )
    height = models.PositiveIntegerField(
        default=0
    )
    width = models.PositiveIntegerField(
        default=0
    )
    small_image_url = models.CharField(
        max_length=200,
        default=""
    )
    height_s = models.PositiveIntegerField(
        default=0
    )
    width_s = models.PositiveIntegerField(
        default=0
    )
    medium_image_url = models.CharField(
        max_length=200,
        default=""
    )
    height_m = models.PositiveIntegerField(
        default=0
    )
    width_m = models.PositiveIntegerField(
        default=0
    )
    sort_position = models.PositiveIntegerField(
        default=0
    )
    color = models.CharField(
        max_length=8,
        default="#ffffff"
    )

    def __str__(self):
        pin_title = ""
        if len(self.title) < 2 and len(self.description) < 2:
            pin_title = "Untitled"
        elif len(self.title) < 2:
            pin_title = self.description[0:27]
        else:
            pin_title = self.title
        return "{} | {} | {}".format(
            self.section.board.title,
            self.section.title,
            pin_title
        )


class SectionDescription(models.Model):
    description = models.TextField(
        max_length=1500,
        blank=True,
        default=""
    )
    section = models.OneToOneField(
        'Section',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        try:
            return self.section.title
        except AttributeError:
            return self.description[0:100]
