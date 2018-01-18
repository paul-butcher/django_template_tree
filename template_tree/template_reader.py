import os
import re

from django.conf import settings

from .template_finder import templates_for_engine


def all_templates(exclude_apps=None):
    return {
        'name': 'TEMPLATES',
        'children': [
            to_tree(
                templates_for_engine(engine, exclude_apps),
                engine['BACKEND'].rpartition(".")[2]
            ) for engine in settings.TEMPLATES
        ]
    }


def to_tree(templates, tree_name):
    template_dict = dict(templates)
    out_dict = {}
    re_template_tag = re.compile('\{\%\s*(.+?)\s*\%\}')\
    # Grab a separate copy of the key value pairs, they will be deleted from the dict
    # in the loop
    items = list(template_dict.items())
    for key, value in items:
        with open(value, 'r') as template_file:
            for line in template_file:
                match = re_template_tag.search(line)
                if match:
                    name, args = parse_templatetag(match.group(1))
                    if name == 'extends':
                        parent = parent_template_name(args)
                        if parent not in out_dict:
                            out_dict[parent] = []
                        out_dict[parent].append((key,out_dict.get(key, [])))
                        del template_dict[key]
                    # Extends must be the first tag in the document.
                    # Regardless of whether this is an extends tag,
                    # this file is over.
                    break

    # Collect all orphans in the final output.
    # These will bring with them all of their descendants.
    for key in template_dict.keys():
        out_dict[key] = out_dict.get(key, [])

    return to_d3_tree_format(tree_name, sorted(out_dict.items()))

def parent_template_name(parent_arg):
    """
    Given the argument of an {% extends %} tag, return the name of the template to which it links

    If the argument is a variable, return "__unknown__".  This is a static analyser of the template
    hierarchy, and cannot know all possible values that might be provided.
    """
    parent = parent_arg.strip(""""'""")
    if parent == parent_arg:
        parent = "__unknown__"
    return parent


def to_d3_tree_format(node_name, children):

    out = {'name': node_name}
    if children:
        out['children'] = [to_d3_tree_format(key, sorted(value)) for key, value in children]
    return out


def parse_templatetag(tag_content):
    name, _, args = tag_content.partition(' ')
    return name, args.strip()
