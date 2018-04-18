"""
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * - Neither the name of prim nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""

import gzip

class SimLogStats(object):
  """
  Statistics for a simulation log.
  """

  def __init__(self, filename):
    # variables to be read from the log file
    self.total_event_count = None
    self.total_sim_units = None
    self.total_real_seconds = None
    self.events_per_real_second = None
    self.events_per_sim_unit = None
    self.sim_units_per_real_second = None

    # read in raw data
    summary = False
    opener = gzip.open if filename.endswith('.gz') else open
    with opener(filename, 'rb') as fd:
      for line in fd:
        line = line.decode('utf-8')
        if not summary:
          if line.startswith('*** Simulation Summary ***'):
            summary = True
        else:
          if line.startswith('Total event count:'):
            assert self.total_event_count == None
            self.total_event_count = int(line[line.find(':')+1:].strip())
          elif line.startswith('Total sim units:'):
            assert self.total_sim_units == None
            self.total_sim_units = int(line[line.find(':')+1:].strip())
          elif line.startswith('Total real seconds:'):
            assert self.total_real_seconds == None
            self.total_real_seconds = float(line[line.find(':')+1:].strip())
          elif line.startswith('Events per real second:'):
            assert self.events_per_real_second == None
            self.events_per_real_second = float(line[line.find(':')+1:].strip())
          elif line.startswith('Events per sim unit:'):
            assert self.events_per_sim_unit == None
            self.events_per_sim_unit = float(line[line.find(':')+1:].strip())
          elif line.startswith('Sim units per real second:'):
            assert self.sim_units_per_real_second == None
            self.sim_units_per_real_second = float(line[line.find(':')+1:].strip())

    # check that we got everything we expect
    assert self.total_event_count != None
    assert self.total_sim_units != None
    assert self.total_real_seconds != None
    assert self.events_per_real_second != None
    assert self.events_per_sim_unit != None
    assert self.sim_units_per_real_second != None
