from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Albums
from django.db.models import Q

class Albums_List(ListView):
    model = Albums
    template_name = 'albums/list.html'
    ordering = 'pk'
    paginate_by=12

    def get_context_data(self, **kwargs):
        context = super(Albums_List, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['start_page'] = start_index
        context['last_page']=end_index
        return context

class Albums_Search(Albums_List):
    paginate_by=12

    def get_queryset(self):
        q=self.kwargs['q']
        albums_list=Albums.objects.filter(
            Q(artist__contains=q) | Q(album__contains=q)
        ).distinct()
        return albums_list

    def get_context_data(self,**kwargs):
        context=super(Albums_Search,self).get_context_data()
        q=self.kwargs['q']
        context['search_info']=f'Search: {q} ({self.get_queryset().count()})'
        
        return context