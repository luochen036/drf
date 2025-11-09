from rest_framework.pagination import PageNumberPagination

# 自定义分页器
class MyPageNumberPagination(PageNumberPagination):
    page_size = 2  # 每页默认10条数据
    page_size_query_param = "page_size"  # 可以通过查询参数指定每页数据量
    max_page_size = 100  # 每页最大100条数据