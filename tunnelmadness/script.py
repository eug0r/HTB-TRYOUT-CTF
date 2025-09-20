import sys
import time
import struct
from pwn import ELF, process, context

context.log_level = 'debug'

OFFSET = 12
COEFF = 16
MAZE_BYTE_SIZE = 0x1f400
READ_DWORD = 4
MAX_RETRIES = 1000

FORWARD_CMDS = ['U', 'F', 'R']
BACKWARD_CMDS = ['D', 'B', 'L']
MULTIPLIERS = [1, 20, 400]

# maze is a 8000 block array of 16 byte blocks. the value used for our navigation
# is stored at +0xc offset of each block, if the value is 1, we can move to the
# direction of that block, if it is 2 we can't, and if it is 3 we've won.
# the directions we can take: R/L F/B U/D are respectively equivalent to adding
# +/-400, +/-20, +/-1 to our current memory position. These multipliers along with the fact
# that the total number of moves to each direction R/F/U caps at 20, means maze can be
# thought of a 3d coordinate system, a 20*20*20 block. But actually we don't bother
# with that here:
# we will be reading maze entries looking for 1's in all 6 direction, except the one that would
# undo our step. Everytime we hit a total dead-end we will mark the current address as "burnt"
# And restart from the beginning, not taking burnt paths. This will eventually account for branches
# And find a path that gets to the goal
# Would it be more efficient to keep track of visited nodes to backtrack and make it a proper DFS? yes
# yeah

def find_maze_address(elf: ELF, proc):

    sym_offset = elf.symbols['maze']
    base = 0
    libs = proc.libs()
    if elf.path in libs:
        base = libs[elf.path]
    else:
        for k, v in libs.items():
            if k.endswith(elf.path) or elf.path.endswith(k):
                base = v
                break
    return base + sym_offset

def read_dword_from_pid(pid, addr):
    mem_path = f"/proc/{pid}/mem"
    with open(mem_path, 'rb') as mem:
        mem.seek(addr)
        data = mem.read(READ_DWORD)
        return struct.unpack('<i', data)[0]

def maze_runner(binary_path, burnt_addrs):
    retry_count = 0

    while retry_count < MAX_RETRIES:
        retry_count += 1
        print(f"\n\n\n===== attempt {retry_count} =======")

        elf = ELF(binary_path)
        p = process(binary_path)
        time.sleep(0.05)

        maze_addr = find_maze_address(elf, p)

        current_position = maze_addr
        maze_end = current_position + MAZE_BYTE_SIZE

        moves = []
        iteration = 0
        last_forward_mult = 0
        last_backward_mult = 0

        try:
            while True:
                iteration += 1
                did_move = False
                last_val = None

                # forward check
                forward_hits = []
                for mult, cmd in zip(MULTIPLIERS, FORWARD_CMDS):
                    if mult == last_backward_mult:
                        continue
                    addr = current_position + COEFF * mult + OFFSET
                    if not (maze_addr <= addr <= maze_end - READ_DWORD):
                        continue
                    if addr in burnt_addrs:
                        continue

                    val = read_dword_from_pid(p.pid, addr)

                    print(f"[iter {iteration}] forward, mult={mult} addr={hex(addr)} val={val}")
                    if val == 3:
                        print("flag found (value == 3)")
                        last_val = 3
                        did_move = True
                        break
                    if val == 1:
                        forward_hits.append((mult, cmd, addr))

                if last_val == 3:
                    moves.append(cmd)
                    p.close()
                    return moves

                # pick a hit not already taken (burnt)
                if forward_hits:
                    for mult, cmd, addr in forward_hits:
                        if addr not in burnt_addrs:
                            print(f"forward move '{cmd}' {hex(addr)}")
                            p.sendline(cmd.encode())
                            moves.append(cmd)
                            current_position = addr - OFFSET
                            maze_end = current_position + MAZE_BYTE_SIZE
                            did_move = True
                            last_forward_mult = mult
                            last_backward_mult = 0
                            break
                    if not did_move and forward_hits:
                        break

                # backward check
                if not did_move:
                    backward_hits = []
                    for mult, cmd in zip(MULTIPLIERS, BACKWARD_CMDS):
                        if mult == last_forward_mult:
                            continue
                        addr = current_position - COEFF * mult + OFFSET
                        if not (maze_addr <= addr <= maze_end - READ_DWORD):
                            continue
                        if addr in burnt_addrs:
                            continue
                        try:
                            val = read_dword_from_pid(p.pid, addr)
                        except Exception:
                            continue
                        print(f"[iter {iteration}] backward, mult={mult} addr={hex(addr)} val={val}")
                        if val == 3:
                            print("flag found (value == 3)")
                            last_val = 3
                            did_move = True
                            break
                        if val == 1:
                            backward_hits.append((mult, cmd, addr))

                    if last_val == 3:
                        moves.append(cmd)
                        p.close()
                        return moves

                    # burnt check for backward moves
                    if backward_hits:
                        for mult, cmd, addr in backward_hits:
                            if addr not in burnt_addrs:
                                print(f"backward move '{cmd}' {hex(addr)}")
                                p.sendline(cmd.encode())
                                moves.append(cmd)
                                current_position = addr - OFFSET
                                maze_end = current_position + MAZE_BYTE_SIZE
                                did_move = True
                                last_backward_mult = mult
                                last_forward_mult = 0
                                break
                        if not did_move and backward_hits:
                            break
                # deadend
                if not did_move:
                    print(f"*******dead end at {hex(current_position)}; marking burnt")
                    burnt_addrs.add(current_position)
                    break
        finally:
            try:
                p.close()
            except Exception:
                pass

    print("maximum retries reached, aborting")
    return moves

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python3 script.py [path-to-binary]")
        sys.exit(1)

    burnt_addrs = set()
    moves = maze_runner(sys.argv[1], burnt_addrs)
    print("\nMoves taken")
    print("".join(moves))
    print(moves)
