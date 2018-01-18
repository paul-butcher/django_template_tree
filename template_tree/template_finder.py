import os
from django.apps import apps

def templates_for_engine(engine_config, exclude_apps=None):
    """
    Given a template engine definition, as found in the settings.TEMPLATES list,
    iterates over the templates accessible to that engine.

    By default, the admin app is excluded.

    :param engine_config: A template engine definition
    :param exclude_apps: A list of apps to be excluded.
    """
    filesystem_dirs = engine_config.get('DIRS', [])
    for filesystem_dir in filesystem_dirs:
        for path_to_file in files_in_path(os.path.join(filesystem_dir,'')):
            yield path_to_file

    if engine_config.get('APP_DIRS', False):
        for path in all_app_templates(exclude_apps if exclude_apps is not None else ["admin"]):
            yield path


def files_in_path(top):
    """
    Iterates over all files within the given 'top' directory.

    Uses the default os.walk behaviour.
    """
    top_length = len(top)
    for listing in os.walk(top):
        for template_file in listing[2]:
            full_path = os.path.join(listing[0], template_file)
            yield (full_path[top_length:], full_path)


def all_app_templates(exclude_apps):
    return app_templates([value for key, value in apps.app_configs.items() if key not in exclude_apps])


def app_templates(app_configs):
    for app_config in app_configs:
        template_path = os.path.join(app_config.path, 'templates', '')
        for path_to_file in files_in_path(template_path):
            yield path_to_file

