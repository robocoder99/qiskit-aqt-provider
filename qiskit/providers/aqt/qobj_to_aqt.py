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
            line = 'self.cnot({}, {})'.format(inst.params[1], inst.qubits[0])
        elif inst.name == 'cz':
            line = 'self.cz({}, {})'.format(inst.params[1], inst.qubits[0])
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
    return json.dumps(ops)


def qobj_to_aqt(qobj):
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
    out.append("\tdef build(self):")
    out.append("\t\tself.setattr_device('core')")

    # Setup kernel
    out.append("\t@kernel")
    out.append("\tdef run(self):")

    # Add lines
    for experiment in qobj.experiments:
        out.append(["\t\t{}".format(l) 
            for l in _experiment_to_seq(experiment)])


    # Add measurement
    out.append("\t\tself.detect_all()")
    out.append("\t\tr = self.measure_all()")

    return out
