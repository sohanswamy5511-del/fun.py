import random

# ============================================================
# EVENT TYPES
# ============================================================

LUCK = "LUCK"
EXTRA_SPIN = "EXTRA_SPIN"
WEIGHT_ACTIVE = "WEIGHT_ACTIVE"

ADD_SYMBOL_MULT = "ADD_SYMBOL_MULT"
ADD_PATTERN_MULT = "ADD_PATTERN_MULT"

ADD_REPETITION = "ADD_REPETITION"
ADD_CHAIN = "ADD_CHAIN"
ADD_RECHARGE_TARGET = "ADD_RECHARGE_TARGET"


# ============================================================
# EVENT BUS
# ============================================================

class EventBus:
    def __init__(self):
        self.handlers = {}

    def register(self, event_type, handler):
        self.handlers.setdefault(event_type, []).append(handler)

    def emit(self, event_type, event, game_state, context=None):

        if event_type not in self.handlers:
            print(f"⚠ No handler for event: {event_type}")
            return

        for handler in self.handlers[event_type]:
            handler(event, game_state, context)


# ============================================================
# RESOLVER
# ============================================================

class CharmResolver:

    def resolve(self, charm):

        events = []

        for effect in charm.effects:

            if effect.chance is not None:
                if random.randint(1, 100) > effect.chance:
                    continue

            events.append(effect)

        return events


# ============================================================
# EVENT HANDLERS
# ============================================================

def handle_luck(event, game_state, context):
    game_state['pending_luck'] += event.amount
    print(f"  ✓ +{event.amount} luck")


def handle_extra_spin(event, game_state, context):
    game_state['spins_left'] += event.amount
    print(f"  ✓ +{event.amount} spins")


def handle_symbol_mult(event, game_state, context):
    game_state['symbols_mult'] += event.amount
    print(f"  ✓ symbols mult +{event.amount}")


def handle_pattern_mult(event, game_state, context):
    game_state['patterns_mult'] += event.amount
    print(f"  ✓ patterns mult +{event.amount}")


def handle_repetition(event, game_state, context):
    game_state['repetition_targets'].append(event.target)
    print("  ✓ repetition modifier added")


def handle_chain(event, game_state, context):
    game_state['chain_targets'].append(event.target)
    print("  ✓ chain modifier added")


def handle_recharge(event, game_state, context):
    game_state['recharge_targets'].append(event.target)
    print("  ✓ recharge modifier added")


def handle_weight_active(event, game_state, context):

    charm_data = context
    target_cls = event.target
    bonuses = game_state['active_bonuses']

    increase = calculate_weight_increase(target_cls)

    if charm_data['activations_this_round'] == 0:

        bonuses[target_cls] = (
            bonuses.get(target_cls, getattr(target_cls, "weight", 1))
            + increase
        )

        charm_data['last_increase'] = increase

    else:

        increase = charm_data['last_increase'] * 0.9
        bonuses[target_cls] += increase
        charm_data['last_increase'] = increase

    print(f"  ✓ {target_cls.__name__} weight +{increase:.1f}")


# ============================================================
# BUILD EVENT BUS
# ============================================================

event_bus = EventBus()

event_bus.register(LUCK, handle_luck)
event_bus.register(EXTRA_SPIN, handle_extra_spin)

event_bus.register(ADD_SYMBOL_MULT, handle_symbol_mult)
event_bus.register(ADD_PATTERN_MULT, handle_pattern_mult)

event_bus.register(ADD_REPETITION, handle_repetition)
event_bus.register(ADD_CHAIN, handle_chain)
event_bus.register(ADD_RECHARGE_TARGET, handle_recharge)

event_bus.register(WEIGHT_ACTIVE, handle_weight_active)


# ============================================================
# CHARM ACTIVATION SYSTEM
# ============================================================

def activate_charms(owned_charms, game_state, resolver, event_bus):

    available = [
        d for d in owned_charms
        if d['cooldown'] == 0
        and d['charm'].cooldown_rounds > 0
    ]

    if not available:
        print("No cooldown charms available.")
        return

    print("\n🎯 Activating ALL available charms...\n")

    for d in available:

        charm = d['charm']
        print(f"✓ {charm.name} activated!")

        events = resolver.resolve(charm)

        for event in events:

            event_bus.emit(
                event.type,
                event,
                game_state,
                context=d
            )

        d['uses'] += 1
        d['activations_this_round'] += 1
        d['cooldown'] = charm.cooldown_rounds


# ============================================================
# HELPERS
# ============================================================

def has_available_cooldown_charms(owned_charms):

    return any(
        d['cooldown'] == 0
        and d['charm'].cooldown_rounds > 0
        for d in owned_charms
    )