import logging
from django.contrib import messages
from django.http import HttpResponse, HttpResponseGone, HttpResponsePermanentRedirect, HttpResponseRedirect, Http404
from django.utils.translation import gettext as _
from django.views.generic import FormView, UpdateView, RedirectView
from django.views.generic.detail import BaseDetailView

logger = logging.getLogger('django.request')


# Create your views here.
def health(request):
    return HttpResponse()


class FormsetView(FormView):
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'formset' not in kwargs:
            kwargs['formset'] = self.get_form()
        return super(FormsetView, self).get_context_data(**kwargs)

    def form_valid(self, formset):
        """If the form is valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, formset):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(formset=formset))


class FormFormsetView(FormView):
    formset_initial = {}
    formset_class = None
    formset_prefix = None

    def get_initial(self):
        """Return the initial data to use for forms and formsets on this view."""
        return self.initial.copy(), self.formset_initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms and formsets."""
        return self.prefix, self.formset_prefix

    def get_form_class(self):
        """Return the form and formset classes to use."""
        return self.form_class, self.formset_class

    def get_form(self, form_class=None, formset_class=None):
        """Return the form class and formset class to use."""
        if form_class is None or formset_class is None:
            form_class, formset_class = self.get_form_class()
        return form_class(**self.get_form_kwargs()), formset_class(**self.get_formset_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form and formset."""
        form_initial, formset_initial = self.get_initial()
        form_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form_initial,
            'prefix': form_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the form and formset."""
        form_initial, formset_initial = self.get_initial()
        form_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': formset_initial,
            'prefix': formset_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'formset' not in kwargs or 'form' not in kwargs:
            kwargs['form'], kwargs['formset'] = self.get_form()
        return super(FormFormsetView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form and formset instance with the passed
        POST variables and then check if it's valid.
        """
        form, formset = self.get_form()
        if form.is_valid() and formset.is_valid():
            return self.forms_valid(form, formset)
        else:
            return self.forms_invalid(form, formset)

    def forms_valid(self, form, formset):
        """If the form and formset are valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, formset):
        """If the form and formset are invalid, render the invalid form/formset."""
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class DualFormView(FormView):
    form2_initial = {}
    form2_class = None
    form2_prefix = None

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy(), self.form2_initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix, self.form2_prefix

    def get_form_class(self):
        """Return the forms classes to use."""
        return self.form_class, self.form2_class

    def get_form(self, form_class=None, form2_class=None):
        """Return the form to use."""
        if form_class is None or form2_class is None:
            form_class, form2_class = self.get_form_class()
        return form_class(**self.get_form_kwargs()), form2_class(**self.get_form2_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2."""
        form_initial, form2_initial = self.get_initial()
        form_prefix, form2_prefix = self.get_prefix()
        kwargs = {
            'initial': form_initial,
            'prefix': form_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form2_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2."""
        form_initial, form2_initial = self.get_initial()
        form_prefix, form2_prefix = self.get_prefix()
        kwargs = {
            'initial': form2_initial,
            'prefix': form2_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form2' not in kwargs or 'form' not in kwargs:
            kwargs['form'], kwargs['form2'] = self.get_form()
        return super(DualFormView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form and form2 instance with the passed
        POST variables and then check if it's valid.
        """
        form, form2 = self.get_form()
        if form.is_valid() and form2.is_valid():
            return self.forms_valid(form, form2)
        else:
            return self.forms_invalid(form, form2)

    def forms_valid(self, form, form2):
        """If the forms are valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, form2):
        """If the forms are invalid, render the invalid form/formset."""
        return self.render_to_response(self.get_context_data(form=form, form2=form2))


class DualOptionalFormView(DualFormView):

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form and form2 instance with the passed
        POST variables and then check if it's valid.
        """
        form, form2 = self.get_form()
        if form.is_valid() or form2.is_valid():
            return self.forms_valid(form, form2)
        else:
            return self.forms_invalid(form, form2)


class TripleFormView(FormView):
    form2_initial = {}
    form2_class = None
    form2_prefix = None
    form3_initial = {}
    form3_class = None
    form3_prefix = None

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy(), self.form2_initial.copy(), self.form3_initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix, self.form2_prefix, self.form3_prefix

    def get_form_class(self):
        """Return the forms classes to use."""
        return self.form_class, self.form2_class, self.form3_class

    def get_form(self, form_class=None, form2_class=None, form3_class=None):
        """Return the form to use."""
        if form_class is None or form2_class is None or form3_class is None:
            form_class, form2_class, form3_class = self.get_form_class()
        return form_class(**self.get_form_kwargs()), form2_class(**self.get_form2_kwargs()), form3_class(**self.get_form3_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3."""
        form_initial, form2_initial, form3_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix = self.get_prefix()
        kwargs = {
            'initial': form_initial,
            'prefix': form_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form2_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3."""
        form_initial, form2_initial, form3_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix = self.get_prefix()
        kwargs = {
            'initial': form2_initial,
            'prefix': form2_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form3_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3."""
        form_initial, form2_initial, form3_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix = self.get_prefix()
        kwargs = {
            'initial': form3_initial,
            'prefix': form3_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form3' not in kwargs or 'form2' not in kwargs or 'form' not in kwargs:
            kwargs['form'], kwargs['form2'], kwargs['form3'] = self.get_form()
        return super(TripleFormView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form and form2 instance with the passed
        POST variables and then check if it's valid.
        """
        form, form2, form3 = self.get_form()
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            return self.forms_valid(form, form2, form3)
        else:
            return self.forms_invalid(form, form2, form3)

    def forms_valid(self, form, form2, form3):
        """If the forms are valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, form2, form3):
        """If the forms are invalid, render the invalid form/formset."""
        return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3))


class TripleFormFormsetView(FormView):
    form2_initial = {}
    form2_class = None
    form2_prefix = None
    form3_initial = {}
    form3_class = None
    form3_prefix = None
    formset_initial = {}
    formset_class = None
    formset_prefix = None

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy(), self.form2_initial.copy(), self.form3_initial.copy(), self.formset_initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix, self.form2_prefix, self.form3_prefix, self.formset_prefix

    def get_form_class(self):
        """Return the forms classes to use."""
        return self.form_class, self.form2_class, self.form3_class, self.formset_class

    def get_form(self, form_class=None, form2_class=None, form3_class=None, formset_class=None):
        """Return the form to use."""
        if form_class is None or form2_class is None or form3_class is None or formset_class is None:
            form_class, form2_class, form3_class, formset_class = self.get_form_class()
        return form_class(**self.get_form_kwargs()), form2_class(**self.get_form2_kwargs()), form3_class(
            **self.get_form3_kwargs()), formset_class(**self.get_formset_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the forms and formset."""
        form_initial, form2_initial, form3_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form_initial,
            'prefix': form_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form2_kwargs(self):
        """Return the keyword arguments for instantiating the forms and formset."""
        form_initial, form2_initial, form3_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form2_initial,
            'prefix': form2_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form3_kwargs(self):
        """Return the keyword arguments for instantiating the forms and formset."""
        form_initial, form2_initial, form3_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form3_initial,
            'prefix': form3_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the forms and formset."""
        form_initial, form2_initial, form3_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': formset_initial,
            'prefix': formset_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form3' not in kwargs or 'form2' not in kwargs or 'form' not in kwargs and 'formset' not in kwargs:
            kwargs['form'], kwargs['form2'], kwargs['form3'], kwargs['formset'] = self.get_form()
        return super(TripleFormFormsetView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form and form2 instance with the passed
        POST variables and then check if it's valid.
        """
        form, form2, form3, formset = self.get_form()
        if form.is_valid() and form2.is_valid() and form3.is_valid() and formset.is_valid():
            return self.forms_valid(form, form2, form3, formset)
        else:
            return self.forms_invalid(form, form2, form3, formset)

    def forms_valid(self, form, form2, form3, formset):
        """If the forms are valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, form2, form3, formset):
        """If the forms are invalid, render the invalid form/formset."""
        return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, formset=formset))


class QuadFormView(FormView):
    form2_initial = {}
    form2_class = None
    form2_prefix = None
    form3_initial = {}
    form3_class = None
    form3_prefix = None
    form4_initial = {}
    form4_class = None
    form4_prefix = None

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy(), self.form2_initial.copy(), self.form3_initial.copy(), self.form4_initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix, self.form2_prefix, self.form3_prefix, self.form4_prefix

    def get_form_class(self):
        """Return the forms classes to use."""
        return self.form_class, self.form2_class, self.form3_class, self.form4_class

    def get_form(self, form_class=None, form2_class=None, form3_class=None, form4_class=None):
        """Return the form to use."""
        if form_class is None or form2_class is None or form3_class is None or form4_class is None:
            form_class, form2_class, form3_class, form4_class = self.get_form_class()
        return form_class(**self.get_form_kwargs()), form2_class(**self.get_form2_kwargs()), \
               form3_class(**self.get_form3_kwargs()), form4_class(**self.get_form4_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix = self.get_prefix()
        kwargs = {
            'initial': form_initial,
            'prefix': form_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form2_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix = self.get_prefix()
        kwargs = {
            'initial': form2_initial,
            'prefix': form2_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form3_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix = self.get_prefix()
        kwargs = {
            'initial': form3_initial,
            'prefix': form3_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form4_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix = self.get_prefix()
        kwargs = {
            'initial': form4_initial,
            'prefix': form4_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'form4' not in kwargs or 'form3' not in kwargs or 'form2' not in kwargs or 'form' not in kwargs:
            kwargs['form'], kwargs['form2'], kwargs['form3'], kwargs['form4'] = self.get_form()
        return super(QuadFormView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form and form2 instance with the passed
        POST variables and then check if it's valid.
        """
        form, form2, form3, form4 = self.get_form()
        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            return self.forms_valid(form, form2, form3, form4)
        else:
            return self.forms_invalid(form, form2, form3, form4)

    def forms_valid(self, form, form2, form3, form4):
        """If the forms are valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, form2, form3, form4):
        """If the forms are invalid, render the invalid form/formset."""
        return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, form4=form4))


class QuadFormFormsetView(FormView):
    form2_initial = {}
    form2_class = None
    form2_prefix = None
    form3_initial = {}
    form3_class = None
    form3_prefix = None
    form4_initial = {}
    form4_class = None
    form4_prefix = None
    formset_initial = {}
    formset_class = None
    formset_prefix = None

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self.initial.copy(), self.form2_initial.copy(), self.form3_initial.copy(), self.form4_initial.copy(), \
               self.formset_initial.copy()

    def get_prefix(self):
        """Return the prefix to use for forms."""
        return self.prefix, self.form2_prefix, self.form3_prefix, self.form4_prefix, self.formset_prefix

    def get_form_class(self):
        """Return the forms classes to use."""
        return self.form_class, self.form2_class, self.form3_class, self.form4_class, self.formset_class

    def get_form(self, form_class=None, form2_class=None, form3_class=None, form4_class=None, formset_class=None):
        """Return the form to use."""
        if form_class is None or form2_class is None or form3_class is None or form4_class is None or formset_class is None:
            form_class, form2_class, form3_class, form4_class, formset_class = self.get_form_class()
        return form_class(**self.get_form_kwargs()), form2_class(**self.get_form2_kwargs()), \
               form3_class(**self.get_form3_kwargs()), form4_class(**self.get_form4_kwargs()), formset_class(**self.get_formset_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form_initial,
            'prefix': form_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form2_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form2_initial,
            'prefix': form2_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form3_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form3_initial,
            'prefix': form3_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form4_kwargs(self):
        """Return the keyword arguments for instantiating the form and form2 and form3 and form4."""
        form_initial, form2_initial, form3_initial, form4_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': form4_initial,
            'prefix': form4_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_formset_kwargs(self):
        """Return the keyword arguments for instantiating the forms and formset."""
        form_initial, form2_initial, form3_initial, form4_initial, formset_initial = self.get_initial()
        form_prefix, form2_prefix, form3_prefix, form4_prefix, formset_prefix = self.get_prefix()
        kwargs = {
            'initial': formset_initial,
            'prefix': formset_prefix
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if 'formset' not in kwargs or 'form4' not in kwargs or 'form3' not in kwargs or 'form2' not in kwargs or 'form' not in kwargs:
            kwargs['form'], kwargs['form2'], kwargs['form3'], kwargs['form4'], kwargs['formset'] = self.get_form()
        return super(QuadFormFormsetView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form and form2 instance with the passed
        POST variables and then check if it's valid.
        """
        form, form2, form3, form4, formset = self.get_form()
        if form.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and formset.is_valid():
            return self.forms_valid(form, form2, form3, form4, formset)
        else:
            return self.forms_invalid(form, form2, form3, form4, formset)

    def forms_valid(self, form, form2, form3, form4, formset):
        """If the forms are valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, form2, form3, form4, formset):
        """If the forms are invalid, render the invalid form/formset."""
        return self.render_to_response(self.get_context_data(form=form, form2=form2, form3=form3, form4=form4, formset=formset))


class DetailUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super(DetailUpdateView, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        return super(DetailUpdateView, self).get_context_data(**kwargs)


class RedirectDeleteView(RedirectView, BaseDetailView):
    success_message = None

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def pop_kwargs(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            kwargs.pop('pk')
            pk = None
        if slug is not None and (pk is None):
            slug_field = self.get_slug_field()
            kwargs.pop(slug_field)
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        kwargs = self.pop_kwargs(**kwargs)
        url = self.get_redirect_url(*args, **kwargs)
        if url:
            if self.success_message:
                messages.success(request, self.success_message)
            self.object.delete()
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            logger.warning(
                'Gone: %s', request.path,
                extra={'status_code': 410, 'request': request}
            )
            return HttpResponseGone()
