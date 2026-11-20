#!/usr/bin/env python3
"""Generates source/fxswitch.h from fx_apfOpcodeTable in source/fxinst.c.

fx_run() (with -DFX_SWITCH_DISPATCH) dispatches the GSU opcodes with a switch
built from this file instead of calling through the function pointer table,
so the opcode bodies get inlined into the interpreter loop. Indices that call
the same function share one case, so every body is inlined only once.
Entries 0x04c/0x14c/0x24c/0x34c (plot/rpix) are rewritten at run time by
fxemu.c and stay as a call through the table (default case).

Run from the repository root after any change to the opcode table:
    python3 tools/gen_fxswitch.py
"""
import os
import re

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'source')
s = open(os.path.join(root, 'fxinst.c')).read()
t = s[s.index('void (*fx_apfOpcodeTable[])(void) ='):]
t = t[t.index('{') + 1:t.index('};')]
t = re.sub(r'/\*.*?\*/', '', t, flags=re.S)
ents = [e.strip() for e in t.split(',') if e.strip()]
assert len(ents) == 1024, len(ents)
dyn = {0x04c, 0x14c, 0x24c, 0x34c}
groups = {}
for i, e in enumerate(ents):
    if i in dyn:
        continue
    m = re.fullmatch(r'&(fx_\w+)', e)
    assert m, e
    groups.setdefault(m.group(1), []).append(i)
out = ['/* Generated from fx_apfOpcodeTable by tools/gen_fxswitch.py: do not edit. */',
       '/* Entries 0x04c/0x14c/0x24c/0x34c (plot/rpix) change at run time: default case. */']
for f, idx in groups.items():
    out.append(''.join('case 0x%03x: ' % i for i in idx) + '%s(); break;' % f)
out.append('default: (*fx_apfOpcodeTable[vIndex])(); break;')
open(os.path.join(root, 'fxswitch.h'), 'w').write('\n'.join(out) + '\n')
print('fxswitch.h: %d functions, %d entries' % (len(groups), sum(len(v) for v in groups.values())))
