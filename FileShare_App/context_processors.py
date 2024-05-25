from .models import Category

def categories(request):
    categories = Category.objects.all().order_by('category')
    return {'categories': categories}