from rest_framework.pagination import PageNumberPagination


class CourseLessonPagination(PageNumberPagination):
    """
    Пагинация для списков курсов и уроков.
    """

    page_size = 5  # 🔹 количество объектов на одной странице
    page_size_query_param = (
        "page_size"  # 🔹 можно переопределить в URL, например ?page_size=10
    )
    max_page_size = 50  # 🔹 ограничение на максимум
