
import logging
import os.path

log = logging.getLogger("Main.Jnius-Interface.Config")

jd_root = '/media/Storage/Scripts/jd'


class_path_entries = []

class_path_entries.append(os.path.join(jd_root, 'jd', 'plugins', 'decrypter'))
class_path_entries.append(os.path.join(jd_root, 'jd', 'plugins', 'hoster'))
class_path_entries.append(os.path.join(jd_root, 'libs'))
class_path_entries.append(os.path.join(jd_root, 'Core.jar'))
class_path_entries.append(os.path.join(jd_root, 'JDownloader.jar'))
class_path_entries.append(os.path.join(jd_root))

log.debug("Have %s classpath entries", len(class_path_entries))

import jnius_config
jnius_config.add_options('-Xrs', '-Xmx4096m')
jnius_config.set_classpath(*class_path_entries)

log.debug("Starting up JVM")
import jnius
from jnius import autoclass

log.debug("JVM has started")



# browser = autoclass("jd.http.Browser")
# browser = autoclass("jd.http.BrowserSettingsThread")

log.debug("Doing JVM system setup")
system = autoclass("java.lang.System")
security = autoclass("java.security.Security")


system.setProperty("java.net.preferIPv4Stack", "true")
system.setProperty("java.util.Arrays.useLegacyMergeSort", "true")
security.setProperty("networkaddress.cache.negative.ttl", "0")


application = autoclass("org.appwork.utils.Application")
application.setApplication("headless_jd")
log.debug("Application initialized.")

# sll = autoclass("jd.SecondLevelLaunch")
# application.getRoot(sll.class)


log.debug("Loading controllers")
extensionController     = autoclass('org.jdownloader.extensions.ExtensionController')
hostPluginController    = autoclass('org.jdownloader.plugins.controller.crawler.CrawlerPluginController')
crawlerPluginController = autoclass('org.jdownloader.plugins.controller.host.HostPluginController')


log.debug("Invalidating cache(if needed)")
# extensionController.getInstance().invalidateCacheIfRequired()
hostPluginController.getInstance().invalidateCacheIfRequired()
crawlerPluginController.getInstance().invalidateCacheIfRequired()

log.debug("Loading plugin class loader")
plugin_loader = autoclass("org.jdownloader.plugins.controller.PluginClassLoader")

print(plugin_loader)
log.debug("Loading loader instance")
plugin_loader_instance = plugin_loader.getInstance()
log.debug("Loading loader internal class")
plugin_loader_child = plugin_loader_instance.getChild()
log.debug("Loading plugins")

loaders = {
	'AdFly' : plugin_loader_child.loadClass('jd.plugins.decrypter.AdfLy')
}

log.debug("Loaded %s plugins successfully!", len(loaders))



