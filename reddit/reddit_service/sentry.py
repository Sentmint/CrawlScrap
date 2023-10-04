import sentry_sdk
import os

def init_sentry():
    dsn = os.environ.get('REDDIT_SENTRY_DSN', None)
    traces = float(os.environ.get('REDDIT_SENTRY_TRACES_SAMPLE_RATE', 1.0))
    profiles = float(os.environ.get('REDDIT_SENTRY_PROFILES_SAMPLE_RATE', 1.0))
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate = traces,
            profiles_sample_rate = profiles
        )
