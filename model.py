from process import Process
from create import Create
from random import random


class Model:

    def __init__(self, elements, transition_period=0):
        self.list = elements
        self.tnext = 0.0
        self.event = 0
        self.tcurr = self.tnext
        self.transition_period = transition_period
        self.exit_times = []
        self.queue_changes = 0

    def simulate(self, time, results):
        model_responses = []
        next_moment = 100
        for e in self.list:
            e.set_transition_period(self.transition_period)
        while self.tcurr < time:
            if not self.transition_period and self.tcurr >= next_moment:
                processed_demands = self.list[1].get_quantity() + self.list[2].get_quantity()
                time_in_bank_total = sum(self.exit_times[6:]) - sum(self.list[0].arrival_times[:len(self.exit_times[6:])])
                model_responses.append(time_in_bank_total / processed_demands)
                next_moment += 100
            self.tnext = float('inf')
            for index, e in enumerate(self.list):
                e.check_block_condition()
                if (e.get_tnext() < self.tnext or (e.get_tnext() == self.tnext and random() >= 0.5))\
                        and (isinstance(e, Create) or (isinstance(e, Process) and e.get_state() != 2)):
                    self.tnext = e.get_tnext()
                    self.event = index

            for e in self.list:
                if self.tcurr >= self.transition_period:
                    e.do_statistic(self.tnext - self.tcurr)
            self.tcurr = self.tnext
            for e in self.list:
                e.set_tcurr(self.tcurr)
            self.list[self.event].out_act()
            if self.event in (1, 2):
                self.exit_times.append(self.tcurr)
            self.check_queue_change()
        self.save_results(results)
        return model_responses

    def check_queue_change(self):
        if self.list[1].get_queue() - self.list[2].get_queue() >= 2:
            self.list[1].set_queue(self.list[1].get_queue() - 1)
            self.list[2].set_queue(self.list[2].get_queue() + 1)
            if self.tcurr >= self.transition_period:
                self.queue_changes += 1
        elif self.list[2].get_queue() - self.list[1].get_queue() >= 2:
            self.list[2].set_queue(self.list[2].get_queue() - 1)
            self.list[1].set_queue(self.list[1].get_queue() + 1)
            if self.tcurr >= self.transition_period:
                self.queue_changes += 1

    def save_results(self, results):
        def add_to_results(result_dict, key, value):
            if key in result_dict:
                result_dict[key] += value
            else:
                result_dict[key] = value

        time_modelling = self.tcurr - self.transition_period

        for e in self.list:
            if str(e) not in results:
                results[str(e)] = {}
            add_to_results(results[str(e)], "Кількість", e.get_quantity())
            if isinstance(e, Process):
                add_to_results(results[str(e)], "Середнє завантаження", e.get_load_total() / time_modelling)
                add_to_results(results[str(e)], "Середня кількість клієнтів у черзі", e.get_queue_total() / time_modelling)

        add_to_results(results, "Середня кількість клієнтів у банку",
                       (self.list[1].get_customers_total() + self.list[2].get_customers_total()) / time_modelling)
        processed_demands = self.list[1].get_quantity() + self.list[2].get_quantity()
        add_to_results(results, "Середній інтервал часу між від\'їздами клієнтів від вікон",
                       time_modelling / processed_demands)
        exit_after_transition = self.exit_times[6+self.list[0].arrived_before_transition_time:]
        enter_after_transition = self.list[0].arrival_times[self.list[0].arrived_before_transition_time:self.list[0].arrived_before_transition_time+len(exit_after_transition)]
        time_in_bank_total = sum(exit_after_transition) - sum(enter_after_transition)
        add_to_results(results, "Середній час перебування клієнта в банку", time_in_bank_total / processed_demands)
        num_refusals = self.list[1].get_refusal()
        add_to_results(results, "Відсоток клієнтів, яким відмовлено в обслуговуванні",
                       num_refusals / (self.list[1].get_quantity() + self.list[2].get_quantity() + num_refusals) * 100)
        add_to_results(results, "Кількість змін під\'їзних смуг", self.queue_changes)
