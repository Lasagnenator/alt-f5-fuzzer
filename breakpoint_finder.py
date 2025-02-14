#!/usr/bin/env python3
import re
import subprocess

instructions = ['jbe', 'jnbe', 'jz', 'jpe', 'jne', 'jp', 'jb', 'jae', 'je',
                'jrcxz', 'jnae', 'jnb', 'jo', 'jcxz', 'ja', 'jna', 'jns', 'jnc', 
                'jng', 'jnge', 'js', 'jnl', 'jno', 'jg', 'jnle', 'jpo', 'jl', 
                'jnp', 'jecxz', 'jc', 'jle', 'jge', 'jnz']

def get_disassembly(program):
    # get addresses that are jumped to
    subprocess.Popen(f'objdump -d {program} > /tmp/disass', shell=True).communicate()

    with open('/tmp/disass2', 'w') as disass:
        with open('/tmp/disass', 'r') as f:
            for line in f:
                if re.match(r'.*:.*j[a-z ].*<.*>', line):
                    # only get specific jump instructions
                    if any(instruction in line for instruction in instructions):
                        disass.write(line)

def get(program):
    jmp_addr = []
    breakpoints = []

    get_disassembly(program)

    subprocess.Popen("cut -f1,3,4 /tmp/disass2 | cut -d'<' -f1 > /tmp/disass3", shell=True).communicate()

    # add addresses that are being jumped to to the breakpoints list
    # add the address of the jmp instruction to the jmp_addr list
    with open('/tmp/disass3', 'r') as f:
        for line in f:
            jmp_addr.append(line.split(':')[0])

            info = re.split(r'j[a-z ]+', line)
            breakpoints.append(info[1].strip())

    # add each subsequent instruction after each address in the jmp_addr list
    f = open('/tmp/disass', 'r')
    lines = f.readlines()
    for i, line in enumerate(lines):
        if any(line.startswith(addr) for addr in jmp_addr) and (i + 1) < len(lines):
            breakpoints.append(lines[i + 1].split(":")[0].lstrip())
    f.close()

    return sorted(set(breakpoints))

def gdb_command_str(program: str) -> str:
    """
    Construct a string to pass into gdb that will set up all breakpoints
    and makes them automatically continue.
    """
    addrs = get(program)
    set_breakpoints = "\n".join(("break *0x"+x) for x in addrs) + '\n'
    # print(set_breakpoints)
    # enable_count = 'enable count ' + ' '.join(('*0x' + x) for x in addrs) + '\n'
    # print(enable_count)
    pass_cmd = "\ncommands 1-$bpnum\nsilent\ncontinue 1000000\nend\n"

    full_command = set_breakpoints + pass_cmd + ""

    return full_command

def count_unique_hits(breakpoint_output: bytes) -> float:
    """
    Count how many unique breakpoints were hit.
    """
    lines = breakpoint_output.split(b"\n")[1:-1]
    count = 0

    for line in lines:
        if line.startswith(b"\tbreakpoint already hit"):
            count += 1

    #print(breakpoint_output)
    return float(count)

def count_total_hits(breakpoint_output: bytes) -> float:
    """
    Count how many breakpoints were hit in total.
    """
    lines = breakpoint_output.split(b"\n")[1:-1]
    count = 0

    for line in lines:
        if line.startswith(b"\tbreakpoint already hit"):
            count += int(line.split(b" ")[3])

    return float(count)
