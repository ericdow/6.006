import rubik

def common_node(frontier_s, frontier_e):
    """ Return true if frontiers contain any common nodes """
    if len(frontier_s) < len(frontier_e):
        for n in frontier_s:
            if n in frontier_e:
                return n
    else:
        for n in frontier_e:
            if n in frontier_s:
                return n

    return None

def shortest_path(start, end):
    """
    Using 2-way BFS, finds the shortest path from start_position to
    end_position. Returns a list of moves. 

    You can use the rubik.quarter_twists move set.
    Each move can be applied using rubik.perm_spply
    """

    frontier_s = {start}
    frontier_e = {end}
    
    level_s = {start : 0}
    level_e = {end : 0}
    
    parent_s = {start : None}
    parent_e = {end : None}

    i_s = 1
    i_e = 1

    cn = common_node(frontier_s, frontier_e)

    while frontier_s and frontier_e and not cn:
        # Do a step of BFS from the start side
        next_s = set()
        for u in frontier_s:
            for move in rubik.quarter_twists:
                v = rubik.perm_apply(move, u)
                if v not in level_s:
                    level_s[v] = i_s
                    parent_s[v] = u
                    next_s.add(v)
        frontier_s = next_s
        i_s += 1

        # Check for a common node in the frontier
        cn = common_node(frontier_s, frontier_e)
        if cn:
            break
        
        # Do a step of BFS from the end side
        next_e = set()
        for u in frontier_e:
            for move in rubik.quarter_twists:
                v = rubik.perm_apply(move, u)
                if v not in level_e:
                    level_e[v] = i_e
                    parent_e[v] = u
                    next_e.add(v)
        frontier_e = next_e
        i_e += 1

        # Search should finish before 14 moves
        if (i_s + i_e > 16):
            return None

        # Check for a common node in the frontier
        cn = common_node(frontier_s, frontier_e)

    # Trace back to start and end by following parent pointers
    moves = []
    if cn:
        p = cn
        while p != start:
            c = p
            p = parent_s[c]
            for move in rubik.quarter_twists:
                if rubik.perm_apply(move, p) == c:
                    moves.append(move)
        
        moves.reverse()

        p = cn
        while p != end:
            c = p
            p = parent_e[c]
            for move in rubik.quarter_twists:
                if rubik.perm_apply(move, c) == p:
                    moves.append(move)

    return moves
