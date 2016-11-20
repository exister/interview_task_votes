import coreapi
from django.utils.encoding import force_text
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator, types_lookup
from rest_framework.views import APIView
from rest_framework_swagger import renderers


class BaseAPIViewSchema:
    def _get_fields_from_serializer(self, serializer, method):
        fields = []
        for field in serializer.fields.values():
            if field.read_only or isinstance(field, serializers.HiddenField):
                continue

            required = field.required and method != 'PATCH'
            description = force_text(field.help_text) if field.help_text else ''
            field = coreapi.Field(
                name=field.field_name,
                location='form',
                required=required,
                description=description,
                type=types_lookup[field]
            )
            fields.append(field)
        return fields


class LoginSchema(BaseAPIViewSchema):
    def get_serializer_fields(self, path, method, view):
        serializer = view.serializer_class()
        return self._get_fields_from_serializer(serializer, method)


class BaseSchemaGenerator(SchemaGenerator):
    def has_view_permissions(self, path, method, view):
        return True

    def get_serializer_fields(self, path, method, view):
        try:
            return super().get_serializer_fields(path, method, view)
        except AssertionError as e:
            return []


class ApiV1SchemaGenerator(BaseSchemaGenerator):
    def get_serializer_fields(self, path, method, view):
        if path == '/api/v1/login/':
            return LoginSchema().get_serializer_fields(path, method, view)
        return super().get_serializer_fields(path, method, view)


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]
    exclude_from_schema = True

    def get(self, request):
        generator = ApiV1SchemaGenerator()
        schema = generator.get_schema(request=request)

        return Response(schema)

swagger_schema_view = SwaggerSchemaView.as_view()
