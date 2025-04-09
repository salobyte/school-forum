from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from PIL import Image



##### USERS #####
class StudentUser(AbstractUser):
        birth_date = models.DateField(null=True)
        objects = UserManager()

StudentUser = get_user_model()

class Profile(models.Model):
        user= models.OneToOneField(StudentUser, on_delete = models.CASCADE, related_name = "profile", primary_key=True)
        biography = models.TextField(max_length=500, blank=True, default = "This user hasn't added a biography yet.")
        avatar = models.ImageField(upload_to="media/avatars/", default = "media/avatars/default.jpg", null=True, blank=True)

        def __str__(self):
                return f"{self.user.username}'s Profile"

        def save(self, *args, **kwargs):
                if not self.avatar:
                        self.avatar = 'media/avatars/default.jpg'

                super().save(*args, **kwargs)

                if self.avatar:
                        if "default.jpg" not in self.avatar.name:
                                img = Image.open(self.avatar.path)
                                max_size = (170, 170)

                                if img.height > 170 or img.width > 170:
                                        img.thumbnail(max_size)
                                        img.save(self.avatar.path)
                else:
                        self.avatar.path = "media/avatars/default.jpg"

##### POSTS #####
class postInfo(models.Model):
        user = models.ForeignKey(StudentUser, on_delete = models.CASCADE, related_name = "posts", null=True)
        post_title = models.CharField(max_length = 500)
        post_body = models.TextField(max_length= 40000)
        post_created = models.DateTimeField()

        class Meta:
                verbose_name = "post"
                verbose_name_plural = "posts"
                ordering =["-post_created"]

        def __str__(self):
                return self.post_title
        
        @property
        def likes_count(self):
                return likes.objects.filter(post_id = self.id).count()
        
        @property
        def reply_count(self):
                return replies.objects.filter(post_id=self.id).count()

class likes(models.Model):
        class Meta:
                verbose_name = "likes"
                unique_together = ('user', 'post')
        post = models.ForeignKey(postInfo, on_delete=models.CASCADE, related_name="likes")
        user = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name="liked_posts")

        def __str__(self, post, user):
                return str(f"{user.username} liked {post.post_title}.")

##### REPLIES #####

class replies(models.Model):
        class Meta:
                verbose_name = "reply"
                verbose_name_plural = "replies"
        user = models.ForeignKey(StudentUser, on_delete = models.CASCADE, related_name = "replies", null=True)
        post = models.ForeignKey(postInfo, on_delete = models.CASCADE, related_name = "replies")
        reply_text = models.TextField(max_length= 10000)
        reply_created = models.DateTimeField()
        reply_index = models.PositiveIntegerField(default=0) 

        @property
        def reply_likes_count(self):
                return reply_likes.objects.filter(reply_id = self.id).count()


        def __str__(self):
                return str(self.reply_text)

class reply_likes(models.Model):
        class Meta:
                verbose_name = "likes"
                unique_together = ('user', 'reply')
        reply = models.ForeignKey(replies, on_delete=models.CASCADE, related_name="likes")
        user = models.ForeignKey(StudentUser, on_delete=models.CASCADE, related_name="liked_replies")

        def __str__(self, reply, user):
                return str(f"{user.username} liked {reply.reply_text}.")