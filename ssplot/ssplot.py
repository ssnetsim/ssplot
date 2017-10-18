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

# Python 3 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import copy
import gridstats
import gzip
import math
import numpy
import percentile
import sys
import random
import matplotlib.ticker as ticker

def maxNoInfinity(v):
  m = float('inf')
  for t in v:
    if not math.isinf(t):
      if math.isinf(m):
        m = t
      else:
        m = max(t, m)
  return m

def setStyle(style, plt, lineCount):
  lw = [1] * lineCount
  lineStyles = ['solid'] * lineCount
  # rainbow
  if style == 'rainbow':
    cmap = plt.get_cmap('gist_rainbow')
    colors = [cmap(idx) for idx in numpy.linspace(0, 1, lineCount)]
    markerStyles = ["None"] * lineCount
    markerSize = [3] * lineCount
  # rainbow-dots
  elif style == 'rainbow-dots':
    cmap = plt.get_cmap('gist_rainbow')
    colors = [cmap(idx) for idx in numpy.linspace(0, 1, lineCount)]
    markerStyles = ['o'] * lineCount
    markerSize = [3] * lineCount
  # inferno
  elif style == 'inferno':
    cmap = plt.get_cmap('inferno')
    colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, lineCount)]
    lw = [2] * lineCount
    markerStyles = ["None"] * lineCount
    markerSize = [4] * lineCount
  # inferno-dots
  elif style == 'inferno-dots':
    cmap = plt.get_cmap('inferno')
    colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, lineCount)]
    lw = [2] * lineCount
    markerStyles = ['o'] * lineCount
    markerSize = [4] * lineCount
  # black
  elif style == 'black':
    colors = ['k'] * lineCount
    lines = ['solid', 'dashed','dashdot','dotted']
    markers = ['s', '^', 'o', 'd', 'x', '|', 'None']
    styles = [(m, l) for l in lines for m in markers]
    assert len(styles) > lineCount, 'Not enough marks for no. lines'
    markerStyles = [s[0] for s in styles]
    lineStyles = [s[1] for s in styles]
    markerSize = [4] * lineCount
  # inferno-markers
  elif style == 'inferno-markers':
    cmap = plt.get_cmap('inferno')
    colors = [cmap(idx) for idx in numpy.linspace(0.1, 0.9, lineCount)]
    lines = ['solid','dashed','dashdot','dotted']
    markers = ['s', '^', 'o', 'd', 'x', '|', 'None']
    styles = [(m, l) for l in lines for m in markers]
    assert len(styles) > lineCount, 'Not enough marks for no. lines'
    markerStyles = [s[0] for s in styles]
    lineStyles = [s[1] for s in styles]
    markerSize = [4] * lineCount
  else:
    assert False, 'Unsupported style: {}'.format(style)

  #create tuple
  styleAll = zip(colors, lineStyles, lw, markerStyles, markerSize)
  return list(styleAll)

