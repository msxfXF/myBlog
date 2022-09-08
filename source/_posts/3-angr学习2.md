---
title: 3-angr学习2
date: 2022-06-23 20:55:57
tags: 
- 固件
- 逆向
categories: 
- 固件
---

## Blocks
blocks是给定地址处，代码的基本片段，可以使用```project.factory.block()```创建

``` ipython
>>> block = proj.factory.block(proj.entry) # lift a block of code from the program's entry point
<Block for 0x401670, 42 bytes>

>>> block.pp()                          # pretty-print a disassembly to stdout
0x401670:       xor     ebp, ebp
0x401672:       mov     r9, rdx
0x401675:       pop     rsi
0x401676:       mov     rdx, rsp
0x401679:       and     rsp, 0xfffffffffffffff0
0x40167d:       push    rax
0x40167e:       push    rsp
0x40167f:       lea     r8, [rip + 0x2e2a]
0x401686:       lea     rcx, [rip + 0x2db3]
0x40168d:       lea     rdi, [rip - 0xd4]
0x401694:       call    qword ptr [rip + 0x205866]

>>> block.instructions                  # 指令数量
0xb
>>> block.instruction_addrs             # 指令地址list
[0x401670, 0x401672, 0x401675, 0x401676, 0x401679, 0x40167d, 0x40167e, 0x40167f, 0x401686, 0x40168d, 0x401694]
```

另外，可以输出blocks的汇编语句和VEX语句
```ipython
>>> block.capstone                       # capstone disassembly
<CapstoneBlock for 0x401670>
>>> block.vex                            # VEX IRSB (that's a Python internal address, not a program address)
<pyvex.block.IRSB at 0x7706330>
```
``` ipython
>>> block.capstone.insns
[<CapstoneInsn "xor" for 0x400580>,
 <CapstoneInsn "mov" for 0x400582>,
 <CapstoneInsn "pop" for 0x400585>,
 <CapstoneInsn "mov" for 0x400586>,
 <CapstoneInsn "and" for 0x400589>,
 <CapstoneInsn "push" for 0x40058d>,
 <CapstoneInsn "push" for 0x40058e>,
 <CapstoneInsn "mov" for 0x40058f>,
 <CapstoneInsn "mov" for 0x400596>,
 <CapstoneInsn "mov" for 0x40059d>,
 <CapstoneInsn "call" for 0x4005a4>]
```

### States
Project 对象仅仅表示初始化后的程序，执行时，需要使用SimState对象存储状态

``` ipython
>>> state = proj.factory.entry_state()
<SimState @ 0x401670>
```

SimState包含程序的内存、寄存器、文件系统数据等任何运行时数据。可以使用```state.regs```、```state.mem```来访问寄存器和内存。

``` ipython
>>> state.regs.rip        # get the current instruction pointer
<BV64 0x401670>
>>> state.regs.rax
<BV64 0x1c>
>>> state.mem[proj.entry].int.resolved  # interpret the memory at the entry point as a C int
<BV32 0x8949ed31>
```

需要注意的是寄存器和内存的值不是Python的int，而是一种包装后的**bitvectors**类型，该类型可以表示未定义(UNINITIALIZED)，可以包装溢出，具有长度，具有名字或值。

int和bitvector相互转换方式:

``` ipython
>>> bv = state.solver.BVV(0x1234, 32)       # create a 32-bit-wide bitvector with value 0x1234
<BV32 0x1234>                               # BVV stands for bitvector value
>>> state.solver.eval(bv)                # convert to Python int
0x1234
```

存取规则：

- 使用array\[index\]表示地址
- 使用.\<type\>断言类型，如：char, short, int, long, size_t, uint8_t, uint16_t
- 默认对Python int有隐式类型转换，使用.resolved转为bitvector，使用.concrete转为Python int

### Simulation Managers

simulation managers控制语句的移动和状态的改变，simgr.active是状态的列表，默认状态是simgr.active
``` ipython
>>> simgr = proj.factory.simulation_manager(state)
<SimulationManager with 1 active>
>>> simgr.active
[<SimState @ 0x401670>]
```

使用```simgr.step()```步进一个block
``` ipython
>>> simgr.active
[<SimState @ 0x1020300>]
>>> simgr.active[0].regs.rip                 # new and exciting!
<BV64 0x1020300>
>>> state.regs.rip                           # still the same!
<BV64 0x401670>
``` 

### Analyses
Analyses是有许多功能强大的工具，包括CFG、DFG、BinDiff，需要仔细看对应的文档进行使用！！！

[API文档]{http://angr.io/api-doc/angr.html?highlight=cfg#module-angr.analysis}