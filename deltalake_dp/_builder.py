from typing import Iterator
from jinja2.loaders import DictLoader, FileSystemLoader
import yaml
import os
import shutil
import itertools
from jinja2 import Environment, Undefined
from pathlib import Path
from collections import ChainMap
from ._utils import Index, NoAliasDumper, ObjectType


def _load_config(config_dir: str, config_filename: str):
    # prep the paths
    config_path = f"{config_dir}/{config_filename}"

    # serialize the config
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    return config


def _get_db_object_list(project_path: str, object_type: ObjectType):

    if object_type == ObjectType.DATABASES:
        objects_path = project_path
    else:
        objects_path = f"{project_path}/{object_type.name.capitalize()}"

    object_names = [
        Path(f).stem for f in os.listdir(objects_path) if f.endswith(".sql")
    ]
    return object_names


def _get_db_object_key_index(db_project: str, config: dict, object_names: Iterator):

    index_keys = [
        config["projects"][db_project].keys(),
        config["environments"].keys(),
        object_names,
    ]
    index_keys = [Index.get_index(p) for p in itertools.product(*index_keys)]
    return index_keys


def _render_object_params(db_project: str, object_keys: Iterator, config: dict):

    template_dict = {}
    for k in object_keys:
        env = Index.get_index_env(k)
        contents: str = yaml.dump(
            config["environments"][env],
            indent=NoAliasDumper.INDENT,
            Dumper=NoAliasDumper,
        )
        template_dict[k] = contents

    param_loader = DictLoader(template_dict)
    param_env = Environment(loader=param_loader, undefined=Undefined)

    param_dict = {}
    for k in template_dict.keys():
        db = Index.get_index_db(k)
        dbenv = Index.get_index_env(k)
        table = Index.get_index_table(k)
        params = config["projects"][db_project][db]
        params["database_name"] = db
        params["table_name"] = table
        params["storage"] = config["environments"][dbenv]["storage"]
        template = param_env.get_template(k)
        rendered = template.render(params)
        rendered = yaml.safe_load(rendered)

        param_dict[k] = dict(ChainMap(params, rendered))

    return param_dict


def _build_obj_parameters(
    db_project: str, path: str, config: dict, obj_type: ObjectType
):

    objs = _get_db_object_list(f"{path}/{db_project}", obj_type)
    obj_keys = _get_db_object_key_index(db_project, config, objs)
    obj_param = _render_object_params(db_project, obj_keys, config)

    return obj_param


def _build_parameters(db_project: str, path: str, config: dict):

    all_params = {}

    for o in ObjectType:
        obj_param = _build_obj_parameters(db_project, path, config, o)
        all_params = ChainMap(obj_param, all_params)

    all_params = dict(all_params)

    return all_params


def _create_build_dir(build_path: str):

    if os.path.exists(build_path):
        shutil.rmtree(build_path)
    else:
        os.makedirs(build_path)


def _render_script(env: Environment, index: str, params: dict, scripts: dict):
    def lookup_template(tpt: str) -> bool:
        return Path(tpt).stem == Index.get_index_table(index)

    l = env.list_templates(filter_func=lookup_template)[0]
    template = env.get_template(l)
    rendered = template.render(params)
    rendered = f"{rendered};\n\n"

    dbenv = Index.get_index_env(index)
    db = Index.get_index_db(index)
    script_filename = f"{dbenv}_{db}.sql"
    try:
        s = scripts[script_filename]
        s = f"{s}{rendered}"
    except KeyError:
        s = rendered

    scripts[script_filename] = s


def _save_scripts(db_project: str, build_path: str, scripts: dict):
    os.makedirs(f"{build_path}/{db_project}", exist_ok=True)
    for k, v in scripts.items():

        save_path = f"{build_path}/{db_project}/{k}"

        with open(save_path, "w") as f:
            f.write(v)


def build(db_project: str, path: str, config_filename: dict):

    # load the configuration file into a dict
    config = _load_config(path, config_filename)

    # create the build directory where the build scripts will be created
    build_path = f"{path}_build"
    _create_build_dir(build_path)

    # build the parameter dictionary for each table
    # The parameters are held in the configuration file and are jinja templated themselves
    # the parameters for which are in the same config file. This process:
    # 1. renders out the jinja
    # 2. blows out the parameters for each db object
    # 3. index keys them in a dictionary with the convention
    #    [database]![environment]![objectname]
    # The net result is that we have a dictionary of jinja parameters
    # for each sql object file that we can easily lookup and use.
    params = _build_parameters(db_project, path, config)

    # load the sql files into jinja
    project_path = f"{path}/{db_project}"
    loader = FileSystemLoader(project_path)
    env = Environment(loader=loader, undefined=Undefined)

    # render the scripts for each environment and db into a dictionary
    # for every keyed object in the parameters dict
    scripts = {}
    for k, v in params.items():
        _render_script(env, k, v, scripts)

    # save the scripts to the build directory
    _save_scripts(db_project, build_path, scripts)
