from rest_framework.routers import (
    DynamicRoute,
    Route,
    SimpleRouter,
)


class CustomRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'post': 'create',
                'patch': 'partial_update',
                'delete': 'delete'
            },
            name='{basename}-detail',
            detail=False,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{url_path}/$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]
