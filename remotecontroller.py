from playercontroller import PlayerController

class RemoteController(PlayerController):

    def __init__(self, conn):
        self.conn = conn

    def ask_yaniv(self):
        pass

    def ask_assaf(self):
        pass

    def ask_play(self, cards, stack_top):
        pass

    def ask_draw(self):
        pass

    def publish_msg(self, msg):
        pass
