from forge.default_settings import *
from forgepro.default_settings import *

INSTALLED_APPS = INSTALLED_APPS + [
    "projects",
    "teams",
    "users",
    "forgepro.sentry",
    "forgepro.stripe",
    "forgepro.stafftoolbar",
    "forgepro.impersonate",
    "forgepro.googleanalytics",
]

MIDDLEWARE = MIDDLEWARE + [
    "forgepro.stafftoolbar.QueryStatsMiddleware",
    "forgepro.sentry.SentryFeedbackMiddleware",
    "forgepro.impersonate.ImpersonateMiddleware",
]

TIME_ZONE = "America/Chicago"

STRIPE_PRICE_ID = environ["STRIPE_PRICE_ID"]

GITHUB_APP_PRIVATE_KEY = environ["GITHUB_APP_PRIVATE_KEY"]
GITHUB_APP_ID = int(environ["GITHUB_APP_ID"])
GITHUB_APP_INSTALLATION_ID = int(environ["GITHUB_APP_INSTALLATION_ID"])
