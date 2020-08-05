# Flask REST API Template

Repository template for using flask as a restful API.

### Includes:

* Web development framework with [flask](https://flask.palletsprojects.com/en/1.1.x/)
* Simple API building with [flask-restful](https://flask-restful.readthedocs.io/en/latest/)
* Dependency management with [poetry](https://python-poetry.org/)
* Testing with [pytest](https://docs.pytest.org/en/stable/)
* Job scheduling with [RQ](https://python-rq.org/)
* Configuration management with [dynaconf](https://github.com/rochacbruno/dynaconf)
* Logging with [loguru](https://github.com/Delgan/loguru)
* Development task automation with [doit](https://pydoit.org/)
* Database with [MongoDB](https://www.mongodb.com/) and [pymongo](https://pymongo.readthedocs.io/en/stable/)
* Caching with [Redis](https://redis.io/) and [python-redis](https://pypi.org/project/redis/)

### And Also:

* Easy development with [docker-compose](https://docs.docker.com/compose/)
* Build pipeline already established for exporting a docker image.
* [Github Actions](https://github.com/features/actions) set up to run Continuous Integration
* 100% Test coverage, including unit and end to end testing
* Sample Todo app, showcasing how to use the template

# Getting Started

Make sure you have, `poetry`, `docker` and `docker-compose` installed and run
the following:

```
$ poetry install
...
$ poetry run doit bootstrap --name my-application-name
...
$ docker-compose up
```

Open [localhost:5000/hello](http://localhost:5000/hello), you should be seeing
`["Hello", "Flask", "Template!"]`.


# How To

## Run automated unit test suite

```
$ poetry run doit test
```

## Run automated end to end tests

```
$ docker-compose up
... in another terminal ...
$ poetry run doit e2e
```
