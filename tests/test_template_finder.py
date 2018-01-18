import collections

try:
    from unittest import mock
except ImportError:
    from django.test import mock

from django.test import TestCase

from pyfakefs.fake_filesystem_unittest import Patcher

from template_tree import template_finder

# Stub the Django app config classes, to save having to create
# fully instantiated versions when just the path is needed.
AppConfig = collections.namedtuple('AppConfig', 'path')
Apps = collections.namedtuple('Apps', 'app_configs')


class TestFilesystemFinder(TestCase):

    patcher = None

    def setUp(self):
        self.patcher = Patcher()
        self.patcher.setUp()
        self.patcher.fs.CreateFile('/tmp/project/templates/base.html')
        self.patcher.fs.CreateFile('/tmp/project/templates/foo/bar.html')
        self.patcher.fs.CreateFile('/tmp/project/other_templates/baz.html')

    def tearDown(self):
        self.patcher.tearDown()

    def test_nothing_to_do(self):
        """
        With neither filesystem nor app directories to search, there can be no template_s.
        """
        self.assertEqual(
            list(
                template_finder.templates_for_engine({
                    'BACKEND': 'django.templates.backends.jinja2.Jinja2',
                    'APP_DIRS': False,
                    'DIRS': []
                })
            ),
            []
        )

    def test_filesystem_loader(self):
        """
        Using the filesystem loader, template_s. are found within the directories specified in DIRS
        for the given engine config.
        """

        self.assertEqual(
            list(
                template_finder.templates_for_engine({
                    'BACKEND': 'django.templates.backends.django.Djangotemplate.',
                    'APP_DIRS': False,
                    'DIRS': ['/tmp/project/templates/', '/tmp/project/other_templates/']
                })
            ),
            [
                ('base.html', '/tmp/project/templates/base.html'),
                ('foo/bar.html', '/tmp/project/templates/foo/bar.html'),
                ('baz.html', '/tmp/project/other_templates/baz.html'),
            ]
        )


class TestAppFinder(TestCase):
    patcher = None

    engine_config = {
        'BACKEND': 'django.templates.backends.django.Djangotemplate_tree_finder.',
        'APP_DIRS': True,
    }

    def setUp(self):
        self.patcher = Patcher()
        self.patcher.setUp()  # called in the initialization code

        # app files
        self.patcher.fs.CreateFile('/tmp/project/project/templates/abc.html')
        self.patcher.fs.CreateFile('/tmp/project/my_app/templates/my_app/def.html')
        self.patcher.fs.CreateFile('/tmp/project/your_app/templates/your_app/def.html')

        self.mock_apps = Apps(collections.OrderedDict([
            ('project', AppConfig('/tmp/project/project/')),
            ('my_app', AppConfig('/tmp/project/my_app/')),
            ('your_app', AppConfig('/tmp/project/your_app/'))
        ]))

    def tearDown(self):
        self.patcher.tearDown()  # somewhere in the cleanup code

    def test_app_loader(self):
        """
        Using the app loader, template_tree_finder. are found within the directories corresponding to the apps
        for the given engine config.
        """

        with mock.patch('template_tree.template_finder.apps', new=self.mock_apps):
            self.assertEqual(
                list(template_finder.templates_for_engine(self.engine_config)),
                [
                    ('abc.html', '/tmp/project/project/templates/abc.html'),
                    ('my_app/def.html', '/tmp/project/my_app/templates/my_app/def.html'),
                    ('your_app/def.html', '/tmp/project/your_app/templates/your_app/def.html'),
                ]
            )

    def test_exclude_apps(self):
        """
        exclude_apps excludes template_tree_finder. from the given apps
        """

        with mock.patch('template_tree.template_finder.apps', new=self.mock_apps):
            self.assertEqual(
                list(
                    template_finder.templates_for_engine(
                        self.engine_config,
                        ['my_app', 'your_app']
                    )
                ),
                [
                    ('abc.html', '/tmp/project/project/templates/abc.html')
                ]
            )

    def test_default_app_exclusion(self):
        """
        By default, the admin app is excluded.
        """
        mock_apps = Apps(collections.OrderedDict([
            ('project', AppConfig('/tmp/project/project/')),
            ('admin', AppConfig('/tmp/project/my_app/')),
            ('your_app', AppConfig('/tmp/project/your_app/'))
        ]))

        with mock.patch('template_tree.template_finder.apps', new=mock_apps):
            self.assertEqual(
                list(
                    template_finder.templates_for_engine(self.engine_config)
                ),
                [
                    ('abc.html', '/tmp/project/project/templates/abc.html'),
                    ('your_app/def.html', '/tmp/project/your_app/templates/your_app/def.html'),
                ]
            )

    def test_include_admin_apps(self):
        """
        The admin app can be included in the report, by providing an empty list
        """
        mock_apps = Apps(collections.OrderedDict([
            ('project', AppConfig('/tmp/project/project/')),
            ('admin', AppConfig('/tmp/project/my_app/')),
            ('your_app', AppConfig('/tmp/project/your_app/'))
        ]))

        with mock.patch('template_tree.template_finder.apps', new=mock_apps):
            self.assertEqual(
                list(
                    template_finder.templates_for_engine(
                        self.engine_config,
                        []
                    )
                ),
                [
                    ('abc.html', '/tmp/project/project/templates/abc.html'),
                    ('my_app/def.html', '/tmp/project/my_app/templates/my_app/def.html'),
                    ('your_app/def.html', '/tmp/project/your_app/templates/your_app/def.html'),
                ]
            )
