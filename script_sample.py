#!/usr/bin/env python3

import angr
import sys
import os

def solution(core_file, input_file):
    project = angr.Project(core_file, load_options={
        'main_opts': {
            'backend':'elfcore',
        },
    })
    def exit_func(state):
        print("exit")
        exit(0)
    length = os.path.getsize(input_file)
    #print(length)
    state = project.factory.blank_state(add_options=angr.options.modes['symbolic'], arch='x86_64')
    symbol_bytes = []
    for i in range(length):
        symbol_bytes.append(state.solver.BVS("simbol", 8))

    print(state.regs.rip)
    pointer = state.regs.rdi
    for i in range(length):
        state.mem[pointer + i].byte = symbol_bytes[i]

    return_addr = state.mem[state.regs.rsp].uint64_t.concrete
    state.inspect.b('instruction', instruction=return_addr, action= exit_func)
    project.hook(0x7ffff7fd8d9c, exit_func)
    symbols = []
    with open(input_file, "rb") as f:
        a = f.read()
    print(a)
    print(len(a))
    with open(input_file, "rb") as f:
        for i in range(length):
            symbols.append(f.read(1))
    #print(symbols)
    constraints = []
    for i in range(length):
        constraints.append(symbols[i] == symbol_bytes[i])

    #print(constraints)

    while True:
        succ = state.step()
        if len(succ.successors) == 1:
            state = succ.successors[0]
        elif len(succ.successors) == 2:
            print("Here!")

            state1, state2 = succ.successors
            if state1.solver.satisfiable(extra_constraints=constraints):
                state = state1
                state_other = state2
                print("first")
            else:
                state = state2
                state_other = state1
                print("second")
            print("I'm here")
            for i in range(4):
                print(state.solver.eval(symbol_bytes[i], cast_to=bytes))
            print("all")
        else:
            break

if __name__ == "__main__":
    exec_name = sys.argv[1]
    file_path = sys.argv[2]
    solution(exec_name, file_path)