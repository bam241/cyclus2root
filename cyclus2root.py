from cymetric import timeseries as cytim
import cymetric as cym
import ROOT
import numpy as np
import sys


def read_input(input):
    f = open(input, 'r')
    matrix = []
    for line in f:
        matrix.append(line)
    return matrix


def build_param_list(input_file):
    params = []
    input_list = read_input(input_file)
    for line in input_list:
        if line != '\n':
            params.append(get_param(line))
    return params


def get_param(line):
    (key, facilities1_, facilities2_, nucs_) = line.rstrip('\r\n').split(';')
    facilities1 = facilities1_.split(',')
    facilities2 = facilities2_.split(',')
    nucs = nucs_.split(',')
    return key, facilities1, facilities2, nucs


def build_var(parameter_list):
    global T
    T = ROOT.vector('double')()
    global P
    P = ROOT.vector('double')()
    global var
    var = []
    for i in range(len(parameter_list)):
        var.append(ROOT.vector('double')())


def main():
# Get list of output metrics
    parameter_list = build_param_list(sys.argv[1])

# Initialise variable
    build_var(parameter_list)
# Open Ttree, and branch variables
    initialize_tree()
# fill the Tree
    fill_tree(parameter_list)
# Write and Close ROOT file
    f.Write()
    f.Close()


def reset_var():
    T.clear()
    P.clear()
    for i in range(len(var)):
        var[i].clear()


def initialize_tree(file_name="tree.root", tree_name="myTTree"):

    global f, t
    global T, P, var
    f = ROOT.TFile(file_name, "recreate")
    t = ROOT.TTree(tree_name, "tree title")

    entry = np.zeros(1, dtype=int)
    t.Branch('T', T)
    t.Branch('P', P)

    for i in range(len(var)):
        bname = 'B' + str(i)
        t.Branch(bname, var[i])


def fill_tree(parameter_list):
# Loop on Cyclus DB
    global T, P, var
    file_list = [
            '/Users/mouginot/work/fcci_calculation/exo_1/cyclus.sqlite',
            '/Users/mouginot/work/fcci_calculation/exo_2/cyclus.sqlite',
            '/Users/mouginot/work/fcci_calculation/exo_3/cyclus.sqlite',
            '/Users/mouginot/work/fcci_calculation/exo_4/cyclus.sqlite']
    for file_name in file_list:
        db = cym.dbopen(file_name)
        evaler = cym.Evaluator(db=db, write=False)
# Reset Variables
        reset_var()
        T += evaler.eval('TimeList')['TimeStep'].tolist()
        P += cytim.get_power(evaler)['Value'].tolist()
# Read variable
        print(file_name)
        for i, parameter in enumerate(parameter_list):
            var[i].clear()
            val = get_val(evaler, parameter)
            var[i] += val
# Update Ttree
        t.Fill()
# Close cyclus DB
        db.close()
        del evaler


def get_val(ev, parameter):
    key = parameter[0]
    for i in range(len(parameter))[1:]:
        if parameter[i] == ['']: parameter[i][:] = []
    fac1 = parameter[1]
    fac2 = parameter[2]
    nucs = parameter[3]

    if key == "inv":
        return cytim.inventories(ev, facilities=parameter[1], nucs=parameter[3])['Quantity']
    if key == "trans":
        return cytim.transactions(ev, senders=parameter[1], receivers=parameter[2], nucs=parameter[3])['Mass']

main()
