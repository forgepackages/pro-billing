from forge.default_settings import *
from forgepro.default_settings import FORGEPRO_APPS, FORGEPRO_MIDDLEWARE

INSTALLED_APPS = (
    INSTALLED_APPS
    + ["projects", "teams", "users", "packages", "django_hosts"]
    + FORGEPRO_APPS
)

MIDDLEWARE = (
    ["django_hosts.middleware.HostsRequestMiddleware"]
    + MIDDLEWARE
    + FORGEPRO_MIDDLEWARE
    + ["django_hosts.middleware.HostsResponseMiddleware"]
)

TIME_ZONE = "America/Chicago"

STRIPE_PRICE_ID = environ["STRIPE_PRICE_ID"]

GITHUB_APP_PRIVATE_KEY = environ["GITHUB_APP_PRIVATE_KEY"]
GITHUB_APP_ID = int(environ["GITHUB_APP_ID"])
GITHUB_APP_INSTALLATION_ID = int(environ["GITHUB_APP_INSTALLATION_ID"])

ROOT_HOSTCONF = "hosts"
DEFAULT_HOST = "billing"
