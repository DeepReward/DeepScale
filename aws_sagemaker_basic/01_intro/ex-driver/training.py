# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except
# in compliance with the License. A copy of the License is located at
#
# https://aws.amazon.com/apache-2-0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
import sys
import csv
from curses import wrapper, use_default_colors, napms, curs_set

road_centers = [0,2,3,3,2,0,-2,-3,-3,-2];
training_csv = []
car_pos = 0

def draw_road(screen):
    road_csv = []

    # needed to clear the terminal on Cloud9
    for i in range(len(road_centers)):
        screen.addstr(i+1, 1, "." * 25)
    screen.refresh()

    for i in range(len(road_centers)):
        road_center = road_centers[i]
        road_left = road_center-3;
        road_right = road_centers[i] + 3;
        line = ''
        for j in range(car_pos-12, car_pos+13):
            paint = '░'
            if j==road_left or j==road_right: paint = '█'
            if j > road_left and j < road_right: paint = '▒';
            line += paint
        road_csv.extend(list(line.replace("░","0").replace("█","1").replace("▒","2")))
        screen.addstr(i+1, 1, line)
    # draw the car
    screen.addstr(len(road_centers), 13, "▀")
    screen.refresh()
    return road_csv

def main(stdscr):
    global car_pos
    use_default_colors()
    stdscr.border()
    curs_set(0)
    stdscr.addstr(1, 1, "Press any key to start..")
    stdscr.getch()

    stdscr.nodelay(True)
    for i in range(150):
        label = "1" # straight
        road_csv = draw_road(stdscr)
        napms(300)
        # read everything off the buffer
        # only interested in the last non -1 character
        ch = 0
        while True:
            key = stdscr.getch()
            if key==-1: break
            else: ch = key

        if ch == 260: # left
            car_pos-=1
            label = "0"
        if ch == 261: # right
            car_pos+=1
            label = "2"

        road_csv.insert(0, label)
        training_csv.append(road_csv)
        pop = road_centers.pop()
        road_centers.insert(0, pop)


    stdscr.nodelay(False)
    stdscr.addstr(12, 1, "Press any key to quit")
    stdscr.getkey()


if __name__ == "__main__":
    from curses import wrapper
    wrapper(main)

    with open('training.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in training_csv:
            writer.writerow(row)
