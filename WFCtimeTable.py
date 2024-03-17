# import numpy as np
#
# n_sections = 3
# n_days_per_week = 5
# n_subjects_per_day = 9
# subjects: dict[str, int] = {"CC": 6, "CD": 6, "OOAD": 6, "CC_LAB": 2, "OOAD_LAB": 2,
#                             "F": 500, "G": 500, "H": 500, "I": 500, "J": 500, "K": 500}
# total_subjects = sum(subjects.values())
# timetable = np.zeros((n_sections, n_days_per_week, n_subjects_per_day), dtype='U10')
#
# # Initialize constraints for each cell
# cell_constraints = {
#     f'{sec}_{day}_{hour}':
#         list(subjects.keys())
#     for sec in range(n_sections) for day in range(n_days_per_week) for hour in range(n_subjects_per_day)
# }
#
#
# # Define function to update constraints after placing a class
# def update_constraints(section, day, hour, cls):
#     # Update constraints for the same section
#     for h in range(n_subjects_per_day):
#         key = f'{section}_{day}_{h}'
#         if key in cell_constraints and cls in cell_constraints[key]:
#             cell_constraints[key].remove(cls)
#
#     # Update constraints for the same day
#     for s in range(n_sections):
#         key = f'{s}_{day}_{hour}'
#         if key in cell_constraints and cls in cell_constraints[key]:
#             cell_constraints[key].remove(cls)
#
#     # Update constraints for the same hour
#     for s in range(n_sections):
#         for d in range(n_days_per_week):
#             key = f'{s}_{d}_{hour}'
#             if key in cell_constraints and cls in cell_constraints[key]:
#                 cell_constraints[key].remove(cls)
#
#
# # Define function for wave function collapse
# def wave_function_collapse():
#     while len(cell_constraints) > 0:
#         # Choose cell with minimum entropy
#         min_entropy = float('inf')
#         min_cell = None
#         for cell, constraints in cell_constraints.items():
#             entropy = len(constraints)
#             if entropy < min_entropy:
#                 min_entropy = entropy
#                 min_cell = cell
#
#         # Choose a class randomly from remaining options
#         if len(cell_constraints[min_cell]) > 0:
#             selected_class = np.random.choice(cell_constraints[min_cell])
#             # print(selected_class, "+++")
#         else:
#             print("No valid classes to assign. Exiting...")
#             return
#
#         # Get section, day, and hour from the cell name
#         section, day, hour = map(int, min_cell.split('_'))
#
#         # Assign the class to the timetable
#         timetable[section, day, hour] = selected_class
#         print(timetable[section, day, hour], selected_class, "----")
#         # Update constraints
#         update_constraints(section, day, hour, selected_class)
#
#         # Remove cell from constraints
#         del cell_constraints[min_cell]
#
#
# # Generate timetable
# wave_function_collapse()
# print(timetable)
# # Print timetable
# for sec in range(n_sections):
#     print(f"Section {sec + 1}:")
#     for day in range(n_days_per_week):
#         print(f"Day {day + 1}:", end=" ")
#         for hour in range(n_subjects_per_day):
#             print(f"{timetable[sec, day, hour]}", end=" ")
#         print()
#     # print()
from typing import Iterable

# blocked = [
#     [
#         [0, 0, 0, 1, 1, 1, 0, 0, 0],
#         [0, 0, 0, 1, 1, 1, 0, 0, 0],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ],
#     [
#         [0, 0, 0, 1, 1, 1, 0, 0, 0],
#         [0, 0, 0, 1, 1, 1, 0, 0, 0],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ],
#     [
#         [0, 0, 0, 1, 1, 1, 0, 0, 0],
#         [0, 0, 0, 1, 1, 1, 0, 0, 0],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 0, 0]
#     ]
# ]

import numpy as np
import colorama

n_sections = 3
n_days_per_week = 5
n_subjects_per_day = 9
subjects: dict[str, int] = {
    "CC": 6,  # CC
    "CD": 6,  # CD
    "OOAD": 6,  # OOAD
    "CC_LAB": 2,  # CCLAB
    "OOAD_LAB": 2,  # OOADLAB
    'elec-1': 3,
    'elec-2': 3,
    "-": 11
}

teachers: dict[str, int] = {
    "CC": 1,  # CC
    "CD": 1,  # CD
    "OOAD": 1,  # OOAD
    "CC_LAB": 1,  # CCLAB
    "OOAD_LAB": 1,  # OOADLAB
    'elec-1': n_sections,
    'elec-2': n_sections,
    "-": n_sections
}

total_subjects = sum(subjects.values())
listed_states = []


def ofst(n):
    return (60*n)**2


def get_ndx(ndx_tuple):
    sec, day, period = ndx_tuple
    return (sec * n_days_per_week + day) * n_subjects_per_day + period


def get_entropy(cls):
    return subjects[cls] * teachers[cls]


def get_min_cls(state):
    min_cls = None
    min_entropy = np.inf
    for cls in state.classes:
        if (cls_entropy := get_entropy(cls))<min_entropy:
            min_entropy = cls_entropy
            min_cls = cls
    return min_cls


def get_collapsable_state(tt:list['State']):
    mintropy = np.inf
    mindxtropy = None
    for sec in range(n_sections):
        for day in range(n_days_per_week):
            for period in range(n_subjects_per_day):
                ndx = get_ndx((sec, day, period))
                if not isinstance(tt[ndx], SuperState):
                    continue
                if tt[ndx].entropy <= mintropy:
                    mintropy = tt[ndx].entropy
                    mindxtropy = sec, day, period
    if mindxtropy is None:
        return None
    return {'state': tt[get_ndx(mindxtropy)], 'ndx': mindxtropy}
    # return min(tt, key=lambda x: x.entropy)

