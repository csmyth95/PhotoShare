# Sitemaps file from goddjango.com/23 robots and sitemaps
from django.contrib.sitemaps import Sitemap

from polls.models import Entry

# from django.contrib.sitemaps import Sitemap
from photologue.models import Gallery, Photo


class PollSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Entry.objects.all()

    def lastmod(self, obj):
        return obj.pub_date


# Note: Gallery and Photo are split, because there are use cases for having galleries
# in the sitemap, but not photos (e.g. if the photos are displayed with a lightbox).


class GallerySitemap(Sitemap):
    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Gallery.objects.on_site().is_public()

    def lastmod(self, obj):
        return obj.date_added


class PhotoSitemap(Sitemap):
    def items(self):
        # The following code is very basic and will probably cause problems with
        # large querysets.
        return Photo.objects.on_site().is_public()

    def lastmod(self, obj):
        return obj.date_added
