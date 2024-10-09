import sentry_sdk

sentry_sdk.init(
    dsn="https://449d7c58fd3d64fcbb54a8ade190718c@o4508088242798593.ingest.de.sentry.io/4508088271110224",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

division_by_zero = 1 / 0