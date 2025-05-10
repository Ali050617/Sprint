from rest_framework.pagination import PageNumberPagination


class FollowersListPagination(PageNumberPagination):
    page_size = 10

class FollowingListPagination(PageNumberPagination):
    page_size = 10