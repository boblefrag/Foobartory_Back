class ValidationError(Exception):
    pass

def validate(**requirements):
    """
    Ensure worker has enough ressources to complete a task. Raises a ValidationError otherwise
    Ensure worker is on the right activity. Raises ValueError otherwise
    """

    def _check_requirements(f):
        def wrapper(self, *args):
            if self.activity != f.__name__ and f.__name__ != "change_activity":
                raise ValueError(
                    f"Worker is on {self.activity} activity, not {f.__name__}"
                )
            func_kwargs = {}
            for requirement, value in requirements.items():
                if callable(value):
                    # the value expected can be any callable
                    # we compute the result of the callable before checking for validity
                    func_val = value()
                else:
                    func_val = value
                func_kwargs[requirement] = func_val
                try:
                    assert getattr(self, requirement) >= func_val
                except AssertionError:
                    raise ValidationError()
            return f(self, *args, **func_kwargs)

        return wrapper

    return _check_requirements
