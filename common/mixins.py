from django.db import models
from django.utils.text import slugify

class SlugMixIn(models.Model):
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class AddedOnMixIn(models.Model):
    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


