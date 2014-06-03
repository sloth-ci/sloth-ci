def extend(cls):
    class Ext(cls):
        def __init__(self, config):
            super().__init__(config)

        def execute(self, action):
            print('Hello from a dummy executor that ignores the action and just does nothing.')
    
    return Ext