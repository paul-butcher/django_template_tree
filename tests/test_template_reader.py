from template_tree.template_reader import to_tree

from django.test import TestCase

from pyfakefs.fake_filesystem_unittest import Patcher


class TestTemplateReader(TestCase):

    patcher = None

    def setUp(self):
        self.patcher = Patcher()
        self.patcher.setUp()

    def tearDown(self):
        self.patcher.tearDown()

    def test_nothing_to_do(self):
        self.assertEqual(to_tree([], 'banana'), {'name': 'banana'})

    def test_flat(self):
        """
        If none of the templates have  {% extends %}, the result will be flat
        """
        self.patcher.fs.CreateFile('/tmp/project/templates/base.html')
        self.patcher.fs.CreateFile('/tmp/project/templates/foo/bar.html', contents='hello dolly')
        self.patcher.fs.CreateFile('/tmp/project/other_templates/baz.html')

        self.assertEqual(
            to_tree(
                [
                    ('base.html', '/tmp/project/templates/base.html'),
                    ('foo/bar.html', '/tmp/project/templates/foo/bar.html'),
                    ('baz.html', '/tmp/project/other_templates/baz.html'),
                ],
                'banana'
            ),
            {
                'name': 'banana',
                'children': [
                    {'name': 'base.html'},
                    {'name': 'baz.html'},
                    {'name': 'foo/bar.html'}
                ],
            }
        )


    def test_extends(self):
        """
        If {%extends%} contains a string, a tree will be formed
        """
        self.patcher.fs.CreateFile('/tmp/project/templates/base.html')
        self.patcher.fs.CreateFile(
            '/tmp/project/templates/foo/bar.html',
            contents='{% extends "base.html"%}'
        )
        self.patcher.fs.CreateFile(
            '/tmp/project/other_templates/baz.html',
            contents='{% extends "base.html"%}'
        )

        self.assertEqual(
            to_tree(
                [
                    ('base.html', '/tmp/project/templates/base.html'),
                    ('foo/bar.html', '/tmp/project/templates/foo/bar.html'),
                    ('baz.html', '/tmp/project/other_templates/baz.html'),

                ],
                'banana'
            ),
            {
                'name': 'banana',
                'children': [
                    {
                        'name': 'base.html',
                        'children': [
                            {'name': 'baz.html'},
                            {'name': 'foo/bar.html'},
                        ]
                    },
                ],
            }
        )

    def test_variable_extends(self):
        """
        If {%extends%} contains a variable, it becomes a child of __unknown__
        """
        self.patcher.fs.CreateFile('/tmp/project/templates/base.html')
        self.patcher.fs.CreateFile(
            '/tmp/project/templates/foo/bar.html',
            contents='{% extends base %}'
        )
        self.patcher.fs.CreateFile('/tmp/project/other_templates/baz.html')

        self.assertEqual(
            to_tree(
                [
                    ('base.html', '/tmp/project/templates/base.html'),
                    ('foo/bar.html', '/tmp/project/templates/foo/bar.html'),

                ],
                'banana'
            ),
            {
                'name': 'banana',
                'children': [
                    {
                        'name': '__unknown__',
                        'children': [
                            {'name': 'foo/bar.html'}
                        ]
                    },
                    {'name': 'base.html'}
                ],
            }
        )

    def test_bad_extends(self):
        """
        If extends is not the first tag, it is ignored.
        """
        self.patcher.fs.CreateFile('/tmp/project/templates/base.html')
        self.patcher.fs.CreateFile(
            '/tmp/project/templates/foo/bar.html',
            contents="hello {% firstof world dolly sailor %} {% extends 'base.html'%}")

        self.assertEqual(
            to_tree(
                [
                    ('base.html', '/tmp/project/templates/base.html'),
                    ('foo/bar.html', '/tmp/project/templates/foo/bar.html'),
                ],
                'banana'
            ),
            {
                'name': 'banana',
                'children': [
                    {'name': 'base.html'},
                    {'name': 'foo/bar.html'}
                ],
            }
        )
