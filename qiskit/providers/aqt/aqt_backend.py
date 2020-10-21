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

import requests

from qiskit.providers import BaseBackend
from qiskit.providers.models import BackendConfiguration
from . import aqt_job
from . import qobj_to_aqt


class AQTSimulator(BaseBackend):

    def __init__(self, provider):
        self.url = None #"https://gateway.aqt.eu/marmot/sim/"
        configuration = {
            'backend_name': 'aqt_qasm_simulator',
            'backend_version': '0.0.1',
            'url': self.url,
            'simulator': True,
            'local': False,
            'coupling_map': None,
            'description': 'DAX ion trap compiler',
            'basis_gates': ['id', 'x', 'y', 'z', 'h', 'rx', 'ry', 'rxx', 'cx', 'cz'],
            'memory': False,
            'n_qubits': 11,
            'conditional': False,
            'max_shots': 1024,
            'max_experiments': 1,
            'open_pulse': False,
            'gates': [
                {
                    'name': 'TODO',
                    'parameters': [],
                    'qasm_def': 'TODO'
                }
            ]
        }
        super().__init__(
            configuration=BackendConfiguration.from_dict(configuration),
            provider=provider)

    def run(self, qobj):
        aqt_json = qobj_to_aqt.qobj_to_aqt(qobj)[0]
        header = {"SDK": "qiskit"}
        print(qobj)
        print(aqt_json)

        job = aqt_job.AQTJob(self, 0, qobj=qobj)
        return job

