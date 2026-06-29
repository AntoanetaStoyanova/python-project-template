"""Entry point for {{cookiecutter.project_name}}."""

from {{cookiecutter.project_slug}}.log import setup_logging

PROJECT_NAME = "{{cookiecutter.project_slug}}"

# dans les autres module .py 
# import logging
#  logger = logging.getLogger(__name__)
def main() -> None:
    logger = setup_logging(PROJECT_NAME)
    logger.info("Starting %s", PROJECT_NAME)


if __name__ == "__main__":
    main()
