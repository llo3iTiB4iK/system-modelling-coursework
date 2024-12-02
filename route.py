
class Route:

    def __init__(self, element, priority=1, blocked=False, block_condition=None):
        self.element = element
        self.priority = priority
        self.blocked = blocked
        self.block_condition = block_condition
