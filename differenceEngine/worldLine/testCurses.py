import curses
from curses import wrapper
import numpy as np
import urllib.request
import socket


def get_ipv6():
    ip = urllib.request.urlopen("https://ident.me").read().decode("utf8")
    with open("myCurrentIpv6.out", "w") as file:
        file.write(f"{ip}")
    return f"{ip}"


coord = [2, 3]
mapp = {
    "menu": {
        (2, 3): {0: "hellow", 2: "hellow"},
        (3, 3): {0: "menu", 2: "menu"},
        (4, 3): {0: "get_current_ipv6", 2: "get_current_ipv6"},
    },
    "hellow": {(2, 3): {0: "menu", 2: "menu"}},
    "start": {(2, 3): {0: "start", 2: "start"}, (3, 3): {0: "menu", 2: "menu"}},
    "get_current_ipv6": {
        (2, 3): {0: "menu", 2: "menu"},
        (3, 3): {2: "press to get", 1: get_ipv6},
    },
}


def main(stdscr):  # curses._CursesWindow):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_color(3, 255, 0, 0)
    a = 0
    height, width = stdscr.getmaxyx()
    map = mapp["start"]
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"{a},{coord[0]},{coord[1]},press ese to quit")
        for x, y in map:
            stdscr.addstr(x, y, f"{map[(x,y)][2]}")
            # if 1 in map[(x, y)]:
            #     map[(x, y)][1]()
        if (coord[0], coord[1] + 1) in map:
            stdscr.addstr(coord[0], coord[1], "*", curses.color_pair(1))
        else:
            stdscr.addstr(coord[0], coord[1], "*")
        stdscr.refresh()
        a = stdscr.getch()
        if a == 27:
            break
        if a == 258:
            coord[0] += 1
            coord[0] %= height
        if a == 259:
            coord[0] -= 1
            coord[0] %= height
        if a == 260:
            coord[1] -= 1
            coord[1] %= width
        if a == 261:
            coord[1] += 1
            coord[1] %= width
        if a == 10 and (coord[0], coord[1] + 1) in map:
            if 1 in map[(coord[0], coord[1] + 1)]:
                map[(coord[0], coord[1] + 1)][2] = map[(coord[0], coord[1] + 1)][1]()
            elif 0 in map[(coord[0], coord[1] + 1)]:
                map = mapp[map[(coord[0], coord[1] + 1)][0]]


wrapper(main)
