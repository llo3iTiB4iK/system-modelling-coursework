import sys
from element import Element


class Process(Element):

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.queue = 0
        self.max_queue = kwargs.get('max_queue', sys.maxsize)
        self.state = 0
        self.load_total = 0
        self.customers_total = 0
        self.queue_total = 0
        self.refusal = 0

    def in_act(self):
        if self.state == 2 and super().get_tnext() == float('inf'):
            super().set_tnext(super().get_tcurr() + super().get_delay())
        elif self.state == 0:
            self.state = 1
            super().set_tnext(super().get_tcurr() + super().get_delay())
        else:
            if self.queue_is_full():
                if self.tcurr > self.transition_period:
                    self.refusal += 1
                return False
            else:
                self.queue += 1
        return True

    def out_act(self):
        next_route = super().get_next_element()
        if not next_route or not next_route.blocked:
            super().out_act()
            super().set_tnext(float('inf'))
            self.state = 0

            if self.queue > 0:
                self.queue -= 1
                self.state = 1
                super().set_tnext(super().get_tcurr() + super().get_delay())

            if next_route:
                next_route.element.in_act()

    def check_block_condition(self):
        was_blocked = super().is_blocked()
        super().check_block_condition()
        if super().is_blocked():
            self.state = 2
        elif was_blocked:
            if super().get_tnext() < float('inf'):
                self.state = 1
                super().set_tnext(super().get_tcurr())
            else:
                self.state = 0

    def do_statistic(self, delta):
        is_busy = int(super().get_tnext() < float('inf'))
        self.load_total += is_busy * delta
        self.customers_total += (is_busy + self.queue) * delta
        self.queue_total += self.queue * delta

    def get_queue(self):
        return self.queue

    def set_queue(self, queue):
        self.queue = queue

    def queue_is_full(self):
        return self.queue == self.max_queue

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_refusal(self):
        return self.refusal

    def get_load_total(self):
        return self.load_total

    def get_customers_total(self):
        return self.customers_total

    def get_queue_total(self):
        return self.queue_total
