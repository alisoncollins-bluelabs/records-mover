# Database drivers

Adding a database driver to records_mover can be divided up into three steps:

* Add integration testing and subclass DBDriver to get tests to pass
* Add code for native bulk import support
* Add code for native bulk export support

Here are the basic things you'll need to do to get through the
process.  Every database is different, and this document only gets
updated periodically, so you may run into additional things you need
to do or figure out.  If they seem like things people will hit in the
future, add them to this document!

## Basic support

1. Create a feature branch
2. Get a test database set up
  * Modify `tests/integration/docker-compose.yml` to include a Docker
    image for your new database.  If your database can't be run in a
    Docker image, you'll need some way to get to a database that can
    be used during integration testing.  Be sure to add a link from
    the 'records_mover' container to your new container.
  * Run `./itest-dc up -d` to bring up the docker-compose environment.
  * Run `./itest-dc start` to start the docker-compose environment.
  * Watch logs with `./itest-dc logs -f`
  * Fix any issues and repeat until it is successful and the logs look right.
2. Set up the `itest` script to be able to test your new database.
  * Modify the `local_dockerized_dbfacts` function in `./itest` to
    point to the new database.
  * Create a `wait-for-${your-new-db-type:?}.sh` script matching
    `wait-for-postgres.sh`.
  * Modify `tests/integration/inside-docker-dbfacts.yml` to include an
    entry for your new database.
  * Modify `tests/integration/bin/db-connect` to handle your new
    database type if needed.
  * Modify `Dockerfile` to add any new client binaries needed for your
    database and run `./itest --docker build` to build the new image.
  * Run `./itest shell`, which will start the docker-compose and start
    a shell with the db-facts you just created set.
  * Run `db ${your-new-db-name:?}` within that shell and verify it
    connects.
  * Exit out of the `./itest shell` session.
  * Run `./itest ${your-new-db-type:?}` and verify it doesn't
    recognize the argument.
  * Search down for instances of 'postgres' in the `itest` script and
    come up with the equivalent for your new database.
  * Run `./itest ${your-new-db-type:?}` again and verify thigns fail
    somewhere else (e.g., a Python package not being installed or a
    test failing most likely)
  * Push up your changes to the feature branch.
2. Now work to get the same failure out of CircleCI:
  * Replicate the current `postgres_itest` in `.circleci/config.yml`,
    including matching all of the references to it.
  * Be sure to change the `with-db dockerized-postgres` line to refer
    to your database type.
  * Push up changes and verify that tests fail because your new
    database "is not a valid DB name".
  * Note that you can (temporarily!) allow your new integration test
    to run without waiting for unit and Redshift tests to run by
    commenting out the dependency like this - just be sure to leave an
    annotation comment reminding you to fix it before the PR is
    merged!
    ```yaml
    #          requires:  # TODO restore this
    #            - redshift-itest
    ```
  * Modify the `integration_test_with_dbs` job to include a Docker
    image for your new database, similar to `docker-compose.yml`
    above.
  * Modify `tests/integration/circleci-dbfacts.yml` to point to your
    new integration test database account, whether in Docker or
    cloud-hosted.
  * Iterate on the errors until you get the same errors you got in
    your `./itest` runs.
3. Fix the tests!
  * Now that you have tests running (and failing), you can address the
    problems one by one.  Here are things you are likely to need to
    do--I'd suggest waiting for the problem to come up via the test
    and then applying the fix until the tests pass.  If you encounter
    things not on the list below, add them here for the next person!
  * Add Python driver (either SQLAlchemy or if SQLAlchemy supports it
    natively, maybe just the DBAPI driver) as a transtive dependency
    in `setup.py`.  Rerun `./deps.sh` and then `./itest --docker
    build` to re-install locally.
  * If database connections aren't working, you may want to insert
    some debugging into `records_mover/db/connect.py` to figure out
    what's going on.
4. If there are things you see below that you know are needed from the
   above list, but the tests are passing, consider adding an
   integration test to match.
5. Add support for bulk import if the database supports it TODO
5. Add support for bulk export if the database supports it TODO