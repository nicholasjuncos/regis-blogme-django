import datetime
from django.db import models
from django.contrib.auth import get_user_model
from model_utils.models import TimeStampedModel, StatusModel
from model_utils import Choices

User = get_user_model()


# class Tag(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name


class Post(TimeStampedModel, StatusModel):
    STATUS = Choices(
        ('D', 'draft'),
        ('P', 'published')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, default='D', max_length=1)
    post_date = models.DateField()
    title = models.CharField(max_length=100)
    title_sub_text = models.CharField(max_length=200, blank=True)
    subtitle1 = models.CharField(max_length=50)
    text1 = models.TextField()
    subtitle2 = models.CharField(max_length=50, blank=True)
    text2 = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="blog/posts/", null=True, blank=True)
    image1 = models.ImageField(upload_to="blog/posts/", null=True, blank=True)
    image1_title = models.CharField(max_length=50, blank=True)
    image1_text = models.CharField(max_length=200, blank=True)
    image2 = models.ImageField(upload_to="blog/posts/", null=True, blank=True)
    image2_title = models.CharField(max_length=50, blank=True)
    image2_text = models.CharField(max_length=200, blank=True)
    image3 = models.ImageField(upload_to="blog/posts/", null=True, blank=True)
    image3_title = models.CharField(max_length=50, blank=True)
    image3_text = models.CharField(max_length=200, blank=True)

    # @property
    # def like_count(self):
    #     return self.like_set.all().count()

    @property
    def description(self):
        return str(self.text1) + str(self.text2)

    @property
    def user(self):
        return self.author

    @property
    def active(self):
        if self.status == 'P' and datetime.date.today() <= self.post_date:
            return True
        else:
            return False

    @property
    def is_published(self):
        if self.status == 'P':
            return True
        return False

    @property
    def in_future(self):
        return self.post_date > datetime.date.today()

    def __str__(self):
        return self.title + ", " + str(self.post_date)


# TODO: Switch to this model
# class PostImage(models.Model):
#     post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="blog/posts/")
#     title = models.CharField(max_length=50, blank=True)
#     description = models.CharField(max_length=200, blank=True)


class Comment(TimeStampedModel):
    article = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)


class Reply(TimeStampedModel):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE)
    reply = models.CharField(max_length=1000)


# class Report(TimeStampedModel):
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True)

class Like(TimeStampedModel):
    article = models.ForeignKey(Post, related_name="likes", null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="likes", null=True, blank=True, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, related_name="likes", null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.datetime.now()
        return super(Like, self).save(*args, **kwargs)


class Follow(models.Model):
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authors_following")
    author_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_follower', 'author_followed')

    def __str__(self):
        return self.user_follower.__str__() + " following " + self.author_followed.__str__()
