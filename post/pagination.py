from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_query_param = "page"  # Query parameter for page number
    page_size_query_param = "size"  # Query parameter for page size
    max_page_size = 10  # Maximum allowed page size
