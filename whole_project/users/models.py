from django.db import models
from django.contrib.auth import get_user_model

from PIL import Image

User = get_user_model()


# ----- Model for profile users -----
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.jpg', upload_to='profile_avatars')
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        max_size = 300
        if img.height > max_size or img.width > max_size:
            output_size = (max_size, max_size)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
# ----- End model  for profile users -----
