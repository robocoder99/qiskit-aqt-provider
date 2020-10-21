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

# pylint: disable=protected-access

import time

import requests

from qiskit.providers import BaseJob
from qiskit.providers import JobError
from qiskit.providers import JobTimeoutError
from qiskit.result import Result
from .qobj_to_aqt import qobj_to_aqt


class AQTJob(BaseJob):
    def __init__(self, backend, job_id, qobj=None, aqt_qobj=None):
        super().__init__(backend, job_id)
        self._backend = backend        
        self.qobj = qobj
        self.aqt_qobj = aqt_qobj
        self._job_id = job_id        
 
    def result(self):        
        result = {'samples': [0,0]}
        results = [
            {
                'success': True,
                'shots': len(result['samples']),
                'data': {'dax_code': self.aqt_qobj},
                'header': {'name': self.qobj.experiments[0].header.name}
            }]

        return Result.from_dict({
            'results': results,
            'backend_name': self._backend._configuration.backend_name,
            'backend_version': self._backend._configuration.backend_version,
            'qobj_id': self.qobj.qobj_id,
            'success': True,
            'job_id': self._job_id,
        })

    def cancel(self):
        pass

    def status(self):
        return  'success'        

    def submit(self):
        pass
        
