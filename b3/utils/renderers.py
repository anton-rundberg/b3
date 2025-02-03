from rest_framework import serializers
from rest_framework.renderers import BrowsableAPIRenderer, HTMLFormRenderer


class CustomHTMLFormRenderer(HTMLFormRenderer):
    """
    Override form renderer to avoid fetching related data

    Implemented so we can use DJDT to debug query performance easier
    """

    def __init__(self):
        super().__init__()
        self.default_style[serializers.RelatedField] = {
            "base_template": "input.html",
        }
        self.default_style[serializers.ManyRelatedField] = {
            "base_template": "input.html"
        }


class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    form_renderer_class = CustomHTMLFormRenderer
