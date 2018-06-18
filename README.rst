Python-Failsafe
===============

Overview
--------

> [Fail-safe](https://en.wikipedia.org/wiki/Fail-safe) in engineering is a design feature or practice that in the event of a specific type of failure, inherently responds in a way that will cause no or minimal harm to other equipment, the environment or to people.
> - Wikipedia

In software engineering, failsafe can keep your system away from cascading failure, infinite hanging, etc. Some of the most useful methods have been exploited, such as retrying, jitter, back-off, circuit breaker, fallback etc. A robust system has to apply any one of these techniques or to mix all of them to against failures.

Install
-------

Get started by pip install::

    $ pip install failsafe

Usage
-----

Decorator::

    @failsafe(retry={'max_tries': 3, 'delay': 1, 'errors': (ValueError, ), })
    def remote_call(xyz):
        return xyz

Call::

    # no failsafe call
    remote_call(xyz)

    # failsafe call
    remote_call.failsafe(xyz)


Decorator can also be applied to async functions::

    @failsafe(retry={'max_tries': 3, 'delay': 1, 'errors': (ValueError, ), })
    async def remote_call(xyz):
        return xyz

    # failsafe async call
    await remote_call.failsafe(xyz)


Retry::

    @failsafe(retry={'max_tries': 3, 'delay': 1, 'errors': (ValueError, ), })
    def remote_call(xyz):
        return xyz

Retry with jitter::

    @failsafe(retry={'max_tries': 3, 'jitter': 1, 'delay': 1, 'errors': (ValueError, ), })
    def remote_call(xyz):
        return xyz

Retry with back-off::

    @failsafe(retry={'max_tries': 3, 'backoff': 1, 'delay': 1, 'errors': (ValueError, ), })
    def remote_call(xyz):
        return xyz

Fallback with a callback::

    def f(xyz):
        return 'dummy'

    @failsafe(fallback=f)
    def remote_call(xyz):
        return xyz

Fallback with a value::

    @failsafe(fallback={'value': 'dummy'})
    def remote_call(xyz):
        return xyz

Circuit breaker::

    @failsafe(breaker={'failure': 3, 'delay': 1, 'test': 3, 'timeout': 1.0})
    def remote_call(xyz):
        return xyz

Circuit breaker opening with last 3 of 5 call failed::

    @failsafe(breaker={'failure': (3, 5), 'delay': 1, 'test': (3, 5), 'timeout': 1.0})
    def remote_call(xyz):
        return xyz


Alternatives
------------

* `Pyfailsafe <https://github.com/Skyscanner/pyfailsafe>`_: This is another promising Failsafe library in Python. It has different flavor on the API. But generally they share many basic concepts. Pyfailsafe is using APLv2 license.

Developing
----------

Contribute
----------

License
-------

All files are released with the MIT license.
