from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=64,unique=True)
    path = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="childs", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if self.parent:
            self.path = f"{self.parent.path} > {self.name}"
        else:
            self.path = self.name
        super().save(*args, **kwargs)

    
    def get_all_subcategories(self):
        subcategories = []
        stack = [self]
        while stack:
            current = stack.pop()
            subcategories.append(current.id)
            stack.extend(current.childs.all())
        return subcategories


class Product(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, db_index=True)
    image = models.ImageField(upload_to="products/img/")
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2, db_index=True)
    price_after_discount = models.DecimalField(max_digits=10,decimal_places=2, blank=True,null=True)
    stock = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField("account.User", blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products", null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ("-created_at",)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"pk": self.id})
    
    @property
    def discount_percentage(self):
        return round(((self.price - self.price_after_discount) / self.price) * 100)


class Comment(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1024)
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} - {self.product}"