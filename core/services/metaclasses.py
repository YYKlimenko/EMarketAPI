from fastapi import Depends


class ServiceMeta(type):

    def __new__(mcs, name, base, dct):
        repository = dct.get('repository')
        if repository is None:
            raise AttributeError('The repository didn\'t find')

        def __init__(self, repository=Depends(repository)):
            self.repository = repository
            self.updatable_fields = self.updatable_fields or [
                attr for attr in self.response_schema.__fields__ if attr != 'id'
            ]

        cls = super().__new__(mcs, name, base, dct)
        cls.__init__ = __init__
        return cls
