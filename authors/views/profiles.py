from authors.models import Profile  # noqa

from django.shortcuts import get_object_or_404  # noqa

from django.views.generic import TemplateView


class ProfileViews(TemplateView):
    template_name = 'authors/pages/profile.html'
    def get(self, request, *args, **kwargs): # noqa

        context = self.get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = get_object_or_404(Profile.objects.filter(
            pk=profile_id).select_related('author'), pk=profile_id)
        return self.render_to_response({
            **context,
            'profile': profile,
        })
