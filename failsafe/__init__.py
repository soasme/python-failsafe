__version__ = '0.1.0'


import logging
from time import sleep
from functools import wraps


logger = logging.getLogger(__name__)


class Failsafe(object):

    def __init__(self, function, retry, fallback, breaker, executor):
        self.function = function
        self.retry = retry
        self.fallback = fallback
        self.breaker = breaker
        self.executor = executor

    def __call__(self, *args, **kwargs):
        if self.retry is not None:
            max_retries = self.retry.get('max_retries', 3)
            delay = self.retry.get('delay', 1)
            errors = self.retry.get('errors', (Exception, ))
            for left_retries in range(max_retries, 0, -1):
                try:
                    return self.function(*args, **kwargs)
                except Exception as error:
                    if not isinstance(error, errors):
                        raise error
                    if delay:
                        logger.warning('%s run failed %d times and will retry in %d seconds.',
                                self.function, max_retries - left_retries + 1, delay)
                        sleep(delay)
            raise error
        else:
            return self.function(*args, **kwargs)


def failsafe(retry=None,
             fallback=None,
             breaker=None,
             executor=None,
             ):
    def decorator(f):
        _failsafe = Failsafe(function=f,
                             retry=retry,
                             fallback=fallback,
                             breaker=breaker,
                             executor=executor)
        setattr(f, 'failsafe', _failsafe)
        return f
    return decorator


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # todo: apply context,.use default context if not set.

    # todo: add jitter, backoff, duration, hooks (abort), based on return value, async.
    @failsafe(retry={'max_tries': 3, 'delay': 1, 'errors': (ValueError, ), })
    def get_remote_data():
        sleep(2.0)
        raise ValueError('demo')
        return 1

    @failsafe(fallback={'value': None, })
    def get_remote_data():
        sleep(2.0)
        raise ValueError('demo')

    # todo: support '3-5', 'last 3 out of 5', (3, 5), 3 for failure and test.
    # todo: async
    # todo: on_failure, on_test
    @failsafe(breaker={'failure': 3, 'delay': 1, 'test': 3, 'timeout': 1.0})

    #print(get_remote_data())
    print(get_remote_data.failsafe())
