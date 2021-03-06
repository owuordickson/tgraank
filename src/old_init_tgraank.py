# -*- coding: utf-8 -*-
"""
@author: "Dickson Owuor"
@credits: "Joseph Orero and Anne Laurent,"
@license: "MIT"
@version: "2.0"
@email: "owuordickson@gmail.com"
@created: "19 November 2019"

Usage:
    $python3 init_tgraank.py -f ../data/DATASET.csv -c 0 -s 0.5 -r 0.5 -p 1

Description:
    f -> file path (CSV)
    c -> reference column
    s -> minimum support
    r -> representativity

"""

import sys
from optparse import OptionParser
from algorithms.common.handle_data import HandleData
from algorithms.tgraank.t_graank_v1 import Tgrad
from src.algorithms.common.profile_cpu import Profile


def init_algorithm(f_path, refItem, minSup, minRep, allowPara, eq=False):
    try:
        wr_line = ""
        d_set = HandleData(f_path)
        if d_set.data:
            titles = d_set.title
            d_set.init_attributes(eq)
            tgp = Tgrad(d_set, refItem, minSup, minRep, allowPara)
            if allowPara >= 1:
                msg_para = "True"
                list_tgp = tgp.run_tgraank(parallel=True)
            else:
                msg_para = "False"
                list_tgp = tgp.run_tgraank()
            #list_tgp = list(filter(bool, list_tgp))
            #if len(list_tgp) > 5:
            #    list_tgp.sort(key=lambda k: (k[0][0], k[0][1]), reverse=True)

            wr_line = "Algorithm: T-GRAANK \n"
            wr_line += "No. of (dataset) attributes: " + str(d_set.column_size) + '\n'
            wr_line += "No. of (dataset) tuples: " + str(d_set.size) + '\n'
            wr_line += "Minimum support: " + str(minSup) + '\n'
            wr_line += "Minimum representativity: " + str(minRep) + '\n'
            wr_line += "Multi-core execution: " + str(msg_para) + '\n'
            wr_line += "Number of cores: " + str(tgp.cores) + '\n'
            wr_line += "Number of tasks: " + str(tgp.max_step) + '\n\n'
            for txt in titles:
                col = int(txt[0])
                if col == refItem:
                    wr_line += (str(txt[0]) + '. ' + str(txt[1]) + '**' + '\n')
                else:
                    wr_line += (str(txt[0]) + '. ' + str(txt[1]) + '\n')

            wr_line += str("\nFile: " + f_path + '\n')
            wr_line += str("\nPattern : Support" + '\n')

            for obj in list_tgp:
                if obj:
                    for i in range(len(obj[0])):
                        wr_line += (str(obj[0][i]) + ' : ' + str(obj[1][i]) +
                                    ' | ' + obj[2][i].to_string() + '\n')
        return wr_line
    except Exception as error:
        wr_line = "Failed: " + str(error)
        print(error)
        return wr_line


if __name__ == "__main__":
    if not sys.argv:
        # pType = sys.argv[1]
        file_path = sys.argv[1]
        ref_col = sys.argv[2]
        min_sup = sys.argv[3]
        min_rep = sys.argv[4]
        allow_p = sys.argv[5]
    else:
        optparser = OptionParser()
        optparser.add_option('-f', '--inputFile',
                             dest='file',
                             help='path to file containing csv',
                             # default=None,
                             # default='../data/DATASET2.csv',
                             default='../data/rain_temp2013-2015.csv',
                             # default='../data/Directio.csv',
                             type='string')
        optparser.add_option('-c', '--refColumn',
                             dest='refCol',
                             help='reference column',
                             default=1,
                             type='int')
        optparser.add_option('-s', '--minSupport',
                             dest='minSup',
                             help='minimum support value',
                             default=0.5,
                             type='float')
        optparser.add_option('-r', '--minRepresentativity',
                             dest='minRep',
                             help='minimum representativity',
                             default=0.5,
                             type='float')
        optparser.add_option('-p', '--allowMultiprocessing',
                             dest='allowPara',
                             help='allow multiprocessing',
                             default=1,
                             type='int')
        (options, args) = optparser.parse_args()
        inFile = None
        if options.file is None:
            print('No data-set filename specified, system with exit')
            print("Usage: $python3 init_tgraank.py -f filename.csv -c refColumn -s minSup  -r minRep")
            sys.exit('System will exit')
        else:
            inFile = options.file
        file_path = inFile
        ref_col = options.refCol
        min_sup = options.minSup
        min_rep = options.minRep
        allow_p = options.allowPara

    import time
    # import tracemalloc

    start = time.time()
    # tracemalloc.start()
    res_text = init_algorithm(file_path, ref_col, min_sup, min_rep, allow_p)
    # snapshot = tracemalloc.take_snapshot()
    end = time.time()

    wr_text = ("Run-time: " + str(end - start) + " seconds\n")
    # wr_text += (Profile.get_quick_mem_use(snapshot) + "\n")
    wr_text += str(res_text)
    f_name = str('res_temp' + str(end).replace('.', '', 1) + '.txt')
    HandleData.write_file(wr_text, f_name)
    print(wr_text)
