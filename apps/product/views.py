from django.views.generic import ListView, DetailView
from django.db.models import Avg,Count, F, ExpressionWrapper, FloatField
from .models import Category, Product


class ProductListView(ListView):
    template_name = "product/list.html"
    model = Product
    context_object_name = "products"
    category_breadcrumb = None
    last_index_breadcrumb = 0
    loop_rating = range(1,6)
    paginate_by = 12

    def filter_queryset(self, queryset):
        category_name = self.request.GET.get("category")
        min_rate = self.request.GET.get("rating")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        with_discount = self.request.GET.get("with_discount")

        if category_name:
            try:
                category = Category.objects.prefetch_related('childs').get(name=category_name)
                subcategories = category.get_all_subcategories()
                queryset = queryset.filter(category_id__in=subcategories)
                self.category_breadcrumb = category.path.split(" > ")
                self.last_index_breadcrumb = len(self.category_breadcrumb)  
            except Category.DoesNotExist:
                pass
        
        if min_rate:
            try:
                min_rate = int(min_rate)
                queryset = queryset.filter(average_score__gte=min_rate)
            except ValueError:
                pass
        
        if min_price:
            try:
                min_price = int(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass
        
        
        if max_price:
            try:
                max_price = int(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                pass

        if with_discount == "yes":
            queryset = queryset.exclude(price_after_discount=None)

        return queryset

    def sort_queryset(self, queryset):
        sorted_key = self.request.GET.get("sorted_by")
        match sorted_key:
            case "popular":
                queryset = queryset.annotate(likes_count=Count("likes")).order_by("-likes_count")
            case "oldest":
                queryset = queryset.order_by("created_at")
            case "-price":
                queryset = queryset.order_by("-price")
            case "price":
                queryset = queryset.order_by("price")
            case "discount":
                queryset = queryset.annotate(discount_num=ExpressionWrapper(((F("price") - F("price_after_discount")) / F("price")),output_field=FloatField(),)).order_by("-discount_num")
        return queryset

    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True).annotate(average_score=Avg("comments__score"))
        queryset = self.filter_queryset(queryset).order_by("-created_at")
        queryset = self.sort_queryset(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_breadcrumb"] = self.category_breadcrumb
        context["last_index_breadcrumb"] = self.last_index_breadcrumb
        context["loop_rating"] = self.loop_rating
        return context


class ProductDetailView(DetailView):
    template_name = "product/detail.html"
    model = Product
    loop_rating = range(1,6)
    context_object_name = "product"
        
    def get_queryset(self):
        queryset = self.model.objects.filter(is_active=True).annotate(average_score=Avg("comments__score")).prefetch_related("comments")

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loop_rating"] = self.loop_rating
        return context
