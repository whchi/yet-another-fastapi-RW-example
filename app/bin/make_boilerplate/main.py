from enum import Enum
import re

from mako.template import Template
import typer

from app.core.filesystem.file_util import FileUtil
from app.helpers import app_path

app = typer.Typer()


def context(name: str) -> None:
    context_path = app_path(f'api/contexts/{name}')
    if FileUtil.exists(app_path(context_path)):
        typer.secho(f'context "{name}" already exists',
                    fg=typer.colors.RED,
                    bg=typer.colors.BLACK)
        return

    dirs = ['domain', 'gateway', 'usecase']
    for dir_ in dirs:
        FileUtil.make_dirs(f'{context_path}/{dir_}')
        FileUtil.write(f'{context_path}/{dir_}/__init__.py', '')

    FileUtil.write(f'{context_path}/__init__.py',
                   'from .router import router\n\n__all__ = [\'router\']\n')
    template = Template(filename=app_path('bin/make_boilerplate/stubs/router.mako'))
    FileUtil.write(f'{context_path}/router.py', template.render_unicode())

    typer.secho(f'context "{name}" created',
                fg=typer.colors.GREEN,
                bg=typer.colors.BLACK)


def model(name: str) -> None:
    models = FileUtil.get_all_files(app_path('models'))
    existing_model_names = [f.split('/')[-1][:-3] for f in models]

    if name in existing_model_names:
        typer.secho(f'model "{name}" already exists',
                    fg=typer.colors.RED,
                    bg=typer.colors.BLACK)
        return

    import inflect
    template = Template(filename=app_path('bin/make_boilerplate/stubs/model.mako'))
    content = template.render_unicode(table_name=inflect.engine().plural_noun(name),
                                      model=snake_to_pascal(name))
    FileUtil.write(app_path(f'models/{name}.py'), content)

    typer.secho(f'model "{name}" created', fg=typer.colors.GREEN, bg=typer.colors.BLACK)


def pascal_to_snake(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def snake_to_pascal(name: str) -> str:
    return ''.join(word.title() for word in name.split('_'))


class BoilerplateType(str, Enum):
    model = 'model'
    context = 'context'


@app.command()
def main(boilerplate_type: BoilerplateType, name: str) -> None:
    name = pascal_to_snake(name)
    match boilerplate_type:
        case 'model':
            model(name)
        case 'context':
            context(name)
        case _:
            raise NotImplementedError


if __name__ == '__main__':
    app()
