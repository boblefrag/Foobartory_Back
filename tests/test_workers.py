from unittest.mock import Mock, patch
import pytest
from foobar_workers.manager import Manager
from foobar_workers.worker import REQUIREMENTS, Worker


@patch("random.random", return_value=0.1)
@patch("random.uniform", return_value=2)
@pytest.mark.parametrize("activity", Worker.activities().keys())
def test_task_success(mock_random, mock_uniform, activity):
    """
    GIVEN a worker with enough ressources
    WHEN doing an activity
    THEN the activity succeed and rssources are consumed
    """
    john = Manager()
    paul = Worker(john)
    paul.activity = activity

    # we need to give paul all the ressources he needs to complete his tasks
    for k, v in getattr(REQUIREMENTS, activity).items():
        if callable(v):
            v = v()
        if k not in ["seconds"]:
            setattr(paul.manager, k, v)
        else:
            setattr(paul, k, v)
    # complete the task
    getattr(paul, activity)()

    # check that requirements are consumed
    for ressource in getattr(REQUIREMENTS, activity).keys():
        if ressource not in ["seconds"]:

            assert getattr(paul.manager, ressource) == 0
        else:
            assert getattr(paul, ressource) == 0


@pytest.mark.parametrize("activity", Worker.activities().keys())
def test_task_not_enough_ressource(activity):
    """
    GIVEN a worker with no ressources
    WHEN trying to do an activity
    THEN AssertionError is raised
    """
    john = Manager()
    paul = Worker(john)
    paul.activity = activity
    with pytest.raises(AssertionError):
        getattr(paul, activity)()


@pytest.mark.parametrize("activity", Worker.activities().keys())
def test_task_not_on_activity(activity):
    """
    GIVEN a worker with no activity
    WHEN trying to do an activity
    THEN ValueError is raised
    """
    john = Manager()
    paul = Worker(john)
    if activity != "change_activity":
        with pytest.raises(ValueError):
            getattr(paul, activity)()
