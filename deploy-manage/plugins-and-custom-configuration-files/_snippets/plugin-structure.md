A plugin is a ZIP file that contains a plugin descriptor file and binaries. The descriptor file is called `stable-plugin-descriptor.properties` for plugins built against the stable plugin API, or `plugin-descriptor.properties` for plugins built against the classic plugin API. A plugin ZIP file should contain only one descriptor file.

{{es}} assumes that the ZIP file contains binaries. If it finds any source code, it fails with an error message, causing provisioning to fail. Make sure the ZIP file contains binaries, and not source code.
