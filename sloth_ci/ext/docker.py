import docker


def extend(cls):
    class Ext(cls):
        def __init__(self, config):
            super().__init__(config)

            self.foo = 'qwe'

        def execute(self, action):
            print('Execute %s' % action)
            print('self.foo = %s' % self.foo)
    
    return Ext