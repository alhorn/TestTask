from typing import (
    List,
    Optional,
)

from drf_yasg import generators


def schema_generator_cls(excluded_paths: Optional[List[str]] = None):
    excluded_paths = excluded_paths or []

    class OpenAPISchemaGenerator(generators.OpenAPISchemaGenerator):
        def get_schema(self, request=None, public=False):
            swagger = super().get_schema(request, public)
            self._generate_tags(swagger)
            return swagger

        @staticmethod
        def _generate_tags(swagger):
            for endpoint, path in swagger.paths.items():
                try:
                    _, _, version, domain, _ = endpoint.split("/", maxsplit=4)
                    tags = [f"{domain} [{version}]"]
                except ValueError:
                    _, domain, _ = endpoint.split("/", maxsplit=2)
                    tags = [domain]

                for _, op in path.operations:
                    op.tags = tags

        def should_include_endpoint(self, path, method, view, public):
            include = (not any([path.startswith(x) for x in excluded_paths])) if excluded_paths else True
            return super().should_include_endpoint(path, method, view, public) and include

    return OpenAPISchemaGenerator
