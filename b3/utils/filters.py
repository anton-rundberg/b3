from django.utils.encoding import force_str
from rest_framework.compat import coreapi, coreschema
from rest_framework.filters import OrderingFilter


class ExtendedOrderingFilter(OrderingFilter):
    # Note that this does not work with drf_spectacular out of the box
    # It needs to be rewritten to override get_schema_operation_parameters instead
    # See: https://drf-spectacular.readthedocs.io/en/latest/customization.html?highlight=OpenApiFilterExtension#declare-custom-library-filters-with-openapifilterextension # noqa
    def get_schema_fields(self, view):
        assert (
            coreapi is not None
        ), "coreapi must be installed to use `get_schema_fields()`"
        assert (
            coreschema is not None
        ), "coreschema must be installed to use `get_schema_fields()`"

        # If fields are stated explicitly then add them to API Field description
        valid_fields = getattr(view, "ordering_fields", self.ordering_fields)
        if valid_fields is not None and valid_fields != "__all__":
            description = "{ordering_description} Available fields: {fields}".format(
                ordering_description=self.ordering_description,
                fields=" ".join(["`" + field + "`" for field in valid_fields]),
            )
        else:
            description = self.ordering_description

        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_str(self.ordering_title),
                    description=force_str(description),
                ),
            )
        ]
