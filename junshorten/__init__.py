
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
system.setProperty("jna.debug_load", "true")
system.setProperty("jna.debug_load.jna", "true")

application = autoclass("org.appwork.utils.Application")
application.setApplication("headless_jd")

application.getResource("tmp/jna").mkdir()
system.setProperty("jna.tmpdir", application.getResource("tmp/jna").getAbsolutePath())

log.debug("Application initialized.")


util = autoclass("jd.utils.JDUtilities")


print(util)
print(util.getJDHomeDirectoryFromEnvironment())

# import java.io.File;
# import java.lang.ClassLoader;
# import java.net.URL;
# import java.net.URLClassLoader;

# File file  = new File("./Core.jar");
# System.out.println("File: " + file);

# URL url = file.toURL();
# URL[] urls = new URL[]{url};

# ClassLoader cl = new URLClassLoader(urls);
# Class cls = cl.loadClass("jd.SecondLevelLaunch");

# System.out.println("Loaded class: " + cls);


filetype = autoclass("java.io.File")
fileinstance = filetype(os.path.join(jd_root, 'Core.jar'))
urlinstance = fileinstance.toURL()
print(urlinstance)

urlloader = autoclass("java.net.URLClassLoader")
print(urlloader)
classloader = urlloader([urlinstance])
print(classloader)
sll = classloader.loadClass("jd.SecondLevelLaunch")
print(sll)
print(sll.toString())
print(dir(sll))

sllins = sll.newInstance()
print("Instance:", sllins)

import sys
sys.exit()


sll_classes = [
	'jd.SecondLevelLaunch$1',
	'jd.SecondLevelLaunch$10$1',
	# 'jd.SecondLevelLaunch$10',
	'jd.SecondLevelLaunch$11',
	'jd.SecondLevelLaunch$12$1$1',
	'jd.SecondLevelLaunch$12$1$2',
	'jd.SecondLevelLaunch$12$1$3',
	'jd.SecondLevelLaunch$12$1$4$1$1',
	'jd.SecondLevelLaunch$12$1$4$1',
	'jd.SecondLevelLaunch$12$1$4$2',
	'jd.SecondLevelLaunch$12$1$4',
	'jd.SecondLevelLaunch$12$1$5$1$1',
	'jd.SecondLevelLaunch$12$1$5$1$2',
	'jd.SecondLevelLaunch$12$1$5$1',
	'jd.SecondLevelLaunch$12$1$5',
	'jd.SecondLevelLaunch$12$1$6$1',
	'jd.SecondLevelLaunch$12$1$6',
	'jd.SecondLevelLaunch$12$1$7',
	'jd.SecondLevelLaunch$12$1',
	'jd.SecondLevelLaunch$12',
	'jd.SecondLevelLaunch$13',
	'jd.SecondLevelLaunch$14',
	'jd.SecondLevelLaunch$15',
	'jd.SecondLevelLaunch$16',
	'jd.SecondLevelLaunch$17',
	'jd.SecondLevelLaunch$2',
	'jd.SecondLevelLaunch$3',
	'jd.SecondLevelLaunch$4',
	'jd.SecondLevelLaunch$5',
	'jd.SecondLevelLaunch$6',
	'jd.SecondLevelLaunch$7',
	# 'jd.SecondLevelLaunch$8',
	'jd.SecondLevelLaunch$9',
	# 'jd.SecondLevelLaunch',
	'jd.SecondLevelLaunch',
]


for sll_name in sll_classes:
	log.debug("Loading %s", sll_name)
	tmp = autoclass(sll_name)
	print(tmp)
	print(dir(tmp))


import sys
sys.exit()

sll2 = autoclass("jd.SecondLevelLaunch$2")
import pdb
pdb.set_trace()
print("SecondLevelLaunch: ", sll)
application.getRoot(getattr(sll, "class"))


log.debug("Loading HostPluginController.")
hostplugincontroller = autoclass("org.jdownloader.plugins.controller.host.HostPluginController")
hostplugincontroller.getInstance().ensureLoaded()
log.debug("HostPluginController loaded.")

log.debug("Loading PackagizerController.")
packagizercontroller = autoclass("org.jdownloader.controlling.packagizer.PackagizerController")
packagizercontroller.getInstance()
log.debug("PackagizerController loaded.")

log.debug("Loading DownloadController.")
downloadcontroller   = autoclass("jd.controlling.downloadcontroller.DownloadController")
downloadcontroller.getInstance().initDownloadLinks()
log.debug("DownloadController loaded.")

log.debug("Loading LinkCollector.")
linkcollector        = autoclass("jd.controlling.linkcollector.LinkCollector")
linkcollector.getInstance().initLinkCollector()
log.debug("LinkCollector loaded.")

log.debug("Loading RemoteAPIController.")
remoteapicontroller  = autoclass("org.jdownloader.api.RemoteAPIController")
remoteapicontroller.getInstance()
log.debug("RemoteAPIController loaded.")

log.debug("Loading ExternInterface.")
externinterface      = autoclass("org.jdownloader.api.cnl2.ExternInterface")
externinterface.getINSTANCE()
log.debug("ExternInterface loaded.")


formatter = autoclass("jd.nutils.Formatter")

import pdb
pdb.set_trace()



# Thread.currentThread().setName("ExecuteWhenGuiReachedThread: Init Host Plugins");
# HostPluginController.getInstance().ensureLoaded();
# HOST_PLUGINS_COMPLETE.setReached();
# PackagizerController.getInstance();
# /* load links */
# Thread.currentThread().setName("ExecuteWhenGuiReachedThread: Init DownloadLinks");
# DownloadController.getInstance().initDownloadLinks();
# Thread.currentThread().setName("ExecuteWhenGuiReachedThread: Init Linkgrabber");
# LinkCollector.getInstance().initLinkCollector();
# /* start remote api */
# Thread.currentThread().setName("ExecuteWhenGuiReachedThread: Init RemoteAPI");
# RemoteAPIController.getInstance();
# Thread.currentThread().setName("ExecuteWhenGuiReachedThread: Init MYJDownloader");
# MyJDownloaderController.getInstance();
# Thread.currentThread().setName("ExecuteWhenGuiReachedThread: Init Extern INterface");
# ExternInterface.getINSTANCE();

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



