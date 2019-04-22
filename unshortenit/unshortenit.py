import logging
from typing import List
import requests

from .module import UnshortenModule
from .modules import AdfLy, AdFocus, ShorteSt, MetaRefresh
from unshortenit import __version__


DEFAULT_HEADERS = {
    'User-Agent': 'unshortenit {}'.format(__version__),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': "no-cache",
}


class UnshortenIt:

    modules = {}
    _default_headers = None
    _default_timeout = None

    def __init__(self,
                default_timeout: int  = 30,
                default_headers: dict = None,
                urlcache:        dict = None,

            ):
        self._default_headers = default_headers or DEFAULT_HEADERS
        self._default_timeout = default_timeout
        self._urlcache        = urlcache

        self.log = logging.getLogger("Main.LinkUnshortener")

        self.register_modules([
            AdfLy,
            AdFocus,
            ShorteSt,
            MetaRefresh
        ])

    def register_module(self, module: UnshortenModule):
        if not isinstance(module, UnshortenModule):
            module = module(headers=self._default_headers, timeout=self._default_timeout)
        self.modules[module.name] = module

    def register_modules(self, modules: List[UnshortenModule]):
        for module in modules:
            self.register_module(module)

    def __unshorten(self,
                  uri:              str,
                  module:           str  = None,
                  timeout:          int  = None,
                  unshorten_nested: bool = False,
                  resolve_30x:      bool = True,
                  use_cache:        bool = True,
              ):

        timeout = timeout or self._default_timeout

        if module and module in self.modules:
            if self._urlcache and self._urlcache.get(uri, None):
                return self._urlcache.get(uri)
            res = self.modules[module].unshorten(uri)
            if self._urlcache:
                self._urlcache[uri] = res
            return res

        if unshorten_nested:
            last_uri = uri
            while True:
                matched = False
                for k, m in self.modules.items():
                    if m.is_match(uri):
                        self.log.info("Unshortener %s wants to process URL: '%s'", k, uri)
                        if use_cache and self._urlcache and self._urlcache.get(uri, None):
                            uri = self._urlcache.get(uri)
                        else:
                            uri = m.unshorten(uri)
                        matched = True
                        if uri == last_uri:
                            break
                        if self._urlcache:
                            self._urlcache[last_uri] = uri
                        last_uri = uri
                if not matched:
                    break
        else:
            for k, m in self.modules.items():
                if m.is_match(uri):
                    self.log.info("Unshortener %s wants to process URL: '%s'", k, uri)
                    if use_cache and self._urlcache and self._urlcache.get(uri, None):
                        res = self._urlcache.get(uri)
                    else:
                        res = m.unshorten(uri)
                    if self._urlcache:
                        self._urlcache[uri] = res
                    self.log.info("URL '%s' resolved to %s", uri, res)

                    return res

        if resolve_30x:

            self.log.info("Unshortener resolving potential 30X redirects for '%s'", uri)
            if use_cache and self._urlcache and self._urlcache.get(uri, None):
                res = self._urlcache.get(uri)
            else:
                res = requests.get(uri, timeout=timeout, headers=self._default_headers)
            if res.url == uri:
                self.log.info("URI Did not change due to 30X redirects.")
            else:
                self.log.info("URL '%s' redirected to %s", uri, res.url)

            if self._urlcache:
                self._urlcache[last_uri] = res.url

            return res.url
        return uri

    def unshorten(self,
                  uri:              str,
                  module:           str  = None,
                  timeout:          int  = None,
                  unshorten_nested: bool = False,
                  resolve_30x:      bool = True,
                  use_cache:        bool = True,
            ) -> str:

        try:
            return self.__unshorten(uri, module, timeout, unshorten_nested, resolve_30x, use_cache)
        except Exception as e:
            self.log.error("Failure unshortening URL: '%s'", uri)
            self.log.error("Exception: %s", e)
            raise e
