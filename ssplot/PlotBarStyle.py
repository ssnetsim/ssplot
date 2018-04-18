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

import numpy

class PlotBarStyle(object):
  """
  This is a plot bar style generator
  """

  __style_map = {}
  __default_style = None

  def __init__(self, style, plt, bar_count):
    assert style in PlotBarStyle.__style_map, \
      '{} is not a registered plot bar style'.format(style)
    self._all_styles = list(zip(*PlotBarStyle.__style_map[style](
      plt, bar_count)))
    assert len(self._all_styles) == bar_count, 'error in style implementation'

  @staticmethod
  def styles():
    return list(PlotBarStyle.__style_map.keys())

  @staticmethod
  def default():
    return PlotBarStyle.__default_style

  @staticmethod
  def registerStyle(style, func, default=False):
    assert style not in PlotBarStyle.__style_map, \
      '{} is already a registered plot style'.format(style)
    PlotBarStyle.__style_map[style] = func
    if default:
      PlotBarStyle.__default_style = style

  def __getitem__(self, index):
    names = ['color', 'edgecolor', 'ecolor', 'hatch']
    style = self._all_styles[index]
    assert len(names) == len(style)
    return dict(zip(names, style))

def colorful(plt, bar_count):
  if bar_count <= 3:
    cmap = plt.get_cmap('brg')
  else:
    cmap = plt.get_cmap('gist_rainbow')
  colors = [cmap(idx) for idx in numpy.linspace(0, 1, bar_count)]
  edgecolors = colors
  ecolors = colors
  hatches = [''] * bar_count
  return colors, edgecolors, ecolors, hatches
PlotBarStyle.registerStyle('colorful', colorful, True)

def black(plt, bar_count):
  colors = ['w'] * bar_count
  edgecolors = ['k'] * bar_count
  ecolors = ['k'] * bar_count
  hatches = ['//', '---', '++', '||', '.', '\\\\', 'o', 'xx', 'O', '*']
  assert len(hatches) >= bar_count, 'Too many bars for plot style'
  return colors, edgecolors, ecolors, hatches[:bar_count]
PlotBarStyle.registerStyle('black', black, False)

"""

Hatches:
‘/’, ‘|’, ‘|’, ‘-‘, ‘+’, ‘x’, ‘o’, ‘O’, ‘.’, ‘*’

def colorfulDots(plt, bar_count):
  line_widths = [1.5] * bar_count
  line_styles = ['solid'] * bar_count
  if bar_count <= 3:
    cmap = plt.get_cmap('brg')
  else:
    cmap = plt.get_cmap('gist_rainbow')
  colors = [cmap(idx) for idx in numpy.linspace(0, 1, bar_count)]
  marker_styles = ['o'] * bar_count
  marker_sizes = [4] * bar_count
  return colors, line_styles, line_widths, marker_styles, marker_sizes
PlotBarStyle.registerStyle('colorful-dots', colorfulDots)

def inferno(plt, bar_count):
  line_widths = [1.5] * bar_count
  line_styles = ['solid'] * bar_count
  cmap = plt.get_cmap('inferno')
  colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, bar_count)]
  marker_styles = ["None"] * bar_count
  marker_sizes = [4] * bar_count
  return colors, line_styles, line_widths, marker_styles, marker_sizes
PlotBarStyle.registerStyle('inferno', inferno)

def infernoDots(plt, bar_count):
  line_widths = [1.5] * bar_count
  line_styles = ['solid'] * bar_count
  cmap = plt.get_cmap('inferno')
  colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, bar_count)]
  marker_styles = ['o'] * bar_count
  marker_sizes = [4] * bar_count
  return colors, line_styles, line_widths, marker_styles, marker_sizes
PlotBarStyle.registerStyle('inferno-dots', infernoDots)

def infernoMarkers(plt, bar_count):
  line_widths = [1] * bar_count
  cmap = plt.get_cmap('inferno')
  colors = [cmap(idx) for idx in numpy.linspace(0.0, 0.9, bar_count)]
  line_styles = ['solid','dashed','dashdot','dotted']
  marker_styles = ['s', '^', 'o', 'd', 'x', '|', 'None']
  marker_line_styles = [(m, l) for l in line_styles for m in marker_styles]
  assert len(marker_line_styles) > bar_count, 'Too many lines for plot style'
  marker_styles = [s[0] for s in marker_line_styles]
  line_styles = [s[1] for s in marker_line_styles]
  marker_sizes = [4] * bar_count
  return colors, line_styles, line_widths, marker_styles, marker_sizes
PlotBarStyle.registerStyle('inferno-markers', infernoMarkers)

def plasma(plt, bar_count):
  line_widths = [1.5] * bar_count
  line_styles = ['solid'] * bar_count
  cmap = plt.get_cmap('plasma')
  colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, bar_count)]
  marker_styles = ["None"] * bar_count
  marker_sizes = [4] * bar_count
  return colors, line_styles, line_widths, marker_styles, marker_sizes
PlotBarStyle.registerStyle('plasma', plasma)

def plasmaDots(plt, bar_count):
  line_widths = [1.5] * bar_count
  line_styles = ['solid'] * bar_count
  cmap = plt.get_cmap('plasma')
  colors = [cmap(idx) for idx in numpy.linspace(0, 0.9, bar_count)]
  marker_styles = ['o'] * bar_count
  marker_sizes = [4] * bar_count
  return colors, line_styles, line_widths, marker_styles, marker_sizes
PlotBarStyle.registerStyle('plasma-dots', plasmaDots)

def plasmaMarkers(plt, bar_count):
  line_widths = [1] * bar_count
  cmap = plt.get_cmap('plasma')
  colors = [cmap(idx) for idx in numpy.linspace(0.0, 0.9, bar_count)]
  line_styles = ['solid','dashed','dashdot','dotted']
  marker_styles = ['s', '^', 'o', 'd', 'x', '|', 'None']
  marker_line_styles = [(m, l) for l in line_styles for m in marker_styles]
  assert len(marker_line_styles) > bar_count, 'Too many lines for plot style'
  marker_styles = [s[0] for s in marker_line_styles]
  line_styles = [s[1] for s in marker_line_styles]
  marker_sizes = [4] * bar_count
  return colors, line_styles, line_widths, marker_styles, marker_sizes
PlotBarStyle.registerStyle('plasma-markers', plasmaMarkers)

def generic_generator(name, color):
  def generic(plt, bar_count):
    line_widths = [1] * bar_count
    colors = [color] * bar_count
    line_styles = ['solid', 'dashed','dashdot','dotted']
    marker_styles = ['s', '^', 'o', 'd', 'x', '|', 'None']
    marker_line_styles = [(m, l) for l in line_styles for m in marker_styles]
    assert len(marker_line_styles) > bar_count, 'Too many lines for plot style'
    line_styles = [s[1] for s in marker_line_styles]
    marker_styles = [s[0] for s in marker_line_styles]
    marker_sizes = [5] * bar_count
    return colors, line_styles, line_widths, marker_styles, marker_sizes
  return generic
for name, color in [('black', 'k'), ('red', 'r'),('gray', '0.5')]:
  PlotBarStyle.registerStyle(name, generic_generator(name, color))
"""
