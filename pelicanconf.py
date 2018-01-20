#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'melvyn'
SITENAME = 'Melvyn\'s blog'
SITEURL = 'https://melvyniandrag.github.io'
SITETITLE = 'Melvyn Ian Drag'
SITESUBTITLE = 'Programmer / Amateur Mathematician'
SITEDESCRIPTION = 'Melvyn\'s Thoughts and Writings'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('TestMakerSite', 'http://www.calistostudios.com'),
         ('DoggyMcDogFace', 'http://www.doggymcdogface.info/'),
         ('Resume', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('github', 'https://github.com/melvyniandrag'),
          ('linkedin', 'https://www.linkedin.com/in/melvyn-ian-drag-374613107/'),
          ('twitter', 'https://twitter.com/MelvynDrag'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme
THEME = "/home/melvyn/Desktop/website/pelican-themes/Flex"

# Flex config stuff
SITELOGO = SITEURL + '/theme/images/profile.png'
