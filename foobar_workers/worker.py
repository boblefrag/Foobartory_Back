import random
from .utils import validate


def check_foobar(worker):
    val = random.random()
    if int(val * 100) < 60:
        return ("foobars", worker.manager.foobars + 1)
    else:
        return ("bars", worker.manager.bars + 1)


def check_bar_price():
    return random.uniform(0.5, 2.0)


class REQUIREMENTS:
    create_foo = {"seconds": 1}
    create_bar = {"seconds": check_bar_price}
    create_foobar = {"seconds": 2, "foos": 1, "bars": 1}
    sell_foobar = {"seconds": 10, "foobars": 5}
    buy_worker = {"euros": 3, "foos": 6}
    change_activity = {"seconds": 5}


RETRIBUTIONS = {
    "create_foo": lambda worker: ("foos", worker.manager.foos + 1),
    "create_bar": lambda worker: ("bars", worker.manager.bars + 1),
    "create_foobar": lambda worker: check_foobar(worker),
    "sell_foobar": lambda worker: ("euros", worker.manager.euros + 5),
}


class Worker:
    """
    A worker is the smallest possible unit of work
    it can:
    - create `foo`
    - create `bar`
    - merge `bar` with `foo` to create a `foobar`
    - sell `foobars` to earn euros
    - buy a new worker
    - change activity
    """

    seconds = 0
    activity = None

    @property
    def bars(self):
        return self.manager.bars

    @property
    def foos(self):
        return self.manager.foos

    @property
    def foobars(self):
        return self.manager.foobars

    @property
    def euros(self):
        return self.manager.euros

    @classmethod
    def activities(cls):
        """
        create a dict that define all the acivities available with this worker
        """
        return {
            func: getattr(cls, func)
            for func in dir(cls)
            if callable(getattr(cls, func))
            and not func.startswith("_")
            and not func == "activities"
        }

    def __init__(self, manager):
        self.manager = manager

    def __repr__(self):
        return f"{self.activity}"

    def _pay_requirements(self, **requirements):
        """
        worker has to pay a requirement to complete a task.
        the @validate decorator took care of the ressources
        before calling this method.

        This way debt is always paid.

        seconds are a worker currency but other ressources are manager's
        """
        for k, v in requirements.items():
            if k not in ["seconds"]:
                obj = self.manager
            else:
                obj = self
            attr = getattr(obj, k)
            setattr(obj, k, attr - v)

    @validate(**REQUIREMENTS.create_foo)
    def create_foo(self, **requirements):
        """
        create_foo like other functions does the same work.
        - ensure requirements are met with validate decorator.
        - pay the resquirement
        - get the retribution
        - send it to the manager
        """
        self._pay_requirements(**requirements)
        attr, value = RETRIBUTIONS["create_foo"](self)
        setattr(self.manager, attr, value)

    @validate(**REQUIREMENTS.create_bar)
    def create_bar(self, **requirements):
        self._pay_requirements(**requirements)
        attr, value = RETRIBUTIONS["create_bar"](self)
        setattr(self.manager, attr, value)

    @validate(**REQUIREMENTS.create_foobar)
    def create_foobar(self, **requirements):
        self._pay_requirements(**requirements)
        attr, value = RETRIBUTIONS["create_foobar"](self)
        setattr(self.manager, attr, value)

    @validate(**REQUIREMENTS.sell_foobar)
    def sell_foobar(self, **requirements):
        self._pay_requirements(**requirements)
        attr, value = RETRIBUTIONS["sell_foobar"](self)
        setattr(self.manager, attr, value)

    @validate(**REQUIREMENTS.buy_worker)
    def buy_worker(self, **requirements):
        """
        buy_worker is a little bit different from his fellows
        it validate, pay requirements but directly create a worker
        for his manager.
        """
        self._pay_requirements(**requirements)
        self.manager.workers.append(Worker(self.manager))

    @validate(**REQUIREMENTS.change_activity)
    def change_activity(self, activity="create_foo", **requirements):
        """
        You will never see a worker in `change_activity` task
        as soon as the requirements are mets, the change is instant
        """
        self._pay_requirements(**requirements)
        self.activity = activity
