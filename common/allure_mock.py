 #!/usr/bin/env python
# encoding: utf-8

from allure_commons._core import plugin_manager


class Attach(object):

    def __call__(self, body, name=None, attachment_type=None, extension=None):
        print("\n", body)
        plugin_manager.hook.attach_data(body=body, name=name, attachment_type=attachment_type, extension=extension)

    def file(self, source, name=None, attachment_type=None, extension=None):
        plugin_manager.hook.attach_file(source=source, name=name, attachment_type=attachment_type, extension=extension)


attach = Attach()
