from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import (StaticPage, HeroSection, HomepageBlock, BenefitItem,
                     Testimonial, FAQ, NewsletterSubscriber, JournalPost)
from .forms import NewsletterForm, ContactForm
from apps.shop.models import Product, Collection, Category


def home(request):
    hero = HeroSection.objects.filter(is_active=True).first()
    featured_products = Product.objects.filter(
        status='active', is_featured=True
    ).prefetch_related('images')[:8]
    new_products = Product.objects.filter(
        status='active', is_new=True
    ).prefetch_related('images')[:4]
    featured_collection = Collection.objects.filter(is_active=True, is_featured=True).first()
    categories = Category.objects.filter(is_active=True).order_by('order')[:6]
    blocks = HomepageBlock.objects.filter(is_active=True).order_by('order')
    benefits = BenefitItem.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:4]
    newsletter_form = NewsletterForm()

    context = {
        'hero': hero,
        'featured_products': featured_products,
        'new_products': new_products,
        'featured_collection': featured_collection,
        'categories': categories,
        'blocks': blocks,
        'benefits': benefits,
        'testimonials': testimonials,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    page = StaticPage.objects.filter(page_type='about', is_published=True).first()
    return render(request, 'pages/about.html', {'page': page,
        'meta_title': 'Nuestra historia — Palma Cayena',
        'meta_description': 'Conoce la historia de Palma Cayena, marca de vestidos de baño nacida en el Caribe colombiano.'
    })


def contact(request):
    form = ContactForm()
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()
    page = StaticPage.objects.filter(page_type='contact', is_published=True).first()
    return render(request, 'pages/contact.html', {
        'form': form, 'success': success, 'page': page,
        'meta_title': 'Contacto — Palma Cayena',
    })


def shipping(request):
    page = StaticPage.objects.filter(page_type='shipping', is_published=True).first()
    return render(request, 'pages/static_page.html', {
        'page': page, 'meta_title': 'Envíos — Palma Cayena',
    })


def returns(request):
    page = StaticPage.objects.filter(page_type='returns', is_published=True).first()
    return render(request, 'pages/static_page.html', {
        'page': page, 'meta_title': 'Cambios y devoluciones — Palma Cayena',
    })


def terms(request):
    page = StaticPage.objects.filter(page_type='terms', is_published=True).first()
    return render(request, 'pages/static_page.html', {
        'page': page, 'meta_title': 'Términos y condiciones — Palma Cayena',
    })


def privacy(request):
    page = StaticPage.objects.filter(page_type='privacy', is_published=True).first()
    return render(request, 'pages/static_page.html', {
        'page': page, 'meta_title': 'Política de privacidad — Palma Cayena',
    })


def faq(request):
    faqs = FAQ.objects.filter(is_active=True).order_by('category', 'order')
    faq_by_category = {}
    for faq in faqs:
        cat = faq.get_category_display()
        if cat not in faq_by_category:
            faq_by_category[cat] = []
        faq_by_category[cat].append(faq)
    return render(request, 'pages/faq.html', {
        'faq_by_category': faq_by_category,
        'meta_title': 'Preguntas frecuentes — Palma Cayena',
    })


def journal_list(request):
    posts = JournalPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'pages/journal.html', {
        'posts': posts,
        'meta_title': 'Journal — Palma Cayena',
    })


def journal_post(request, slug):
    post = get_object_or_404(JournalPost, slug=slug, is_published=True)
    return render(request, 'pages/journal_post.html', {
        'post': post,
        'meta_title': f'{post.meta_title or post.title} — Palma Cayena',
        'meta_description': post.meta_description or post.excerpt,
    })


def static_page(request, slug):
    page = get_object_or_404(StaticPage, slug=slug, is_published=True)
    return render(request, 'pages/static_page.html', {
        'page': page,
        'meta_title': f'{page.meta_title or page.title} — Palma Cayena',
        'meta_description': page.meta_description,
    })


@require_POST
def newsletter_subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                'name': form.cleaned_data.get('name', ''),
                'source': request.POST.get('source', 'homepage'),
            }
        )
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': False, 'errors': form.errors})
    return redirect(request.META.get('HTTP_REFERER', '/'))
