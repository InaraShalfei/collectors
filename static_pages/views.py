from django.views.generic import TemplateView


class AboutProjectView(TemplateView):
    template_name = 'static_pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте'
        context['simple_text'] = 'Всем привет! Рады видеть вас на страницах нашего сайта!'
        context['main_text'] = ('Данный проект позволяет любому человеку '
                                'делиться своими коллекциями по разным направлениям.')

        return context
