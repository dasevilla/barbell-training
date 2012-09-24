from collections import defaultdict
from pprint import pprint
import itertools

from jinja2 import Environment, FileSystemLoader


class Exercise(object):

    def __init__(self, name, max_weight, increment_size=10, warm_up_sets=3,
                 bar_weight=45, work_sets=3, work_reps=5):
        self.name = name
        self.bar_weight = bar_weight
        self.max_weight = max_weight
        self.increment_size = increment_size
        self.warm_up_sets = warm_up_sets
        self.work_sets = work_sets
        self.work_reps = work_reps

    def round_weight(self, weight, base=5):
        """Round a weight to a certain plate increment"""
        return int(base * round(float(weight)/base))

    def get_sets(self):
        """Returns a list of (weight, reps, sets)"""

        end_weight = self.max_weight
        start_weight = self.bar_weight
        warm_up_steps = self.warm_up_sets

        routine = []

        routine.append({
            'weight': start_weight,
            'weight_side': 0.0,
            'reps': 5,
            'sets': 2,
        })

        set_list = [
            # sets, reps, weight_multi
            # (1, 5, 0.4),
            (1, 4, 0.7),
            (1, 3, 0.9),
            (3, 5, 1.0),
        ]

        for sets, reps, weight_multiplier in set_list:
            weight = self.round_weight(end_weight * weight_multiplier)
            routine.append({
                'weight': weight,
                'weight_side': (weight - start_weight) / 2.0,
                'reps': reps,
                'sets': sets,
            })

        return routine

    def increment(self):
        self.max_weight += self.increment_size


def render(week_list):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('strength.tex')
    print template.render(week_list=week_list)


def pretty_print(week_list):
    for week_num, week in enumerate(week_list):
        for day_num, (routine, exercises) in enumerate(week):
            print 'Week %0d Day %0d Routine %s' % (week_num+1, day_num+1,
                routine)
            for name, sets in exercises:
                print name
                for program in sets:
                    print '%03d\t%d\t%d' % (program['weight'], program['reps'],
                        program['sets'])
            print
        print
    print


def main():
    weeks = 2
    sessions_per_week = 3

    squat = Exercise('Squat', 165, increment_size=10)
    press = Exercise('Press', 90, increment_size=5)
    bench_press = Exercise('Bench Press', 105, increment_size=5)
    dead_lift = Exercise('Dead Lift', 195, bar_weight=135, increment_size=15,
        work_sets=1)  # Only one set

    routines = [
        ("A", (squat, press, dead_lift)),
        ("B", (squat, bench_press, dead_lift)),
    ]

    routine_iter = itertools.cycle(routines)

    week_list = []
    for week_num in range(weeks):

        day_list = []
        for day_num in range(sessions_per_week):
            routine, exercises = routine_iter.next()

            exercise_list = []
            for exercise in exercises:
                exercise_list.append((exercise.name, exercise.get_sets()))
                exercise.increment()

            day_list.append((routine, exercise_list))

        week_list.append(day_list)

    # pretty_print(week_list)
    render(week_list)


if __name__ == '__main__':
    main()
