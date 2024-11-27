def target_basic(entity_set):
    for target in entity_set:
        if target.resilience > 0:
            return target


def target_weakest(entity_set):
    entity_set.sort(key=lambda entity: entity.resilience)
    for target in entity_set:
        if target.resilience > 0:
            return target
    return None


def target_strongest(entity_set):
    entity_set.sort(key=lambda entity: entity.resilience, reverse=True)
    for target in entity_set:
        if target.resilience > 0:
            return target
    return None


def target_next_active(entity_set):
    entity_set.sort(key=lambda entity: entity.turnmeter, reverse=True)
    for target in entity_set:
        if target.resilience > 0:
            return target
    return None
