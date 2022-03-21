import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

from ..common.fields import CIEmailField, CICharField


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = CICharField(
        _('username'),
        max_length=150,
        unique=True,  # Remove this when utilizing email auth
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = CIEmailField(_('email address'), unique=True)
    profile_photo = models.ImageField(upload_to='user/profile/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='user/cover/', blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True)
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('username',)

    # def __str__(self):
    #     return self.email  # Change to email if needed
        # if self.name:
        #     return self.name
        # if self.first_name and self.last_name:
        #     return self.first_name + " " + self.last_name
        # else:
        #     return "Anonymous User"

    @property
    def display_name(self):
        if self.full_name:
            return self.full_name
        return self.username

    @property
    def last_three_articles(self):
        today = datetime.date.today()
        return self.post_set.filter(status="P", post_date__lte=today).order_by("-post_date")[:3]

    @property
    def published_posts(self):
        today = datetime.date.today()
        return self.post_set.filter(status="P", post_date__lte=today).order_by("-post_date")

    @property
    def articles_liked(self):
        return self.likes.exclude(article=None).values_list('article', flat=True)

    @property
    def comments_liked(self):
        return self.likes.exclude(comment=None).values_list('comment', flat=True)

    @property
    def replies_liked(self):
        return self.likes.exclude(reply=None).values_list('reply', flat=True)

    @property
    def full_name(self):
        return (self.first_name + ' ' + self.last_name).strip()

    @property
    def followers_usernames(self):
        return self.followers.all().values_list('user_follower__username', flat=True)

    @property
    def following_usernames(self):
        return self.authors_following.all().values_list('author_followed__username', flat=True)

    def has_group(self, group):
        return self.groups.filter(name=group).exists()

    def initial_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email
        }
