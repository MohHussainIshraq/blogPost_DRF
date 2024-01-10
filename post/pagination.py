from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class StandardResultsSetPagination(PageNumberPagination):
    page_size = getattr(settings, 'PAGINATION_SIZE', 2)
