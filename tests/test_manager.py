from foobar_workers.manager import Manager


def test_manager_add_seconds_running():
    """
    GIVEN a Manager and his first run
    WHEN `run` is called
    THEN each worker get a second and each worker activity is None (it needs 5 seconds to do so)
    """
    peter = Manager()
    assert len(peter.workers) == 2

    peter.run()
    for worker in peter.workers:
        assert worker.seconds == 1
        assert worker.activity == None
    assert peter.get_ressources() == {
        "bars": 0,
        "foos": 0,
        "foobars": 0,
        "euros": 0,
        "workers": 2,
    }


def test_manager_put_workers_on_load():
    """
    GIVEN a Manager and his workers
    WHEN running for 5 seconds
    THEN workers are in `create_foo` but no foos are produced yet
    """

    peter = Manager()
    for _ in range(5):
        peter.run()

    for worker in peter.workers:
        assert worker.seconds == 0
        assert worker.activity == "create_foo"
        assert peter.foos == 0


def test_manager_create_foos():
    """
    GIVEN a Manager and his workers
    WHEN running for 6 seconds
    THEN each workers produce a foo
    """

    peter = Manager()
    for worker in peter.workers:
        worker.seconds = 0
        worker.activity = "create_foo"
    peter.run()
    for worker in peter.workers:
        assert worker.seconds == 0
        assert worker.activity == "create_foo"
        assert peter.foos == 2


def test_manager_create_bars():
    """
    GIVEN a Manager and his workers
    WHEN he create enough foos
    THEN each workers produce bars
    """

    peter = Manager()
    peter.foos = 20
    for worker in peter.workers:
        worker.seconds = 4
        worker.activity = "create_foo"
    peter.run()
    for worker in peter.workers:
        assert worker.seconds == 0
        assert worker.activity == "create_bar"


def test_manager_produce_all_workers():
    """
    GIVEN a Manager and his workers
    WHEN he runs continiously
    THEN he eventualy create 30 workers
    """

    peter = Manager()
    i = 0  # this counter is here to avoid infinite loop if something goes wrong.
    while len(peter.workers) < 30 or i < 350:
        peter.run()
        i += 1
    # if 2 workers were creating workers at the same time we will get 31 instead of 30
    assert len(peter.workers) >= 30
