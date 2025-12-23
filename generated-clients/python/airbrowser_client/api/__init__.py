# flake8: noqa

if __import__("typing").TYPE_CHECKING:
    # import apis into api package
    from airbrowser_client.api.browser_api import BrowserApi
    from airbrowser_client.api.health_api import HealthApi
    from airbrowser_client.api.pool_api import PoolApi
    from airbrowser_client.api.profiles_api import ProfilesApi
    
else:
    from lazy_imports import LazyModule, as_package, load

    load(
        LazyModule(
            *as_package(__file__),
            """# import apis into api package
from airbrowser_client.api.browser_api import BrowserApi
from airbrowser_client.api.health_api import HealthApi
from airbrowser_client.api.pool_api import PoolApi
from airbrowser_client.api.profiles_api import ProfilesApi

""",
            name=__name__,
            doc=__doc__,
        )
    )
