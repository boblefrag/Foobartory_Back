from .worker import Worker, REQUIREMENTS


class Manager:
    """
    A manager is responsible of multiple workers.
    Every turn it give seconds to all his workers and keep track of all the ressources they collect.
    (foo, bars, foobars, euros...)
    For every game the manager starts with 2 workers.
    """

    bars = 0
    foos = 0
    foobars = 0
    euros = 0
    runs = 0

    def __init__(self):
        """
        Create our 2 first workers
        """
        self.workers = [Worker(self) for _ in range(2)]

    def __repr__(self):
        return f"run: {self.runs}, {self.get_ressources()}"

    def run(self):
        """
        calling this method is like waiting for 1 second
        During this second every worker will try to create a ressource or get a new activity.
        The strategy used is very naive.
        - try to create the more valuable ressource
        - fail or succeed
        - if fail, try the next one
        - repeat until success or wait next run
        """
        for worker in self.workers:
            worker.seconds += 1
        self.runs += 1
        self.buy_worker(30)
        self.sell_foobar(12)
        self.create_foobar(10)
        self.create_foo(20)
        self.create_bar(10)

    def get_ressources(self):
        """
        used by __repr__ for a nice printing of what happens
        could be used in logging...
        """
        return {
            "foos": self.foos,
            "bars": self.bars,
            "foobars": self.foobars,
            "euros": self.euros,
            "workers": len(self.workers),
        }

    def release_workers(self, activity):
        """
        a ressource has enough elements. We release all the workers that was mining this ressource.
        """
        workers = [worker for worker in self.workers if worker.activity == activity]
        for worker in workers:
            worker.activity = None

    def create_ressource(self, activity, total=False):
        """
        for each run we try to get a new worker for this ressources.
        for low level ressource (foos and bars) we take everything!
        then for each worker in the correct activity, we mine the selected ressource
        """
        workers = [worker for worker in self.workers if worker.activity == None]
        if len(workers):
            if not total:
                workers = [workers[0]]
            for worker in workers:
                try:
                    worker.change_activity(activity)
                except AssertionError:
                    continue

        workers = [worker for worker in self.workers if worker.activity == activity]
        for worker in workers:
            try:
                getattr(worker, activity)()
            except AssertionError:
                pass

    def create_foo(self, count):
        """
        If we don't have enough foo we create some
        One always need more foos !
        """
        if self.foos >= count:
            self.release_workers("create_foo")
            return
        self.create_ressource("create_foo", total=True)

    def create_bar(self, count):
        """
        If we don't have enough bars we create some
        bar are less preecious than foos
        because when creating foobars, foos can be lost
        bars can't
        """

        if self.bars >= count:
            self.release_workers("create_bar")
            return
        self.create_ressource("create_bar", total=True)

    def create_foobar(self, count):
        """
        We try to create foobars only if we have some foos and bars
        otherwise we release our workers to mine some
        """
        if (
            self.foobars >= count
            or self.foos < REQUIREMENTS.create_foobar["foos"]
            or self.bars < REQUIREMENTS.create_foobar["bars"]
        ):
            self.release_workers("create_foobar")
            return
        self.create_ressource("create_foobar")

    def sell_foobar(self, count):
        """
        Because we can sell up to 5 foobars for only 10 seconds
        We don't even try to sell less.
        """
        if self.euros >= count or self.foobars < REQUIREMENTS.sell_foobar["foobars"]:
            self.release_workers("sell_foobar")
            return
        self.create_ressource("sell_foobar")

    def buy_worker(self, count):
        """
        It's because workers needs foos and euros that we create al little bit more foos than bars
        """
        if (
            self.euros < REQUIREMENTS.buy_worker["euros"]
            or self.foos < REQUIREMENTS.buy_worker["foos"]
            or len(self.workers) >= count
        ):
            self.release_workers("buy_worker")
            return
        self.create_ressource("buy_worker")
