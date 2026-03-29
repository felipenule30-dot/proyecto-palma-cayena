from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Collection, Color, Size


def shop_list(request):
    products = Product.objects.filter(status=Product.STATUS_ACTIVE).prefetch_related('images', 'variants')
    
    # Filters
    category_slug = request.GET.get('categoria')
    collection_slug = request.GET.get('coleccion')
    color_ids = request.GET.getlist('color')
    size_ids = request.GET.getlist('talla')
    price_min = request.GET.get('precio_min')
    price_max = request.GET.get('precio_max')
    sort = request.GET.get('orden', 'recientes')
    
    selected_category = None
    selected_collection = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=selected_category)
    if collection_slug:
        selected_collection = get_object_or_404(Collection, slug=collection_slug, is_active=True)
        products = products.filter(collection=selected_collection)
    if color_ids:
        products = products.filter(colors__id__in=color_ids).distinct()
    if size_ids:
        products = products.filter(sizes__id__in=size_ids).distinct()
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    sort_map = {
        'recientes': '-created_at',
        'precio-asc': 'price',
        'precio-desc': '-price',
        'destacados': '-is_featured',
        'nombre': 'name',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(products, 12)
    page_number = request.GET.get('pagina', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': Category.objects.filter(is_active=True),
        'collections': Collection.objects.filter(is_active=True),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
        'selected_category': selected_category,
        'selected_collection': selected_collection,
        'selected_colors': [int(c) for c in color_ids],
        'selected_sizes': [int(s) for s in size_ids],
        'current_sort': sort,
        'price_min': price_min or '',
        'price_max': price_max or '',
        'total_products': paginator.count,
        'meta_title': 'Tienda — Vestidos de baño Palma Cayena',
        'meta_description': 'Descubre la colección de vestidos de baño de Palma Cayena. Bikinis y trajes de baño diseñados en el Caribe colombiano.',
    }
    return render(request, 'shop/shop_list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(
        status=Product.STATUS_ACTIVE, category=category
    ).prefetch_related('images', 'variants')

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('pagina', 1))

    return render(request, 'shop/shop_list.html', {
        'products': page_obj,
        'selected_category': category,
        'categories': Category.objects.filter(is_active=True),
        'collections': Collection.objects.filter(is_active=True),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
        'current_sort': 'recientes',
        'total_products': paginator.count,
        'meta_title': f'{category.meta_title or category.name} — Palma Cayena',
        'meta_description': category.meta_description or f'Vestidos de baño {category.name} de Palma Cayena.',
    })


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug, is_active=True)
    products = Product.objects.filter(
        status=Product.STATUS_ACTIVE, collection=collection
    ).prefetch_related('images', 'variants')

    return render(request, 'shop/collection_detail.html', {
        'collection': collection,
        'products': products,
        'meta_title': f'{collection.meta_title or collection.name} — Palma Cayena',
        'meta_description': collection.meta_description or '',
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('images', 'variants__size', 'variants__color', 'tags'),
        slug=slug, status=Product.STATUS_ACTIVE
    )
    
    related_products = Product.objects.filter(
        status=Product.STATUS_ACTIVE,
        category=product.category
    ).exclude(id=product.id).prefetch_related('images')[:4]

    sizes = product.variants.filter(is_active=True).values_list('size__id', 'size__name').distinct()
    colors = product.variants.filter(is_active=True).values_list('color__id', 'color__name', 'color__hex_code').distinct()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'sizes': [(s[0], s[1]) for s in sizes if s[0]],
        'colors': [(c[0], c[1], c[2]) for c in colors if c[0]],
        'meta_title': product.meta_title or f'{product.name} — Palma Cayena',
        'meta_description': product.meta_description or product.short_description,
    })
