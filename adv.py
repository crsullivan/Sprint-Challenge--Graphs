from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}
visited[player.current_room] = player.current_room.get_exits()
print('starting room exits:', visited.get(player.current_room))
print("Nearby:", room_graph[0][1])

def bfs(starting_vertex, destination_vertex):
    qq = Queue()
    qq.enqueue([starting_vertex])
    visit = set()
    while qq.size() > 0:
        path = qq.dequeue()
        last_vertex = path[-1]
        if last_vertex == destination_vertex:
                return path
        if last_vertex not in visit:
            visit.add(last_vertex)
            exits = room_graph[last_vertex][1]
            for direction in exits:
                qq.enqueue([*path, exits[direction]])

def dft(v):
    visit = []
    s = Stack()
    s.push(v.id)
    while s.size() > 0:
        v = s.pop()
        if v not in visit:
            visit.append(v)
            exits = room_graph[v][1]
            for direction in exits:
                if exits[direction] not in visit:
                    s.push(exits[direction])
    return visit

def dothething(player):
    path = dft(player.current_room)
    for i in range(len(path) - 1):
        location = player.current_room
        exits = location.get_exits()
        bfs_path = bfs(path[i], path[i+1])
        for i in range(len(bfs_path) - 1):
            room_exits = room_graph[bfs_path[i]][1]
            for direction in room_exits:
                if room_exits[direction] == bfs_path[i + 1]:
                    player.travel(direction)
                    traversal_path.append(direction)


# visit = []
# s = Stack()
# print('room:', player.current_room.id)
# s.push(player.current_room.id)
# while s.size() > 0:
#     v = s.pop()
#     if v not in visit:
#         print("V:", v)
#         visit.append(v)
#         exits = room_graph[v][1]
#         print(exits)
#         traversal_path.append(v)
#         if v not in visited_rooms:
#             visited_rooms.add(v)
#         print(visited_rooms, len(visited_rooms))
#         for direction in exits:
#             if exits[direction] not in visit:
#                 s.push(exits[direction])
# print('DFT Return:', visit)
# print(len(visited_rooms))
# print(len(room_graph))

# TRAVERSAL TEST`
dothething(player)
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

print("Traversal Length:", len(traversal_path))
print("Follow These Directions:", traversal_path)
#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
