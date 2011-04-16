#
# Copyright 2010 Free Software Foundation, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from volk_regexp import *
import string
from emit_omnilog import *

#ok todo list:
#put n_archs into the info struct so it doesn't have to be arch_defs[0].

def make_c(machines, archs, functions, arched_arglist, my_arglist):
    tempstring = r"""
// This file is automatically generated by make_c.py.
// Do not edit this file.
"""
    tempstring += """
#include <volk/volk_common.h>
#include <volk/volk_machines.h>
#include <volk/volk_registry.h>
#include <volk/volk_typedefs.h>
#include <volk/volk_cpu.h>
#include "volk_rank_archs.h"
#include <volk/volk.h>
#include <stdio.h>

"""
    tempstring += emit_prolog();
    
#OK here's the deal. the .h prototypes the functions. the .c impls them as fptrs, can use p_whatever.
#also .c impls the get_machine call
#also .c impls the default call for each fn

#here do static fn get arch
    tempstring += r"""
struct volk_machine *get_machine(void) {
    extern struct volk_machine volk_machines[];
    extern unsigned int n_volk_machines;
    static struct volk_machine *machine = NULL;
    
    if(machine != NULL) return machine;
    else {
        unsigned int max_score = 0;
        int i;
        for(i=0; i<n_volk_machines; i++) {
            if(!(volk_machines[i].caps & (~volk_get_lvarch()))) {
                if(volk_machines[i].caps > max_score) {
                    max_score = volk_machines[i].caps;
                    machine = &(volk_machines[i]);
                }
            }
        }
        printf("Using Volk machine: %s\n", machine->name);
        return machine;
    }
}

static unsigned int get_index(const char **indices, char *arch_name) {
    



}

"""
    
    for i in range(len(functions)):
        tempstring += "void get_" + functions[i] + replace_arch.sub("", arched_arglist[i]) + "\n"
        tempstring += "    %s = get_machine()->%s_archs[volk_rank_archs(get_machine()->%s_desc.arch_defs, get_machine()->%s_desc.n_archs, volk_get_lvarch())];\n" % (functions[i], functions[i], functions[i], functions[i])
        tempstring += "    %s(%s);\n}\n\n" % (functions[i], my_arglist[i])
        tempstring += replace_volk.sub("p", functions[i]) + " " + functions[i] + " = &get_" + functions[i] + ";\n\n"
        

    tempstring += emit_epilog();
        
    return tempstring


