from django.db import models


class Slider(models.Model):
    name = models.CharField(max_length=512)
    image = models.ImageField(upload_to="sliders/img/")
    is_visable = models.BooleanField(default=True)
    link = models.CharField(max_length=2048, null=True, blank=True)
    index = models.PositiveIntegerField(unique=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "slider"
        verbose_name_plural = "sliders"
        ordering = ("-index",)

    def __str__(self):
        return self.name
