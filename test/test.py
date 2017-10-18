#!/usr/bin/env python3

import argparse
import os
import ssplot
import taskrun

def main(args):
  rm = taskrun.ResourceManager(
    taskrun.CounterResource('cpus', 1, args.cpus),
    taskrun.MemoryResource('mem', 3, args.mem))
  vob = taskrun.VerboseObserver(
    description=args.verbose,
    summary=True)
  cob = taskrun.FileCleanupObserver()
  tm = taskrun.TaskManager(
    resource_manager=rm,
    observers=[vob, cob],
    failure_mode=taskrun.FailureMode.ACTIVE_CONTINUE)

  do_splot = args.test == 'all' or args.test == 'splot'
  do_lplot = args.test == 'all' or args.test == 'lplot'
  do_cplot = args.test == 'all' or args.test == 'cplot'
  do_rplot = args.test == 'all' or args.test == 'rplot'

  os.system('rm -rf splots/output')
  os.system('mkdir splots/output')
  os.system('rm -rf lplots/output')
  os.system('mkdir lplots/output')
  os.system('rm -rf cplots/output')
  os.system('mkdir cplots/output')
  os.system('rm -rf rplots/output')
  os.system('mkdir rplots/output')

  ### SPLOTS ###
  if do_splot:
    # qplots
    taskrun.ProcessTask(
      tm, 'qplot_default',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       'splots/output/qplot_default.png'))
    taskrun.ProcessTask(
      tm, 'qplot_default_ns',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns '
       'splots/output/qplot_default_ns.png'))
    taskrun.ProcessTask(
      tm, 'qplot_default_ns_title',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns --title "This is a title" '
       'splots/output/qplot_default_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'qplot_12x6',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 '
       'splots/output/qplot_12x6.png'))
    taskrun.ProcessTask(
      tm, 'qplot_12x6_ns',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns '
       'splots/output/qplot_12x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'qplot_12x6_ns_title',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns --title "This is a title" '
       'splots/output/qplot_12x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'qplot_8x6',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 splots/output/qplot_8x6.png'))
    taskrun.ProcessTask(
      tm, 'qplot_8x6_ns',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns '
       'splots/output/qplot_8x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'qplot_8x6_ns_title',
      ('sslqp splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns --title "This is a title" '
       'splots/output/qplot_8x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'qplot_empty',
      ('sslqp splots/data/latency_RE_RR_1_1.00.csv.gz '
       'splots/output/qplot_empty.png'))

    # scatter
    taskrun.ProcessTask(
      tm, 'scatplot_default',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       'splots/output/scatplot_default.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_axis',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--xmin 5000 --xmax 10000 --ymin 0 --ymax 500 '
       'splots/output/scatplot_axis.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_default_ns',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns '
       'splots/output/scatplot_default_ns.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_default_ns_title',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns --title "This is a title" '
       'splots/output/scatplot_default_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_12x6',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 '
       'splots/output/scatplot_12x6.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_12x6_ns',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns '
       'splots/output/scatplot_12x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_12x6_ns_title',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns --title "This is a title" '
       'splots/output/scatplot_12x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_8x6',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 splots/output/scatplot_8x6.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_8x6_ns',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns '
       'splots/output/scatplot_8x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_8x6_ns_title',
      ('ssscat splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns --title "This is a title" '
       'splots/output/scatplot_8x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'scatplot_empty',
      ('ssscat splots/data/latency_RE_RR_1_1.00.csv.gz '
       'splots/output/scatplot_empty.png'))

    # average
    taskrun.ProcessTask(
      tm, 'aveplot_default',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       'splots/output/aveplot_default.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_axis',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--xmin 5000 --xmax 10000 --ymin 0 --ymax 500 '
       'splots/output/aveplot_axis.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_default_ns',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns '
       'splots/output/aveplot_default_ns.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_default_ns_title',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns --title "This is a title" '
       'splots/output/aveplot_default_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_12x6',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 splots/output/aveplot_12x6.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_12x6_ns',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns '
       'splots/output/aveplot_12x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_12x6_ns_title',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns --title "This is a title" '
       'splots/output/aveplot_12x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_8x6',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 splots/output/aveplot_8x6.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_8x6_ns',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns '
       'splots/output/aveplot_8x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_8x6_ns_title',
      ('ssave splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns --title "This is a title" '
       'splots/output/aveplot_8x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'aveplot_empty',
      ('ssave splots/data/latency_RE_RR_1_1.00.csv.gz '
       'splots/output/aveplot_empty.png'))

    # PDF
    taskrun.ProcessTask(
      tm, 'pdfplot_default',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       'splots/output/pdfplot_default.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_axis',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--xmin 10 --xmax 300 --ymin "-1" --ymax 1.5 '
       'splots/output/pdfplot_axis.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_default_ns',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns '
       'splots/output/pdfplot_default_ns.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_default_ns_title',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns --title "This is a title" '
       'splots/output/pdfplot_default_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_12x6',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 '
       'splots/output/pdfplot_12x6.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_12x6_ns',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns '
       'splots/output/pdfplot_12x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_12x6_ns_title',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns --title "This is a title" '
       'splots/output/pdfplot_12x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_8x6',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 '
       'splots/output/pdfplot_8x6.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_8x6_ns',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns '
       'splots/output/pdfplot_8x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_8x6_ns_title',
      ('sspdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns --title "This is a title" '
       'splots/output/pdfplot_8x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'pdfplot_empty',
      ('sspdf splots/data/latency_RE_RR_1_1.00.csv.gz '
       'splots/output/pdfplot_empty.png'))

    # CDF
    taskrun.ProcessTask(
      tm, 'cdfplot_default',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       'splots/output/cdfplot_default.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_axis',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--xmin 10 --xmax 300 --ymin "-1" --ymax 1.5 '
       'splots/output/cdfplot_axis.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_default_ns',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns '
       'splots/output/cdfplot_default_ns.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_default_ns_title',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns --title "This is a title" '
       'splots/output/cdfplot_default_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_12x6',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 '
       'splots/output/cdfplot_12x6.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_12x6_ns',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns '
       'splots/output/cdfplot_12x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_12x6_ns_title',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns --title "This is a title" '
       'splots/output/cdfplot_12x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_8x6',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 '
       'splots/output/cdfplot_8x6.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_8x6_ns',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns '
       'splots/output/cdfplot_8x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_8x6_ns_title',
      ('sscdf splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns --title "This is a title" '
       'splots/output/cdfplot_8x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'cdfplot_empty',
      ('sscdf splots/data/latency_RE_RR_1_1.00.csv.gz '
       'splots/output/cdfplot_empty.png'))

    # PERC
    taskrun.ProcessTask(
      tm, 'percplot_default',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       'splots/output/percplot_default.png'))
    taskrun.ProcessTask(
      tm, 'percplot_axis',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--xmin 10 --xmax 300 '
       'splots/output/percplot_axis.png'))
    taskrun.ProcessTask(
      tm, 'percplot_default_ns',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns '
       'splots/output/percplot_default_ns.png'))
    taskrun.ProcessTask(
      tm, 'percplot_default_ns_title',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--units ns --title "This is a title" '
       'splots/output/percplot_default_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'percplot_12x6',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 '
       'splots/output/percplot_12x6.png'))
    taskrun.ProcessTask(
      tm, 'percplot_12x6_ns',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns '
       'splots/output/percplot_12x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'percplot_12x6_ns_title',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 12x6 --units ns --title "This is a title" '
       'splots/output/percplot_12x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'percplot_8x6',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 '
       'splots/output/percplot_8x6.png'))
    taskrun.ProcessTask(
      tm, 'percplot_8x6_ns',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns '
       'splots/output/percplot_8x6_ns.png'))
    taskrun.ProcessTask(
      tm, 'percplot_8x6_ns_title',
      ('ssperc splots/data/latency_UR_RR_1_0.70.csv.gz '
       '--size 8x6 --units ns --title "This is a title" '
       'splots/output/percplot_8x6_ns_title.png'))
    taskrun.ProcessTask(
      tm, 'percplot_empty',
      ('ssperc splots/data/latency_RE_RR_1_1.00.csv.gz '
       'splots/output/percplot_empty.png'))

  ### LPLOTS ###
  if do_lplot:
    # empty plot
    empty_files = ' '.join(['lplots/data/aggregate_UR_RR_1_1.00.csv.gz'] * 21)
    taskrun.ProcessTask(tm, 'lplot_empty',
                        'ssllp lplots/output/lplot_empty.png 0 101 5 {}'
                        .format(empty_files))
    # default plots
    files_1 = ''
    files_32 = ''
    for inj in range(0, 101, 5):
      inj = '{0:.02f}'.format(inj/100)
      files_1 += ' lplots/data/aggregate_UR_RR_1_{}.csv.gz'.format(inj)
      files_32 += ' lplots/data/aggregate_UR_RR_32_{}.csv.gz'.format(inj)
    taskrun.ProcessTask(tm, 'lplot_1_default',
                        'ssllp lplots/output/lplot_1_default.png 0 101 5 {}'
                        .format(files_1))
    taskrun.ProcessTask(tm, 'lplot_32_default',
                        'ssllp lplots/output/lplot_32_default.png 0 101 5 {}'
                        .format(files_32))
    # axis
    taskrun.ProcessTask(tm, 'lplot_1_axis',
                        ('ssllp lplots/output/lplot_1_axis.png 0 101 5 '
                         '--ymin 0 --ymax 1000 {}')
                        .format(files_1))
    taskrun.ProcessTask(tm, 'lplot_32_axis',
                        ('ssllp lplots/output/lplot_32_axis.png 0 101 5 '
                         '--ymin 0 --ymax 1000 {}')
                        .format(files_32))
    # nomin
    taskrun.ProcessTask(tm, 'lplot_1_nomin',
                        ('ssllp lplots/output/lplot_1_nomin.png 0 101 5 '
                         '--nomin {}')
                        .format(files_1))
    taskrun.ProcessTask(tm, 'lplot_32_nomin',
                        ('ssllp lplots/output/lplot_32_nomin.png 0 101 5 '
                         '--nomin {}')
                        .format(files_32))
    # ns
    taskrun.ProcessTask(tm, 'lplot_1_ns',
                        ('ssllp lplots/output/lplot_1_ns.png 0 101 5 '
                         '--units ns {}')
                        .format(files_1))
    taskrun.ProcessTask(tm, 'lplot_32_ns',
                        ('ssllp lplots/output/lplot_32_ns.png 0 101 5 '
                         '--units ns {}')
                        .format(files_32))
    # title
    taskrun.ProcessTask(tm, 'lplot_1_title',
                        ('ssllp lplots/output/lplot_1_title.png 0 101 5 '
                         '--title "Single flit packets are nice" {}')
                        .format(files_1))
    taskrun.ProcessTask(tm, 'lplot_32_title',
                        ('ssllp lplots/output/lplot_32_title.png 0 101 5 '
                         '--title "Big 32 flit packets are harsh" {}')
                        .format(files_32))
    # 12x6
    taskrun.ProcessTask(tm, 'lplot_1_12x6',
                        ('ssllp lplots/output/lplot_1_12x6.png 0 101 5 '
                         '--size 12x6 {}')
                        .format(files_1))
    taskrun.ProcessTask(tm, 'lplot_32_12x6',
                        ('ssllp lplots/output/lplot_32_12x6.png 0 101 5 '
                         '--size 12x6 {}')
                        .format(files_32))
    # 6x3
    taskrun.ProcessTask(tm, 'lplot_1_6x3',
                        ('ssllp lplots/output/lplot_1_6x3.png 0 101 5 '
                         '--size 6x3 {}')
                        .format(files_1))
    taskrun.ProcessTask(tm, 'lplot_32_6x3',
                        ('ssllp lplots/output/lplot_32_6x3.png 0 101 5 '
                         '--size 6x3 {}')
                        .format(files_32))


  ### CPLOTS ###
  if do_cplot:
    for field in [None] + ssplot.LoadLatencyStats.FIELDS:
      files = ''
      labels = ''
      for style in ['AGE', 'LCL', 'RND', 'RR']:
        labels += ' --label {}'.format(style)
        for inj in range(0, 101, 5):
          inj = '{0:.02f}'.format(inj/100)
          files += (' cplots/data/aggregate_UR_{0}_32_{1}.csv.gz'
                    .format(style, inj))

      def gfield():
        if field is None:
          return ''
        else:
          return ' --field {}'.format(field)

      # default plot
      taskrun.ProcessTask(tm, 'cplot_{0}_default'.format(field),
                          ('sslcp cplots/output/cplot_{0}_default.png 0 101 5 '
                           '{1} {2}')
                          .format(field, files, gfield()))
      taskrun.ProcessTask(tm, 'cplot_{0}_default_labels'.format(field),
                          ('sslcp cplots/output/cplot_{0}_default_labels.png '
                           '0 101 5 {1} {2} {3}')
                          .format(field, files, labels, gfield()))

      # axis plot
      taskrun.ProcessTask(tm, 'cplot_{0}_axis'.format(field),
                          ('sslcp cplots/output/cplot_{0}_axis.png 0 101 5 '
                           '{1} {2} --ymin 50 --ymax 500')
                          .format(field, files, gfield()))
      taskrun.ProcessTask(tm, 'cplot_{0}_axis_labels'.format(field),
                          ('sslcp cplots/output/cplot_{0}_axis_labels.png '
                           '0 101 5 {1} {2} {3} --ymin 50 --ymax 500')
                          .format(field, files, labels, gfield()))



      # empty plot
      empty_files = ' '.join(['cplots/data/aggregate_empty.csv.gz'] * 84)
      taskrun.ProcessTask(tm, 'cplot_{0}_empty',
                          ('sslcp cplots/output/cplot_{0}_empty.png 0 101 5 '
                           '{1} {2} '
                           '--label one --label two --label three --label four')
                          .format(field, empty_files, gfield()))


  ### RPLOTS ###
  if do_rplot:
    pass


  ### RUN TASKS ###
  tm.run_tasks()

  print('\n\n#### RPLOT tests having been implemented yet ####\n\n')

if __name__ == '__main__':
  ap = argparse.ArgumentParser()
  ap.add_argument('-c', '--cpus', type=int, default=os.cpu_count(),
                  help='maximum number of cpus to use')
  ap.add_argument('-m', '--mem', type=float,
                  default=taskrun.MemoryResource.current_available_memory_gib(),
                  help='maximum amount of memory to use')

  ap.add_argument('--test', type=str, default='all',
                  choices=['all', 'splot', 'lplot', 'cplot', 'rplot'],
                  help='which plots to test')

  ap.add_argument('-v', '--verbose', action='store_true',
                  help='show all commands')

  args = ap.parse_args()
  if args.verbose:
    print(args)
  exit(main(args))
