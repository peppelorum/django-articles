from django.contrib.syndication.feeds import Feed
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from .models import Article, Category

SITE = Site.objects.get_current()

class LatestEntries(Feed):
    link = "/blog/"
    description = "Updates to my blog"

    def title(self):
        return "%s Articles" % SITE.name

    def items(self):
        return Article.objects.active().order_by('-publish_date')[:5]

    def item_author_name(self, item):
        return item.author.username

    def item_categories(self, item):
        return [c.name for c in item.categories.all()] + [keyword.strip() for keyword in item.keywords.split(',')]

    def item_pubdate(self, item):
        return item.publish_date

class CategoryFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise FeedDoesNotExist
        return Category.objects.active().get(slug__exact=bits[0])

    def title(self, obj):
        return "%s: Newest Articles Tagged '%s'" % (SITE.name, obj.slug)

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Articles Tagged '%s'" % obj.slug

    def items(self, obj):
        return self.item_set(obj)[:10]

    def item_set(self, obj):
        return obj.article_set.active().order_by('-publish_date')

    def item_author_name(self, item):
        return item.author.username

    def item_author_link(self, item):
        return reverse('articles_by_author', args=[item.author.username])

    def item_pubdate(self, item):
        return item.publish_date