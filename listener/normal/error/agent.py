import urllib
import re

from ConfigParser import SafeConfigParser as ConfigParser
from StringIO import StringIO

from django.core.cache import cache

from app.utils import log

class Browser(object):
    def __init__(self, capabilities):
        self.lazy_flag = True
        self.cap = capabilities

    def parse(self):
        for name, value in self.cap.items():
            if name in ["tables", "aol", "javaapplets",
                       "activexcontrols", "backgroundsounds",
                       "vbscript", "win16", "javascript", "cdf",
                       "wap", "crawler", "netclr", "beta",
                        "iframes", "frames", "stripper", "wap"]:
                self.cap[name] = (value.strip().lower() == "true")
            elif name in ["ecmascriptversion", "w3cdomversion"]:
                self.cap[name] = float(value)
            elif name in ["css"]:
                self.cap[name] = int(value)
            else:
                self.cap[name] = value
        self.lazy_flag = False

    def __repr__(self):
        if self.lazy_flag: self.parse()
        return repr(self.cap)

    def get(self, name, default=None):
        if self.lazy_flag: self.parse()
        try:
            return self[name]
        except KeyError:
            return default

    def __getitem__(self, name):
        if self.lazy_flag: self.parse()
        return self.cap[name.lower()]

    def keys(self):
        return self.cap.keys()

    def items(self):
        if self.lazy_flag: self.parse()
        return self.cap.items()

    def values(self):
        if self.lazy_flag: self.parse()
        return self.cap.values()

    def __len__(self):
        return len(self.cap)

    def supports(self, feature):
        value = self.cap.get(feature)
        if value == None:
            return False
        return value

    def features(self):
        l = []
        for f in ["tables", "frames", "iframes", "javascript",
                  "cookies", "w3cdomversion", "wap"]:
            if self.supports(f):
                l.append(f)
        if self.supports_java():
            l.append("java")
        if self.supports_activex():
            l.append("activex")
        css = self.css_version()
        if css > 0:
            l.append("css1")
        if css > 1:
            l.append("css2")
        return l

    def supports_tables(self):
        return self.supports("frames")

    def supports_iframes(self):
        return self.supports("iframes")

    def supports_frames(self):
        return self.supports("frames")

    def supports_java(self):
        return self.supports("javaapplets")

    def supports_javascript(self):
        return self.supports("javascript")

    def supports_vbscript(self):
        return self.supports("vbscript")

    def supports_activex(self):
        return self.supports("activexcontrols")

    def supports_cookies(self):
        return self.supports("cookies")

    def supports_wap(self):
        return self.supports("wap")

    def css_version(self):
        return self.get("css", 0)

    def version(self):
        major = self.get("majorver")
        minor = self.get("minorver")
        if major and minor:
            return (major, minor)
        elif major:
            return (major, None)
        elif minor:
            return (None, minor)
        else:
            ver = self.get("version")
            if ver and "." in ver:
                return tuple(ver.split(".", 1))
            elif ver:
                return (ver, None)
            else:
                return (None, None)

    def dom_version(self):
        return self.get("w3cdomversion", 0)


    def is_bot(self):
        return self.get("crawler") == True

    def is_mobile(self):
        return self.get("ismobiledevice") == True

    def name(self):
        return self.get("browser")

    def platform(self):
        return self.get("platform")

class BrowserCapabilities(object):

    def __new__(cls, *args, **kwargs):
        # Only create one instance of this clas
        if "instance" not in cls.__dict__:
            cls.instance = object.__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        self.cache = {}
        self.parse()

    def parse(self):
        key = "browser-capabilities-raw"
        raw = cache.get(key)
        # if the data isn't there, download it
        if raw is None:
            data = None
            log("Fetching from browser capabilities")
            try:
                data = urllib.urlopen("http://www.areciboapp.com/static/browscap.ini")
            except (IOError):
                pass
            if data: # and data.code == 200:
                # that should be one week (1 min > 1 hour > 1 day > 1 week)
                log("...succeeded")
                raw = data.read()
                cache.set(key, raw, 60 * 60 * 24 * 7)
            else:
                log("...failed")
                # try again in 1 hour if there was a problem
                cache.set(key, "", 60 * 60)
                raw = ""
        else:
            log("Using cached browser capabilities")

        string = StringIO(raw)
        cfg = ConfigParser()
        cfg.readfp(string)

        self.sections = []
        self.items = {}
        self.browsers = {}
        parents = set()
        for name in cfg.sections():
            qname = name
            for unsafe in list("^$()[].-"):
                qname = qname.replace(unsafe, "\%s" % unsafe)
            qname = qname.replace("?", ".").replace("*", ".*?")
            qname = "^%s$" % qname
            sec_re = re.compile(qname)
            sec = dict(regex=qname)
            sec.update(cfg.items(name))
            p = sec.get("parent")
            if p: parents.add(p)
            self.browsers[name] = sec
            if name not in parents:
                self.sections.append(sec_re)
            self.items[sec_re] = sec


    def query(self, useragent):
        useragent = useragent.replace(' \r\n', '')
        b = self.cache.get(useragent)
        if b: return b

        if not hasattr(self, "sections"):
            return None

        for sec_pat in self.sections:
            if sec_pat.match(useragent):
                browser = dict(agent=useragent)
                browser.update(self.items[sec_pat])
                parent = browser.get("parent")
                while parent:
                    items = self.browsers[parent]
                    for key, value in items.items():
                        if key not in browser.keys():
                            browser[key] = value
                        elif key == "browser" and value != "DefaultProperties":
                            browser["category"] = value # Wget, Godzilla -> Download Managers
                    parent = items.get("parent")
                if browser.get("browser") != "Default Browser":
                    b = Browser(browser)
                    self.cache[useragent] = b
                    return b
        self.cache[useragent] = None

    __call__ = query


def get():
    key = "browser-capabilities-parsed"
    parsed = cache.get(key)
    if parsed is None:
        parsed = BrowserCapabilities()
        # that should be one week (1 min > 1 hour > 1 day > 1 week)
        cache.set(key, parsed, 60 * 60 * 24 * 7)
    return parsed


def test():
    bc = get()
    for agent in [
        "Mozilla/5.0 (compatible; Konqueror/3.5; Linux; X11; de) KHTML/3.5.2 (like Gecko) Kubuntu 6.06 Dapper",
        "Mozilla/5.0 (X11; U; Linux i686; de; rv:1.8.0.5) Gecko/20060731 Ubuntu/dapper-security Firefox/1.5.0.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20060216 Debian/1.7.12-1.1ubuntu2",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.5) Gecko/20060731 Ubuntu/dapper-security Epiphany/2.14 Firefox/1.5.0.5",
        "Opera/9.00 (X11; Linux i686; U; en)",
        "Wget/1.10.2",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20051128 Kazehakase/0.3.3 Debian/0.3.3-1",
        "Mozilla/5.0 (X11; U; Linux i386) Gecko/20063102 Galeon/1.3test",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_4; en-us) AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.2 Safari/525.20.1",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)" # Tested under Wine
        """Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US;  \r
rv:1.9.0.5) Gecko/2008120121 Firefox/3.0.5,gzip(gfe)""",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.5) Gecko/2008120121 Firefox/3.0.5,gzip(gfe)",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like Gecko) Version/3.2.1 Safari/525.27.1,gzip(gfe)"
      ]:
        b = bc(agent)
        if not b:
            print "! Not found", agent
        else:
            print b.name(), b.version(), b.get("category", ""), b.features()
