import click
from ._builder import build


@click.command()
@click.option("--db_project", type=str)
@click.option("--config_dir", default="./db_projects", type=str)
@click.option("--config_file", default="config.yml", type=str)
def main(db_project, config_dir, config_file):

    #render the SQL templates and build into a single script or notebook.
    build(db_project, config_dir, config_file)

if __name__ == "__main__":
    main()
