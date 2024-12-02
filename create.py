from element import Element


class Create(Element):

    def __init__(self, *args):
        super().__init__(*args)
        super().set_tnext(0.0)
        self.arrival_times = []
        self.arrived_before_transition_time = 0

    def out_act(self):
        super().out_act()
        next_route = super().get_next_element()
        super().set_tnext(super().get_tcurr() + super().get_delay())
        if next_route.element.in_act():
            self.arrival_times.append(super().get_tcurr())
            if super().get_tcurr() < self.transition_period:
                self.arrived_before_transition_time += 1
