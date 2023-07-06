from django.contrib import admin

from .validation import days_of_the_week_abbreviated


class ArrayDagenListFilter(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField. """
    title = "dagen"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "dagen"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. 
        (lookup_value, human-readable value). These
        appear in the admin's right sidebar
        """
        dagen = [(kw, kw) for sublist in days_of_the_week_abbreviated for kw in sublist if kw]
        dagen = sorted(set(dagen))
        return dagen

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        lookup_value = self.value()  # The clicked keyword. It can be None!
        if lookup_value:
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(keywords__contains=[lookup_value])
        return queryset
