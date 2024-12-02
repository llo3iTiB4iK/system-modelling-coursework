from create import Create
from model import Model
from process import Process
from fun_rand import norm
from route import Route
from collections.abc import Mapping


def modify_nested_dicts(ob, func):
    for k, v in ob.items():
        if isinstance(v, Mapping):
            modify_nested_dicts(v, func)
        else:
            ob[k] = func(v)


def create_model(modified=False):
    c1 = Create(0.5, 'exp', 'Прибуття клієнтів')
    p1 = Process(0.8, 'exp', 'Обслуговування касиром 1', max_queue=3)
    p2 = Process(0.8, 'exp', 'Обслуговування касиром 2', max_queue=3)

    c1.set_routes([Route(p1, priority=2, block_condition=lambda: p1.get_queue() > p2.get_queue()), Route(p2)])

    for cashier in [p1, p2]:
        cashier.set_state(1)
        process_duration = max(norm(1, 0.3), 0)
        cashier.set_tnext(process_duration)

    c1.set_tnext(0.1)

    p1.set_queue(2)
    p2.set_queue(2)

    elements = [c1, p1, p2]

    if modified:
        p3 = Process(0, '', 'Очікування черги на виїзд', max_queue=2)
        c2 = Create(0.3, 'unif', 'Проїзд автомобілів')
        c2.set_delay_dev(0.5)
        p4 = Process(0, '', 'Проїзд автомобілів по вулиці біля банку')
        p5 = Process(0.35, '', 'Виїзд автомобіля від банку на вулицю', max_queue=0)

        p1.set_routes([Route(p3, block_condition=lambda: p3.queue_is_full())])
        p2.set_routes([Route(p3, block_condition=lambda: p3.queue_is_full())])

        p3.set_routes([Route(p5, block_condition=lambda: c2.get_tnext() - p5.get_tcurr() < p5.get_delay() or p5.get_state() == 1)])
        c2.set_routes([Route(p4)])

        elements.extend([p3, c2, p4, p5])

    return Model(elements, transition_period=TRANSITION_PERIOD)


NUM_ITER = 20
TRANSITION_PERIOD = 4000

if __name__ == "__main__":
    for is_modified in [False, True]:
        result_dict = {}
        for _ in range(NUM_ITER):
            model = create_model(modified=is_modified)
            model.simulate(5000, result_dict)
        print(f"\n------------- Результати симуляції (модифікована модель = {is_modified}): -------------")
        modify_nested_dicts(result_dict, lambda v: v / NUM_ITER)
        for key, value in result_dict.items():
            print(f"{key}: {value}")
