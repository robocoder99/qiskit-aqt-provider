# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import json

from numpy import pi


def _experiment_to_seq(experiment):
    ops = []
    meas = 0
    for inst in experiment.instructions:
        if inst.name == 'id':
            line = 'self.i({})'.format(inst.qubits[0])
        elif inst.name == 'x':
            line = 'self.x({})'.format(inst.qubits[0])
        elif inst.name == 'y':
            line = 'self.y({})'.format(inst.qubits[0])
        elif inst.name == 'z':
            line = 'self.z({})'.format(inst.qubits[0])
        elif inst.name == 'h':
            line = 'self.h({})'.format(inst.qubits[0])
        elif inst.name == 'rx':
            line = 'self.rx({}, {})'.format(inst.params[0], inst.qubits[0])
        elif inst.name == 'ry':
            line = 'self.ry({}, {})'.format(inst.params[0], inst.qubits[0])
        elif inst.name == 'rz':
            line = 'self.rz({}, {})'.format(inst.params[0], inst.qubits[0])
        elif inst.name == 'cx':
            line = 'self.cnot({}, {})'.format(inst.qubits[0], inst.qubits[1])
        elif inst.name == 'cz':
            line = 'self.cz({}, {})'.format(inst.qubits[0], inst.qubits[1])
        elif inst.name == 'measure':
            meas += 1
            continue
        elif inst.name == 'barrier':
            continue
        else:
            raise Exception("Operation '%s' outside of basis id, x, y, z, h, rx, ry, rz, cx, cz" %
                            inst.name)

        ops.append(line)
    
    if not meas:
        raise ValueError('Circuit must have at least one measurements.')
    return ops


def qobj_to_aqt(qobj, shots):
    """Return a list of DAX code strings for each experiment in a qobj

    If we were actually working with the hardware we would be executing these code strings
    to build a real kernel in DAX.

    """

    if len(qobj.experiments) > 1:
        raise Exception

    out = []

    # Setup class
    out.append("from dax.experiment import *")
    out.append("class ConstructedExperiment(EnvExperiment):")

    # Setup Class' build method
    out.append("\tdef build(self):")
    out.append("\t\tself.setattr_device('core')")
    out.append(f"\t\tself.num_iterations = {shots}") # (x = number of shots)
    
    # Setup Class' run method
    out.append("\tdef run():")
    out.append("\t\tself._run()")
    out.append("\t\treturn self.result_list")

    ## Setup kernel
    out.append("\t@kernel")

    # Setup kernel _run() method (never changes)
    out.append("\tdef _run(self):")
    out.append("\t\tfor _ range(self.num_iterations):")
    out.append("\t\t\tr = self._qiskit_kernel()")
    out.append("\t\t\tself._collect_data(r)")

    # Defining _qiskit_kernel() method (this is the QC program)
    out.append("\tkernel")
    out.append("\tdef _qiskit_kernel():")
    for experiment in qobj.experiments:
        # Init ions
        out.append("\t\tself.load_ions({})".format(experiment.config.n_qubits))
        out.append("\t\tself.initialize_all()")
        
        # Add lines
        out += ["\t\t{}".format(l) 
            for l in _experiment_to_seq(experiment)]

    # Add measurement
    out.append("\t\tself.detect_all()")
    out.append("\t\tr = self.measure_all()")
    out.append("\t\treturn r")
    
    return out
