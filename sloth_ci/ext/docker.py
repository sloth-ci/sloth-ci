from sloth_ci.sloth import Sloth as BaseSloth

import docker


class Sloth(BaseSloth):
    def __init__(self, config):
        super().__init__(config)

        self.foo = 'qwe'

    def execute(self, action):
        print('Execute %s' % action)
        print('self.foo = %s' % self.foo)