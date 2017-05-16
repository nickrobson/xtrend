# article.py
# SENG3011 - Cool Bananas
#
# Displays an article

from django.template.loader import get_template

from ...server.views.article import APIArticleView

class XtrendArticleView(APIArticleView):

    def __init__(self):
        self.template = get_template('assets/xtrend/article.html')