class State:
    def __init__(self, ) -> None:
        self.entropy = np.inf

    def __repr__(self):
        return f'State[{self.entropy}]'

    def __format__(self, format_spec):
        out: str = repr(self)
        if format_spec[0] in '_-':
            return out.center(int(format_spec[1:]))
        return f'{out:{format_spec}}'


class CollapsedState(State):
    def __init__(self, cls, pos):
        self.cls = cls
        self.pos = pos
        super().__init__()
        self.entropy = get_entropy(cls) + pos

    def __hash__(self):
        return hash(f'[{self.cls}]')

    def __repr__(self):
        # return str(self.ID)
        return f"{self.cls}"#f"{self.cls}=[{self.entropy}]"


class SuperState(State):
    ID = 0

    def __init__(self, classes: Iterable[str], pos) -> None:
        self.classes = set(classes)
        self.pos = pos
        super().__init__()
        self.clalc_entropy()
        self.ID = SuperState.ID
        SuperState.ID += 1

    def clalc_entropy(self) -> None:
        self.entropy = sum(get_entropy(cls) for cls in self.classes) + self.pos

    def __hash__(self):
        return hash('_'.join(self.classes))

    def __repr__(self):
        # return str(self.ID)
        return f"{''.join(self.classes)}_[{self.entropy}]"


def print_tt(tt):
    padding = 10#len(''.join(subjects.keys()))+len(str(MAX_ENTROPY))+3-3
    for sec in range(n_sections):
        print('SECTION', sec + 1)
        for day in range(n_days_per_week):
            print("day", day, end=':  ')
            for period in range(n_subjects_per_day):
                state = tt[get_ndx((sec, day, period))]
                clr = ('\033[39m', '\033[92m')[isinstance(state, CollapsedState)]
                print(f"{clr}{state:-{padding}}\033[39m", end=' ')
            print()


def print_tt_stats(tt):
    for s in range(n_sections):
        sec_cls = {}
        for d in range(n_days_per_week):
            for p in range(n_subjects_per_day):
                state = tt[get_ndx((s, d, p))]
                if not isinstance(state, CollapsedState):
                    continue
                sec_cls[state.cls] = sec_cls.get(state.cls, 0) + 1
        print(sec_cls)


def collapse_slot(slot, tt):
    min_cls = get_min_cls(slot['state'])
    print(min_cls)
    slot['state']: CollapsedState = CollapsedState(min_cls, ofst(slot['ndx'][2]))
    tt[get_ndx(slot['ndx'])] = slot['state']
    propagate_constraints(slot, tt)
    return get_collapsable_state(tt)


def propagate_constraints(slot, tt:list[State]):
    sec, day, period = slot['ndx']
    # subj hrs constraint
    count = 0
    for d in range(n_days_per_week):
        for p in range(n_subjects_per_day):
            state = tt[get_ndx((sec, d, p))]
            if not isinstance(state, CollapsedState):
                continue
            # is a CollapsedState
            if state.cls == slot['state'].cls:
                count += 1
    if count == subjects[slot['state'].cls]:
        for d in range(n_days_per_week):
            for p in range(n_subjects_per_day):
                state = tt[get_ndx((sec, d, p))]
                if not isinstance(state, SuperState):
                    continue
                # is a SuperState
                if slot['state'].cls in state.classes:
                    state.classes.remove(slot['state'].cls)
                    # if len(state.classes) == 1:

                    state.clalc_entropy()

    # teachers constraint
    count = 0
    for s in range(n_sections):
        state = tt[get_ndx((s, day, period))]
        if not isinstance(state, CollapsedState):
            continue
        # is a CollapsedState
        if state.cls == slot['state'].cls:
            count += 1
    if count == teachers[slot['state'].cls]:
        for s in range(n_sections):
            state = tt[get_ndx((s, day, period))]
            if not isinstance(state, SuperState):
                continue
            # is a SuperState
            if slot['state'].cls in state.classes:
                state.classes.remove(slot['state'].cls)
                state.clalc_entropy()


def main():
    elective1 = [
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    elective2 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # listed_states.append(
    #     SuperState(subjects.keys(), 0)
    # )
    timetable: list[State] = [
        CollapsedState('elec-1', ofst(k)) if elective1[j][k] else ( CollapsedState('elec-2', ofst(k)) if elective2[j][k] else SuperState((key for key in subjects.keys() if key not in ('elec-1','elec-2')), ofst(k)) )# listed_states[0]
        for i in range(n_sections)
        for j in range(n_days_per_week)
        for k in range(n_subjects_per_day)
    ]

    collapseable_slot = {'state': timetable[0], 'ndx': (0, 0, 0)}
    print(listed_states)

    # print_tt(timetable)
    # collapseable_slot = collapse_slot(collapseable_slot, timetable)
    # print_tt(timetable)
    # print(collapseable_slot, end=f"\n{'*'*100}1\n")

    i=0
    while True:
        if collapseable_slot is None:
            print("The Wave Function has Collapsed")
            print_tt_stats(timetable)
            return
        if len(collapseable_slot['state'].classes) == 0:
            print("IMPOSSIBLE STATE REACHED")
            print_tt_stats(timetable)
            return
        collapseable_slot = collapse_slot(collapseable_slot, timetable)
        print_tt(timetable)
        print(collapseable_slot, end=f"\n{'*' * 100}{i}\n")
        # if input("Enter:"):
        #     break


if __name__ == '__main__':
    MAX_ENTROPY = sum(get_entropy(cls) for cls in subjects.keys())
    main()

