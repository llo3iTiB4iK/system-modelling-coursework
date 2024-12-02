from fun_rand import exp, unif


class Element:
    nextId = 0

    def __init__(self, delay=1.0, dist=None, name=None):
        self.tnext = 0.0
        self.tcurr = self.tnext
        self.delay_mean = delay
        self.delay_dev = None
        self.distribution = dist
        self.id_ = Element.nextId
        Element.nextId += 1
        self.name = name if name else f'element{self.id_}'
        self.quantity = 0
        self.routes = []
        self.transition_period = 0

    def __str__(self):
        return self.name

    def get_delay(self):
        delay = self.delay_mean
        if self.distribution.lower() == 'exp':
            delay = exp(self.delay_mean)
        elif self.distribution.lower() == 'unif':
            delay = unif(self.delay_mean, self.delay_dev)
        return delay

    def set_delay_dev(self, delay_dev):
        self.delay_dev = delay_dev

    def get_distribution(self):
        return self.distribution

    def set_distribution(self, distribution):
        self.distribution = distribution

    def get_quantity(self):
        return self.quantity

    def get_tcurr(self):
        return self.tcurr

    def set_tcurr(self, tcurr):
        self.tcurr = tcurr

    def set_routes(self, routes):
        self.routes = routes

    def is_blocked(self):
        if not self.routes:
            return False
        return all(route.blocked for route in self.routes)

    def check_block_condition(self):
        for route in self.routes:
            if route.block_condition:
                route.blocked = route.block_condition()

    def get_next_element(self):
        if not self.routes:
            return None
        routes_by_priority = sorted(self.routes, key=lambda r: r.priority, reverse=True)
        if self.is_blocked():
            return routes_by_priority[0]
        else:
            for route in routes_by_priority:
                if not route.blocked:
                    return route

    def in_act(self):
        pass

    def out_act(self):
        if self.tcurr >= self.transition_period:
            self.quantity += 1

    def get_tnext(self):
        return self.tnext

    def set_tnext(self, tnext):
        self.tnext = tnext

    def do_statistic(self, delta):
        pass

    def set_transition_period(self, t):
        self.transition_period = t