# a class to represent latency stats
class LatencyStats(object):
  """
  Latency statistics for a single simulation run
  """

  def __init__(self, filename):
    # read in raw data
    self.times = []
    self.latencies = []
    opener = gzip.open if filename.endswith('.gz') else open
    with opener(filename, 'rb') as fd:
      while (True):
        line = fd.readline().decode('utf-8')
        delim = line.find(',')
        if (delim >= 0):
          cols = line.split(',')
          startTime = float(cols[0])
          endTime = float(cols[1])
          self.times.append(startTime)
          self.latencies.append(endTime - startTime)
        else:
          break
      self.times = numpy.array(self.times)
      self.latencies = numpy.array(self.latencies)
      assert len(self.times) == len(self.latencies)

    # size
    self.size = len(self.times)
    if self.size > 0:
      # min and max
      self.tmin = min(self.times)
      self.tmax = max(self.times)
      self.smin = min(self.latencies)
      self.smax = max(self.latencies)
      if self.smin < 0:
        raise Exception('latencies can\'t be negative!')

      # compute time-bucketed averages
      numBins = 40
      binWidth = (self.tmax - self.tmin) / numBins
      self.binTimes = numpy.linspace(self.tmin, self.tmax - binWidth, numBins)
      self.binAverages = [0] * numBins
      binCounts = [0] * numBins
      for idx in range(len(self.latencies)):
        sbin = math.floor((self.times[idx] - self.tmin) / binWidth)
        sbin = min(numBins - 1, sbin)  # tmax causes sbin == numBins
        self.binAverages[sbin] += self.latencies[idx]
        binCounts[sbin] += 1
      for idx in range(len(self.binAverages)):
        if binCounts[idx] > 0:
          self.binAverages[idx] /= binCounts[idx]
        else:
          self.binAverages[idx] = 0

      # compute the probability density function
      self.pdfBins = 50
      hist, self.pdfx = numpy.histogram(self.latencies, bins=self.pdfBins)
      self.pdfy = hist.astype(float) / hist.sum()

      # compute the cumulative distribution function
      self.cdfx = numpy.sort(self.latencies)
      self.cdfy = numpy.linspace(1.0 / self.size, 1.0, self.size)

      # find percentiles
      self.p50 = self.percentile(0.50)
      self.p90 = self.percentile(0.90)
      self.p99 = self.percentile(0.99)
      self.p999 = self.percentile(0.999)
      self.p9999 = self.percentile(0.9999)

  def percentile(self, percent):
    if percent < 0 or percent > 1:
      raise Exception('percent must be between 0 and 1')
    index = int(round(percent * len(self.cdfx)))
    index = min(len(self.cdfy) - 1, index)
    return self.cdfx[index]

  def nines(self):
    if self.size > 0:
      nines = int(math.ceil(math.log10(len(self.cdfx))))
    else:
      nines = 5
    return nines

  def emptyPlot(self, axes, x, y):
    axes.text(x, y, 'No data', clip_on=False, color='red',
              verticalalignment='center',
              horizontalalignment='center')

  def generateScatter(self, axes, showPercentiles=False, randomColors=False,
                      units=None, title=None,
                      xmin=float('NaN'), xmax=float('NaN'),
                      ymin=float('NaN'), ymax=float('NaN')):
    # format axes
    if title:
      axes.set_title(title)
    if units:
      axes.set_xlabel('Time ({0})'.format(units))
    else:
      axes.set_xlabel('Time')
    if units:
      axes.set_ylabel('Latency ({0})'.format(units))
    else:
      axes.set_ylabel('Latency')

    # plot bounds
    if self.size > 0:
      spxmin = self.tmin
      spxmax = self.tmax
      spymin = max(self.smin * 0.99, 0)
      spymax = self.smax * 1.01
    else:
      spxmin = 0
      spxmax = 1
      spymin = 0
      spymax = 1
    if not math.isnan(xmin):
      spxmin = xmin
    if not math.isnan(xmax):
      spxmax = xmax
    if not math.isnan(ymin):
      spymin = ymin
    if not math.isnan(ymax):
      spymax = ymax
    axes.set_xlim(spxmin, spxmax)
    if spymin == spymax:
      axes.set_ylim(spymin-1, spymax+1)
    else:
      axes.set_ylim(spymin, spymax)

    # grid
    axes.grid(True)
    axes.set_axisbelow(True)

    # detect non-empty data set
    if self.size > 0:
      # create plot
      if randomColors:
        colors = numpy.random.rand(len(self.times))
      else:
        colors = 'b'
      axes.scatter(self.times, self.latencies, color=colors, s=2)
      if showPercentiles:
        l50, = axes.plot([spxmin, spxmax], [self.p50, self.p50],
                         c='r', linewidth=2)
        l90, = axes.plot([spxmin, spxmax], [self.p90, self.p90],
                         c='g', linewidth=2)
        l99, = axes.plot([spxmin, spxmax], [self.p99, self.p99],
                         c='c', linewidth=2)
        l999, = axes.plot([spxmin, spxmax], [self.p999, self.p999],
                          c='m', linewidth=2)
        l9999, = axes.plot([spxmin, spxmax], [self.p9999, self.p9999],
                           c='y', linewidth=2)
    else:
      self.emptyPlot(axes, (spxmax - spxmin) / 2, (spymax - spymin) / 2)

  def generateAverage(self, axes, showPercentiles=False, units=None,
                      title=None,
                      xmin=float('NaN'), xmax=float('NaN'),
                      ymin=float('NaN'), ymax=float('NaN')):
    # format axes
    if title:
      axes.set_title(title)
    if units:
      axes.set_xlabel('Time ({0})'.format(units))
    else:
      axes.set_xlabel('Time')
    if units:
      axes.set_ylabel('Mean Latency ({0})'.format(units))
    else:
      axes.set_ylabel('Mean Latency')

    # plot bounds
    if self.size > 0:
      apxmin = self.tmin
      apxmax = self.tmax
      delta1p = (max(self.binAverages) - min(self.binAverages)) * 0.01
      apymin = min(self.binAverages) - delta1p
      apymax = max(self.binAverages) + delta1p
    else:
      apxmin = 0
      apxmax = 1
      apymin = 0
      apymax = 1
    if not math.isnan(xmin):
      apxmin = xmin
    if not math.isnan(xmax):
      apxmax = xmax
    if not math.isnan(ymin):
      apymin = ymin
    if not math.isnan(ymax):
      apymax = ymax
    axes.set_xlim(apxmin, apxmax)
    if apymin == apymax:
      axes.set_ylim(apymin-1, apymax+1)
    else:
      axes.set_ylim(apymin, apymax)

    # grid
    axes.grid(True)
    axes.set_axisbelow(True)

    # detect non-empty data set
    if self.size > 0:
      # create plot
      axes.plot(self.binTimes, self.binAverages)
    else:
      self.emptyPlot(axes, (apxmax - apxmin) / 2, (apymax - apymin) / 2)

  def generatePdf(self, axes, showPercentiles=False, units=None, title=None,
                  xmin=float('NaN'), xmax=float('NaN'),
                  ymin=float('NaN'), ymax=float('NaN')):
    # format axes
    if title:
      axes.set_title(title)
    if units:
      axes.set_xlabel('Latency ({0})'.format(units))
    else:
      axes.set_xlabel('Latency')
    axes.set_ylabel('Probability')

    # plot bounds
    if self.size > 0:
      ppxmin = self.smin
      ppxmax = self.smax
      ppymin = 0
      ppymax = max(self.pdfy) * 1.01
    else:
      ppxmin = 0
      ppxmax = 1
      ppymin = 0
      ppymax = 1
    if not math.isnan(xmin):
      ppxmin = xmin
    if not math.isnan(xmax):
      ppxmax = xmax
    if not math.isnan(ymin):
      ppymin = max(0, ymin)
    if not math.isnan(ymax):
      ppymax = min(1, ymax)
    if ppxmin == ppxmax:
      axes.set_xlim(ppxmin-1, ppxmax+1)
    else:
      axes.set_xlim(ppxmin, ppxmax)
    axes.set_ylim(ppymin, ppymax)

    # grid
    axes.grid(True)
    axes.set_axisbelow(True)

    # detect non-empty data set
    if self.size > 0:
      # create plot
      axes.plot(self.pdfx[:-1], self.pdfy)
      if showPercentiles:
        l50, = axes.plot([self.p50, self.p50], [0, 1], c='r')
        l90, = axes.plot([self.p90, self.p90], [0, 1], c='g')
        l99, = axes.plot([self.p99, self.p99], [0, 1], c='c')
        l999, = axes.plot([self.p999, self.p999], [0, 1], c='m')
        l9999, = axes.plot([self.p9999, self.p9999], [0, 1], c='y')
        unitstr = ' ' + units if units else ''
        axes.legend((l50, l90, l99, l999, l9999),
                    ('50th %ile    ({0:.3f}{1})'.format(self.p50, unitstr),
                     '90th %ile    ({0:.3f}{1})'.format(self.p90, unitstr),
                     '99th %ile    ({0:.3f}{1})'.format(self.p99, unitstr),
                     '99.9th %ile  ({0:.3f}{1})'.format(self.p999, unitstr),
                     '99.99th %ile ({0:.3f}{1})'.format(self.p9999, unitstr)))
    else:
      self.emptyPlot(axes, (ppxmax - ppxmin) / 2, (ppymax - ppymin) / 2)

  def generateCdf(self, axes, showPercentiles=False, units=None, title=None,
                  xmin=float('NaN'), xmax=float('NaN'),
                  ymin=float('NaN'), ymax=float('NaN')):
    # format axes
    if title:
      axes.set_title(title)
    if units:
      axes.set_xlabel('Latency ({0})'.format(units))
    else:
      axes.set_xlabel('Latency')
    axes.set_ylabel('Probability')

    # plot bounds
    if self.size > 0:
      cpxmin = self.smin
      cpxmax = self.smax
      cpymin = 0
      cpymax = 1
    else:
      cpxmin = 0
      cpxmax = 1
      cpymin = 0
      cpymax = 1
    if not math.isnan(xmin):
      cpxmin = xmin
    if not math.isnan(xmax):
      cpxmax = xmax
    if not math.isnan(ymin):
      cpymin = max(0, ymin)
    if not math.isnan(ymax):
      cpymax = min(1, ymax)
    if cpxmin == cpxmax:
      axes.set_xlim(cpxmin-1, cpxmax+1)
    else:
      axes.set_xlim(cpxmin, cpxmax)
    axes.set_ylim(cpymin, cpymax)

    # grid
    axes.grid(True)
    axes.set_axisbelow(True)

    # detect non-empty data set
    if self.size > 0:
      # create plot
      axes.plot(self.cdfx, self.cdfy)
      if showPercentiles:
        axes.plot([self.p50, self.p50], [0, 0.50], c='r')
        axes.plot([cpxmin, self.p50], [0.50, 0.50], c='r')
        axes.plot([self.p90, self.p90], [0, 0.90], c='g')
        axes.plot([cpxmin, self.p90], [0.90, 0.90], c='g')
        axes.plot([self.p99, self.p99], [0, 0.99], c='c')
        axes.plot([cpxmin, self.p99], [0.99, 0.99], c='c')
        axes.plot([self.p999, self.p999], [0, 0.999], c='m')
        axes.plot([cpxmin, self.p999], [0.999, 0.999], c='m')
        axes.plot([self.p9999, self.p9999], [0, 0.9999], c='y')
        axes.plot([cpxmin, self.p9999], [0.9999, 0.9999], c='y')
    else:
      self.emptyPlot(axes, (cpxmax - cpxmin) / 2, (cpymax - cpymin) / 2)

  def generateLogCdf(self, axes, xlog=False, units=None, title=None,
                     xmin=float('NaN'), xmax=float('NaN')):
    # format axes
    if title:
      axes.set_title(title)
    if units:
      axes.set_xlabel('Latency ({0})'.format(units))
    else:
      axes.set_xlabel('Latency')
    axes.set_ylabel('Percentile')
    axes.set_yscale('percentile', nines=self.nines())
    if xlog:
      axes.set_xscale('log')

    # plot bounds
    if self.size > 0:
      lpxmin = self.smin * 0.999
      lpxmax = self.smax * 1.001
    else:
      lpxmin = 0
      lpxmax = 1
    if not math.isnan(xmin):
      lpxmin = xmin
    if not math.isnan(xmax):
      lpxmax = xmax
    axes.set_xlim(lpxmin, lpxmax)
    if self.size == 0:
      axes.set_ylim(0, 0.99999)

    # grid
    axes.grid(True)
    axes.set_axisbelow(True)

    # detect non-empty data set
    if self.size > 0:
      # create the plot
      axes.scatter(self.cdfx, self.cdfy, color='b', s=2)
    else:
      self.emptyPlot(axes, (lpxmax - lpxmin) / 2, 0.9965)

  def quadPlot(self, plt, filename, title='', units=None, average=False,
               spxmin=float('NaN'), spxmax=float('NaN'),
               spymin=float('NaN'), spymax=float('NaN'),
               ppxmin=float('NaN'), ppxmax=float('NaN'),
               ppymin=float('NaN'), ppymax=float('NaN'),
               cpxmin=float('NaN'), cpxmax=float('NaN'),
               cpymin=float('NaN'), cpymax=float('NaN'),
               lpxmin=float('NaN'), lpxmax=float('NaN'),
               size=(16, 10)):
    fig = plt.figure(figsize=size)

    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    self.generateScatter(ax1, showPercentiles=True, randomColors=False,
                         units=units, title='Latency scatter',
                         xmin=spxmin, xmax=spxmax, ymin=spymin, ymax=spymax)
    self.generatePdf(ax2, showPercentiles=True, units=units,
                     title='Probability density function',
                     xmin=ppxmin, xmax=ppxmax, ymin=ppymin, ymax=ppymax)
    self.generateCdf(ax3, showPercentiles=True, units=units,
                     title='Cumulative distribution function',
                     xmin=cpxmin, xmax=cpxmax, ymin=cpymin, ymax=cpymax)
    self.generateLogCdf(ax4, xlog=False, units=units,
                        title='Logarithmic cumulative distribution function',
                        xmin=lpxmin, xmax=lpxmax)

    fig.tight_layout()
    if size[0] < 8.0:
      assert False, 'Figure width must be at least 8'
    if size[1] < 6.0:
      assert False, 'Figure height must be at least 6'
    if title:
      if size[1] >= 8.0:
        fig.suptitle(title, fontsize=20)
      elif size[1] < 8.0:
        fig.suptitle(title, fontsize=16)
      fig.subplots_adjust(top=0.9)
    fig.savefig(filename)

  def scatterPlot(self, plt, filename, title='', units=None,
                  xmin=float('NaN'), xmax=float('NaN'),
                  ymin=float('NaN'), ymax=float('NaN'),
                  size=(16,10)):
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    self.generateScatter(ax1, showPercentiles=True, randomColors=False,
                         units=units, title=title,
                         xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    fig.tight_layout()
    fig.savefig(filename)

  def averagePlot(self, plt, filename, title='', units=None,
                  xmin=float('NaN'), xmax=float('NaN'),
                  ymin=float('NaN'), ymax=float('NaN'),
                  size=(16, 10)):
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    self.generateAverage(ax1, units=units, title=title,
                         xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    fig.tight_layout()
    fig.savefig(filename)

  def pdfPlot(self, plt, filename, title='', units=None,
              xmin=float('NaN'), xmax=float('NaN'),
              ymin=float('NaN'), ymax=float('NaN'),
              size=(16, 10)):
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    self.generatePdf(ax1, showPercentiles=True, units=units, title=title,
                     xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    fig.tight_layout()
    fig.savefig(filename)

  def cdfPlot(self, plt, filename, title='', units=None,
              xmin=float('NaN'), xmax=float('NaN'),
              ymin=float('NaN'), ymax=float('NaN'),
              size=(16, 10)):
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    self.generateCdf(ax1, showPercentiles=True, units=units, title=title,
                     xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    fig.tight_layout()
    fig.savefig(filename)

  def logCdfPlot(self, plt, filename, title='', units=None,
                 xmin=float('NaN'), xmax=float('NaN'),
                 size=(16, 10)):
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    self.generateLogCdf(ax1, xlog=False, units=units, title=title,
                        xmin=xmin, xmax=xmax)

    fig.tight_layout()
    fig.savefig(filename)


# a class to represent load vs. latency stats
class LoadLatencyStats(object):

  FIELDS = ['Minimum', 'Mean', 'Median', '90th%', '99th%', '99.9th%',
            '99.99th%', '99.999th%', 'Maximum']

  def __init__(self, start, stop, step, grids, **kwargs):
    # create arrays
    load = numpy.arange(start, stop, step)
    self.data = {'Load': load}
    for field in LoadLatencyStats.FIELDS:
      self.data[field] = numpy.empty(len(load), dtype=float)

    # parse kwargs
    verbose = kwargs.get('verbose', False);
    statRow = kwargs.get('row', 'Packet')
    if verbose:
      print('load {0}'.format(self.data['Load']))
      print('analyzing {0}s'.format(statRow))

    assert len(grids) == len(self.data['Load']), "wrong number of grids"

    # load data arrays
    for idx, grid in enumerate(grids):
      assert isinstance(grid, gridstats.GridStats), \
        "grids must be GridStats"
      if verbose:
        print('extracting {0}'.format(grid.filename))
      for key in self.data.keys():
        if key != 'Load':
          s = grid.get(statRow, key)
          if verbose:
            print('Load {0} {1} is {2}'.format(self.data['Load'][idx], key, s))
          self.data[key][idx] = s

  # lplot
  def plotAll(self, plt, filename, title='', units=None,
              ymin=float('NaN'), ymax=float('NaN'),
              style='rainbow', size=(16,10), nomin=False):
    if math.isnan(ymin):
      ymin = min(self.data['Minimum'])
    if math.isnan(ymax):
      ymax = maxNoInfinity(self.data['Maximum'])

    # create figure
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    # set plot styles
    fields = LoadLatencyStats.FIELDS
    if nomin:
      fields.remove('Minimum')
    all_style = setStyle(style, plt, len(fields))

    # set axis labels
    ax1.set_xlabel('Load (%)')
    if units:
      ax1.set_ylabel('Latency ({0})'.format(units))
    else:
      ax1.set_ylabel('Latency')

    # plot load vs. latency curves
    lines = []
    for idx, field in enumerate(reversed(fields)):
      lines.append(ax1.plot(self.data['Load'], self.data[field],
                            color=all_style[idx][0],
                            linestyle=all_style[idx][1],
                            lw=all_style[idx][2],
                            marker=all_style[idx][3],
                            markevery=5,
                            markersize=all_style[idx][4],
                            label=field)[0])

    # if given, apply title
    if title:
      ax1.set_title(title, fontsize=20)

    # create legend
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper left', fancybox=True,
               facecolor="white", edgecolor="black", ncol=1)

    # set plot bounds
    ax1.set_xlim(self.data['Load'][0], self.data['Load'][-1]);
    ax1.set_ylim(ymin, ymax);

    # ticks
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax1.xaxis.set_minor_locator(ticker.MaxNLocator(20))

    # grid
    ax1.grid(True)
    ax1.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(filename)

  @staticmethod
  def plotCompare(plt, filename, stats, field='Mean', labels=None, title='',
                  units=None, ymin=float('NaN'), ymax=float('NaN'),
                  style='rainbow', size=(16,10)):
    # make sure the loads are all the same
    mload = stats[0].data['Load']
    for stat in stats:
      assert len(mload) == len(set(mload).intersection(stat.data['Load'])), \
        print('{0} != {1}'.format(mload, stat.data['Load']))
    if labels == None:
      labels = []
    assert len(labels) == 0 or len(labels) == len(stats)
    assert field in LoadLatencyStats.FIELDS

    # create figure
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    # set plot styles
    all_style = setStyle(style, plt, len(stats))

    # set axis labels
    ax1.set_xlabel('Load (%)')
    if units:
      ax1.set_ylabel('{0} Latency ({1})'.format(field, units))
    else:
      ax1.set_ylabel('{0} Latency'.format(field))

    # plot all lines
    lines = []
    for idx, stat in enumerate(stats):
      # label
      label = None
      if len(labels) > 0:
        label = labels[idx]
      line, = ax1.plot(mload, stat.data[field],
                       color=all_style[idx][0],
                       linestyle=all_style[idx][1],
                       lw=all_style[idx][2],
                       marker=all_style[idx][3],
                       markevery=5,
                       markersize=all_style[idx][4],
                       label=label)
      lines.append(line)

    # if given, apply title
    if title:
      ax1.set_title(title, fontsize=20)

    # set plot bounds
    ax1.set_xlim(stats[0].data['Load'][0], stats[0].data['Load'][-1]);
    if not math.isnan(ymin) and not math.isnan(ymax):
      ax1.set_ylim(ymin, ymax)
    elif not math.isnan(ymin):
      ax1.set_ylim(bottom=ymin)
    elif not math.isnan(ymax):
      ax1.set_ylim(top=ymax)

    # ticks
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax1.xaxis.set_minor_locator(ticker.MaxNLocator(20))

    # grid
    ax1.grid(True)
    ax1.set_axisbelow(True)

    # create legend
    if len(labels) > 0:
      labels = [line.get_label() for line in lines]
      ax1.legend(lines, labels, loc='upper left', fancybox=True,
                 facecolor="white", edgecolor="black", ncol=1)

    fig.tight_layout()
    fig.savefig(filename)

# a class to represent rate stats
class RateStats(object):

  FIELDS = ['Minimum', 'Mean', 'Maximum']

  def __init__(self, start, stop, step, grids, **kwargs):
    # check that all grids have the same structure
    for grid in grids[1:]:
      if not grid.sameSize(grids[0]):
        raise ValueError('Grid from {0} doesn\'t match the structure from {1}'
                         .format(grid, grids[0]))

    # create arrays
    injected = numpy.arange(start, stop, step)
    self.data = {'Injected': injected}
    for field in RateStats.FIELDS:
      self.data[field] = numpy.empty(len(injected), dtype=float)

    # parse kwargs
    verbose = kwargs.get('verbose', False);
    if verbose:
      print('load {0}'.format(self.data['Injected']))

    assert len(grids) == len(self.data['Injected']), "wrong number of grids"

    # load data arrays
    for idx, grid in enumerate(grids):
      assert isinstance(grid, gridstats.GridStats), \
        "grids must be GridStats"
      if verbose:
        print('extracting {0}'.format(grid.filename))
      # extract delivered
      delivered = []
      for term in range(0, grid.num_rows - 1):
        delivered.append(grid.get(term, 'delivered', safe=True) * 100)
      # compute stats
      minEj = min(delivered)
      meanEj = sum(delivered) / len(delivered)
      maxEj = max(delivered)
      # prepare data
      self.data['Minimum'][idx] = minEj
      self.data['Mean'][idx] = meanEj
      self.data['Maximum'][idx] = maxEj
      if verbose:
        print('Injected={0} -> Min={1} Mean={2} Max={3}'.format(
          self.data['Injected'][idx], minEj, meanEj, maxEj))

  # rplot
  def plotAll(self, plt, filename, title='',
              ymin=float('NaN'), ymax=float('NaN'),
              style='rainbow', size=(16,10)):
    if math.isnan(ymin):
      ymin = min(self.data['Minimum'])
    if math.isnan(ymax):
      ymax = maxNoInfinity(self.data['Maximum'])

    # create figure
    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(1, 1, 1)

    # set plot styles
    all_style = setStyle(style, plt, len(RateStats.FIELDS))

    # set axis labels
    ax1.set_xlabel('Injected Rate')
    ax1.set_ylabel('Delivered Rate')

    # plot load vs. latency curves
    lines = []
    for idx, field in enumerate(reversed(RateStats.FIELDS)):
      lines.append(ax1.plot(self.data['Injected'], self.data[field],
                            color=all_style[idx][0],
                            linestyle=all_style[idx][1],
                            lw=all_style[idx][2],
                            marker=all_style[idx][3],
                            markersize=all_style[idx][4],
                            label=field)[0])

    # if given, apply title
    if title:
      ax1.set_title(title, fontsize=20)

    # create legend
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='upper left', fancybox=True,
               facecolor="white", edgecolor="black", ncol=1)

    # set plot bounds
    ax1.set_xlim(self.data['Injected'][0], self.data['Injected'][-1]);
    ax1.set_ylim(ymin, ymax);

    # ticks
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
    ax1.xaxis.set_minor_locator(ticker.MaxNLocator(20))

    # grid
    ax1.grid(True)
    ax1.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(filename)
