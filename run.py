from foobar_workers.manager import Manager


if __name__ == "__main__":
    manager = Manager()
    while len(manager.workers) < 30:
        manager.run()
        print(manager)
