from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "/Users/david/Desktop/cs/Graphs/projects/adventure/maps/test_line.txt"
map_file = "/Users/david/Desktop/cs/Graphs/projects/adventure/maps/test_cross.txt"
map_file = "/Users/david/Desktop/cs/Graphs/projects/adventure/maps/test_loop.txt"
map_file = "/Users/david/Desktop/cs/Graphs/projects/adventure/maps/test_loop_fork.txt"
map_file = "/Users/david/Desktop/cs/Graphs/projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


opposite_directions = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}


class Path:

    def recursive_traverse(self, room, visited=None):

        # first we check if no rooms have been visited,
        # then we create a set to store visited room ids
        if visited is None:
            visited = set()

        # after that we create an empty list to store the path already taken
        path_taken = []

        # after that we add current room id to visited
        visited.add(room.id)

        # we then loop thru each room exit for current room
        for room_exit in room.get_exits():

            # then we set pointer for next room in direction of room exit
            next_room = room.get_room_in_direction(room_exit)

            # if the room is yet to be visited
            if next_room.id not in visited:

                # we use recursion to visit the other rooms
                unvisited = self.recursive_traverse(next_room, visited)

                # then if there are rooms left to traverse/visit
                if unvisited:

                    # we update the path using exit and walking direction information
                    current_path = [room_exit] + \
                        unvisited + \
                                   [opposite_directions[room_exit]]

                # then if there are no rooms left to visit/traverse
                else:

                    # we then backtrack where necessary
                    current_path = [
                        room_exit,
                        opposite_directions[room_exit]
                    ]

                # and update the taken path with current path's information
                path_taken = path_taken + \
                    current_path

        # and at the end return final path taken
        return path_taken


# Traversal of the rooms
traversal_path = Path().recursive_traverse(player.current_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


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
