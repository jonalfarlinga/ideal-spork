from random import shuffle


def get_low(target_set):
    for target in target_set:
        if target.resilience > 0:
            return target


def get_high(target_set):
    for target in target_set[::-1]:
        if target.resilience > 0:
            return target


def target_basic(target_set):
    return get_low(target_set)


def target_random(target_set):
    shuffle(target_set)
    return get_low(target_set)


def target_weakest(target_set):
    target_set.sort(key=lambda entity: entity.resilience)
    return get_low(target_set)


def target_strongest(target_set):
    target_set.sort(key=lambda entity: entity.resilience)
    return get_high(target_set)


def target_next_active(target_set):
    target_set.sort(key=lambda entity: entity.turnmeter)
    return get_high(target_set)


def target_weak_to_power(target_set):
    target_set.sort(key=lambda entity: entity.a_defense)
    return target_weakest(target_set)


def target_weak_to_accuracy(target_set):
    target_set.sort(key=lambda entity: entity.a_defense)
    return target_weakest(target_set)


def target_weak_to_will(target_set):
    target_set.sort(key=lambda entity: entity.w_defense)
    return target_weakest(target_set)
