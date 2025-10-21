import sys
import heapq

from functools import lru_cache

def solve(lines: list[str]) -> int:
    room_depth = len(lines) - 3
    rooms = []
    room_positions = [2, 4, 6, 8]
    
    for i in range(4):
        room = []
        for depth in range(room_depth):
            char = lines[2 + depth][room_positions[i] + 1]
            room.append(char)
        rooms.append(tuple(room))

    target_rooms = (
        tuple(['A'] * room_depth),
        tuple(['B'] * room_depth),
        tuple(['C'] * room_depth),
        tuple(['D'] * room_depth)
    )
    
    costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    
    valid_corridor_positions = [0, 1, 3, 5, 7, 9, 10]
    
    @lru_cache(maxsize=None)
    def can_move_to_room(amphipod_type, room):
        if room == target_room_index(amphipod_type):
            for cell in room:
                if cell != '.' and cell != amphipod_type:
                    return False
            return True
        return False
    
    def target_room_index(amphipod_type):
        """Возвращает индекс целевой комнаты"""
        return ord(amphipod_type) - ord('A')
    
    def is_room_organized(room, room_index):
        """Проверяет, организована ли комната"""
        target_type = chr(ord('A') + room_index)
        for cell in room:
            if cell != '.' and cell != target_type:
                return False
        return True
    
    def get_room_position(room_index):
        """Возвращает позицю в коридоре для комнаты"""
        return room_positions[room_index]
    
    def is_path_clear(corridor, start, end):
        """Проверяет, свободен ли путь в коридоре"""
        step = 1 if start < end else -1
        for pos in range(start + step, end + step, step):
            if corridor[pos] != '.':
                return False
        return True
    
    def room_can_accept(room, amphipod_type):
        """Проверяет, может ли комната принять амфипод"""
        target_idx = target_room_index(amphipod_type)
        for cell in room:
            if cell != '.' and cell != amphipod_type:
                return False
        return True
    
    def get_target_depth(room):
        """Находит максимальную глубину, на которую можно поместить амфипод в комнату"""
        for depth in range(len(room) - 1, -1, -1):
            if room[depth] == '.':
                return depth
        return -1
    
    def dijkstra():
        start_state = (0, tuple('.' * 11), tuple(rooms))
        heap = [start_state]
        visited = set()
        
        while heap:
            energy, corridor, current_rooms = heapq.heappop(heap)
            if current_rooms == target_rooms:
                return energy
            
            state_key = (corridor, current_rooms)
            if state_key in visited:
                continue
            visited.add(state_key)
            for corridor_pos in range(11):
                if corridor[corridor_pos] == '.':
                    continue
                
                amphipod = corridor[corridor_pos]
                target_room_idx = target_room_index(amphipod)
                target_room = current_rooms[target_room_idx]
                if not room_can_accept(target_room, amphipod):
                    continue
                
                room_pos = get_room_position(target_room_idx)
                if not is_path_clear(corridor, corridor_pos, room_pos):
                    continue
                
                target_depth = get_target_depth(target_room)
                if target_depth == -1:
                    continue
                steps = abs(corridor_pos - room_pos) + (target_depth + 1)
                move_cost = steps * costs[amphipod]

                new_corridor = list(corridor)
                new_corridor[corridor_pos] = '.'
                
                new_room = list(target_room)
                new_room[target_depth] = amphipod
                new_rooms = list(current_rooms)
                new_rooms[target_room_idx] = tuple(new_room)
                
                new_state = (energy + move_cost, tuple(new_corridor), tuple(new_rooms))
                heapq.heappush(heap, new_state)
            
            for room_idx in range(4):
                room = current_rooms[room_idx]

                if is_room_organized(room, room_idx):
                    continue

                top_amphipod_depth = -1
                for depth in range(room_depth):
                    if room[depth] != '.':
                        top_amphipod_depth = depth
                        break
                
                if top_amphipod_depth == -1:
                    continue
                
                amphipod = room[top_amphipod_depth]
                room_pos = get_room_position(room_idx)

                for corridor_pos in valid_corridor_positions:
                    if not is_path_clear(corridor, room_pos, corridor_pos):
                        continue

                    steps = (top_amphipod_depth + 1) + abs(room_pos - corridor_pos)
                    move_cost = steps * costs[amphipod]

                    new_corridor = list(corridor)
                    new_corridor[corridor_pos] = amphipod
                    
                    new_room = list(room)
                    new_room[top_amphipod_depth] = '.'
                    new_rooms = list(current_rooms)
                    new_rooms[room_idx] = tuple(new_room)
                    
                    new_state = (energy + move_cost, tuple(new_corridor), tuple(new_rooms))
                    heapq.heappush(heap, new_state)
        
        return -1
    
    return dijkstra()

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    result = solve(lines)
    print(result)

if __name__ == "__main__":
    main()