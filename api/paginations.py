from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class customPagination(PageNumberPagination):
    # page_size_query_param = 'page_size'
    # page_query_param = 'page_num'
    page_size_query_param = 'limit'
    page_size = 2
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'status': 200,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        })