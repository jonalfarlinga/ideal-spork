from random import shuffle


def get_top(entity_set):
    for target in entity_set:
        if target.resilience > 0:
            return target


def target_basic(entity_set):
    return get_top(entity_set)


def target_random(entity_set):
    shuffle(entity_set)
    return get_top(entity_set)


def target_weakest(entity_set):
    entity_set.sort(key=lambda entity: entity.resilience)
    return get_top(entity_set)


def target_strongest(entity_set):
    entity_set.sort(key=lambda entity: entity.resilience, reverse=True)
    return get_top(entity_set)


def target_next_active(entity_set):
    entity_set.sort(key=lambda entity: entity.turnmeter, reverse=True)
    return get_top(entity_set)
