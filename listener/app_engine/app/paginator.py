from django.core.paginator import Paginator as BasePaginator
from django.core.paginator import Page, InvalidPage, EmptyPage

class GAEPaginator(BasePaginator):   
    def page(self, number):
        "Returns a Page object for the given 1-based page number."        
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        queryset = self.object_list.fetch((number * self.per_page)+1)
        results = queryset[bottom:top]
        try:
            queryset[top]
            self._num_pages = number + 1
        except IndexError:
            self._num_pages = number
                        
        return Page(results, number, self)
        
Paginator = GAEPaginator

def get_page(request, paginator):
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return page