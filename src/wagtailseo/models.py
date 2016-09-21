# -*- coding: utf-8 -*- 

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface)
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


__ALL__ = ['SEOSettings', 'SEOPageMixin']


class SummaryCard(blocks.StructBlock):
    """Twitter Summary Card

    Example:
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:site" content="@flickr" />
        <meta name="twitter:title" content="Small Island Developing States Photo Submission" />
        <meta name="twitter:description" content="View the album on Flickr." />
        <meta name="twitter:image" content="https://farm6.staticflickr.com/5510/14338202952_93595258ff_z.jpg" />
    """
    site = blocks.CharBlock(max_length=15, required=False)
    title = blocks.CharBlock(max_length=60, required=False)
    description = blocks.CharBlock(max_length=160, required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        template = 'wagtailseo/cards/summary.html'


class SummaryLargeImageCard(SummaryCard):
    """Twitter Summary Card with large image

    Example:
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@nytimes">
        <meta name="twitter:creator" content="@SarahMaslinNir">
        <meta name="twitter:title" content="Parade of Fans for Houston’s Funeral">
        <meta name="twitter:description" content="NEWARK - The guest list and parade of limousines with celebrities emerging from them seemed more suited to a red carpet event in Hollywood or New York than than a gritty stretch of Sussex Avenue near the former site of the James M. Baxter Terrace public housing project here.">
        <meta name="twitter:image" content="http://graphics8.nytimes.com/images/2012/02/19/us/19whitney-span/19whitney-span-articleLarge.jpg">
    """

    class Meta:
        template = 'wagtailseo/cards/summary_large_image.html'


class GooglePlayAppBlock(blocks.StructBlock):
    """Twitter Google Play Twitter Card specifications"""
    name = blocks.CharBlock(max_length=255)
    id = blocks.CharBlock(max_length=255)
    url = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = 'wagtailseo/cards/apps/google_play.html'


class IPhoneAppBlock(blocks.StructBlock):
    """Twitter iPhone App Twitter Card specifications"""
    name = blocks.CharBlock(max_length=255)
    id = blocks.IntegerBlock()
    url = blocks.CharBlock(max_length=255, required=False)

    class Meta:
        template = 'wagtailseo/cards/apps/iphone.html'


class IPadAppBlock(blocks.StructBlock):
    """Twitter iPad App Twitter Card specifications"""

    class Meta:
        template = 'wagtailseo/cards/apps/ipad.html'


class AppCard(blocks.StructBlock):
    """Twitter App Card

    Example:
        <meta name="twitter:card" content="app">
        <meta name="twitter:site" content="@TwitterDev">
        <meta name="twitter:description" content="Cannonball is the fun way to create and share stories and poems on your phone. Start with a beautiful image from the gallery, then choose words to complete the story and share it with friends.">
        <meta name="twitter:app:country" content="US">
        <meta name="twitter:app:name:iphone" content="Cannonball">
        <meta name="twitter:app:id:iphone" content="929750075">
        <meta name="twitter:app:url:iphone" content="cannonball://poem/5149e249222f9e600a7540ef">
        <meta name="twitter:app:name:ipad" content="Cannonball">
        <meta name="twitter:app:id:ipad" content="929750075">
        <meta name="twitter:app:url:ipad" content="cannonball://poem/5149e249222f9e600a7540ef">
        <meta name="twitter:app:name:googleplay" content="Cannonball">
        <meta name="twitter:app:id:googleplay" content="io.fabric.samples.cannonball">
        <meta name="twitter:app:url:googleplay" content="http://cannonball.fabric.io/poem/5149e249222f9e600a7540ef">
    """
    site = blocks.CharBlock(max_length=15, required=False)
    description = blocks.CharBlock(max_length=200, required=False)
    country = blocks.CharBlock(max_length=2, min_length=2)

    apps = blocks.StreamBlock([
        ('googleplay', GooglePlayAppBlock()),
        ('iphone', IPhoneAppBlock()),
        ('ipad', IPadAppBlock())
    ])

    class Meta:
        template = 'wagtailseo/cards/app.html'


class TwitterCard(blocks.StreamBlock):
    summary = SummaryCard()
    summary_large_image = SummaryLargeImageCard()
    app_card = AppCard()


@register_setting
class SEOSettings(BaseSetting):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    panels = [
        ImageChooserPanel('image')
    ]

    class Meta:
        verbose_name = ugettext('SEO')


class SEOPageMixin(Page):
    seo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=ugettext_lazy('Select image to override the default')
    )

    twitter_card = StreamField(TwitterCard)

    seo_panels = [
        ImageChooserPanel('seo_image'),
        StreamFieldPanel('twitter_card')
    ]

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels, heading=ugettext_lazy('Content')),
        ObjectList(Page.promote_panels, heading=ugettext_lazy('Promote')),
        ObjectList(seo_panels, heading=ugettext_lazy('SEO')),
        ObjectList(Page.settings_panels, heading=ugettext_lazy('Settings'), classname='settings')
    ])

    class Meta:
        abstract = True
