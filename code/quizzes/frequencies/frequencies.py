#!/usr/bin/env python3

"""Read a file containing frequencies and quiz user. File format must be singe
white space separated entries.

Usage: frequencies.py data-dir

Parameters ---------- :data-dir: path to a directory containing two files:
  - frequencies: this file contains the actual frequencies that the user will be
    quizzed on
  - gamestate: a file describing the game state
  - pot: a file containing the size of the pot
"""

from sys import argv, exit
from random import shuffle
import csv
from os import path as osp
from argparse import ArgumentParser

parser = ArgumentParser(description='Quiz on solver-generated frequencies')
parser.add_argument('directory', help='root of a solver dataset. must contain files "frequencies", "gamestate", and "pot"')
parser.add_argument('--num-questions', '-n', type=int, default=10, help='number of questions to quiz the user on (0 for all)')
parser.add_argument('--equity-window', type=float, default=2.5)
parser.add_argument('--ev-window', type=float, default=5.00)
parser.add_argument('--frequency-window', type=float, default=7.5)
parser.add_argument('--repeat-missed', action='store_true')
parser.add_argument('--ignore-field', '-i', action='append', help='ignore fields in quiz')

args = parser.parse_args()

EQUITY_WINDOW = args.equity_window        # Percentage of error we allow (this is additive)
EV_WINDOW = args.ev_window                # EV error we allow (multiplicative)
FREQUENCY_WINDOW = args.frequency_window  # Action frequency error we all (this is additive)
NUM_QUESTIONS = args.num_questions
REPEAT_MISSED = args.repeat_missed
IGNORED_FIELDS = [f.lower() for f in (args.ignore_field or [])]

def get_float_input(prompt):
    while True:
        try:
            guess = input("    \033[1;32m{:<12}\033[0m".format(prompt + '>')).strip()
            return float(guess)
        except ValueError as e:
            print("Couldn't parse input {}, try again!".format(guess))

ROOT = args.directory
FREQUENCIES_PATH = osp.join(argv[1], 'frequencies')
GAMESTATE_PATH = osp.join(argv[1], 'gamestate')
POT_PATH = osp.join(argv[1], 'pot')

if not (osp.exists(FREQUENCIES_PATH) and osp.exists(GAMESTATE_PATH) and osp.exists(POT_PATH)):
    print("Cannot locate needed files", FREQUENCIES_PATH, "and", GAMESTATE_PATH)
    print("Exiting")
    exit(1)

with open(GAMESTATE_PATH) as f:
    gamestate = f.read()
with open(FREQUENCIES_PATH) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
    lines = list(reader)
    fieldnames = reader.fieldnames
with open(POT_PATH) as f:
    pot = f.read().strip()
    try:
        pot = float(pot)
    except ValueError as e:
        print("Couldn't read pot value", pot)
        print("Exiting")
        exit(1)
    EV_WINDOW *= 0.01
    EV_WINDOW *= pot

todo = list(lines)
shuffle(todo)
NUM_QUESTIONS = min(NUM_QUESTIONS, len(todo))
if NUM_QUESTIONS > 0:
    todo = todo[:NUM_QUESTIONS]

print("\033[1m")
print("----------------------------------------")
print(gamestate)
print('pot:', pot)
print("----------------------------------------")
print("\033[0m")

total_asked = 0
total_right = 0
distances = {}

for fieldname in fieldnames:
    if fieldname.lower() not in IGNORED_FIELDS:
        distances[fieldname] = []

while todo:
    question = todo.pop()
    hand = question[fieldnames[0]]
    print("[[[\033[1;96m" + hand + "\033[0m]]]", "| pot:", pot, "| ({} left)".format(len(todo) + 1))
    found_wrong = False
    temp_answers = {}
    for i, item in enumerate(reader.fieldnames[1:]):
        if item.lower() in IGNORED_FIELDS: continue
        try:
            answer = float(question[item])
        except ValueError as e:
            print("Couldn't read entry {} from file: expected float. Continuing".format(question[item]))
            continue
        guess = get_float_input(item)
        dist = answer - guess
        dist_sq = dist * dist
        temp_answers[item] = (guess, answer, dist_sq)
        distances[item].append(dist_sq)
        total_asked += 1

    print("Reviewing Answers for [[[\033[1;96m" + hand + "\033[0m]]]")
    for i, item in enumerate(reader.fieldnames[1:]):
        if item.lower() in IGNORED_FIELDS: continue
        guess, answer, dist_sq = temp_answers[item]
        print("    \033[1;32m{:<12}\033[0m".format(item + '>'), end='')
        # We want to create a window of acceptable answers. Default values are
        if i == 0:
            lower, upper = answer - EQUITY_WINDOW, answer + EQUITY_WINDOW
            lower = round(max(0, lower))
            upper = round(min(100, upper))
        elif i == 1:
            lower, upper = answer - EV_WINDOW, answer + EV_WINDOW
            lower = round(max(0, lower),2)
            upper = round(min(pot, upper), 2)
        else:
            lower, upper = answer - FREQUENCY_WINDOW, answer + FREQUENCY_WINDOW
            lower = round(max(0, lower))
            upper = round(min(100, upper))
        if lower <= guess <= upper:
            print("Guess:", guess, " \033[1;32m[Correct  ]\033[0m  Answer:", answer, "| Window: {}".format([lower, upper]))
            total_right += 1
        else:
            print("Guess:", guess, " \033[1;91m[Incorrect]\033[0m  Answer:", answer, "| Window: {}".format([lower, upper]))
            found_wrong = True
    if found_wrong and REPEAT_MISSED:
        todo.insert(0, question)

print("\033[34;1mSummary\n=======\033[0m")
print("Asked", NUM_QUESTIONS, "questions with", total_asked, "subquestions")
print("Answered", total_right, "subquestions correctly {}".format(100 * total_right / total_asked))

print("Average distances")
for fieldname in fieldnames:
    if fieldname.lower() == 'hand': continue
    if fieldname.lower() in IGNORED_FIELDS: continue

    dists = distances[fieldname]
    avg_dist = sum(dists)**0.5 / len(dists)
    if fieldname.lower() == 'ev':
        avg_dist = 100 * avg_dist / pot
    print('\033[33;1m{}:\033[0m {}%'.format(fieldname, round(avg_dist, 1)))
