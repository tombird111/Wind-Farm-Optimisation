import wfo

def print_menu():
    print("Enter a number to run the specified test:")
    print("1. Basic functionality test")
    print("2. Mutation test")
    print("3. Crossover test")
    print("4. Parents kept test")
    print("5. Precision test")
    print("6. All tests")

def append_data(testname, data, note = ""):
    f = open(("Results\\" + testname + ".txt"), "a")
    f.write("!New test: " + note + "\n")
    for i in range(1, len(data[2]) + 1): #For every entry
        txt = "{0},{1}\n"
        data_string = txt.format(i, data[2][i])
        f.write(data_string) #Write generation,fitness then a newline
    txt = "#Best solution: {0} with fitness: {1} \n"
    data_string = txt.format(data[0], data[1])
    f.write(data_string)
    f.close()
    
def test_one():
    #Standard test
    print("Beginning test one")
    append_data("basetest", wfo.run_test(seed = 1))
    append_data("basetestc", wfo.run_test(seed = 1, constant_ws = True))
    print("Finished test one")
    
def test_mut():
    #Test mutations
    mutations = [0.05, 0.2, 0.3]
    print("Beginning mutation test")
    for mutation in mutations:
        append_data("muttest", wfo.run_test(seed = 1, mutation_ratio=mutation), ("Mutation = {}".format(mutation)))
        append_data("muttestc", wfo.run_test(seed = 1, constant_ws = True, mutation_ratio=mutation), ("Mutation = {}".format(mutation)))
    print("Finished mutation test")
    
def test_crossover():
    #Test crossover
    print("Beginning crossover test")
    crossovers = ["single_point", "uniform"]
    for crossover in crossovers:
        append_data("crosstest", wfo.run_test(seed = 1, crossover_type=crossover), ("Crossover = {}".format(crossover)))
        append_data("crosstestc", wfo.run_test(seed = 1, constant_ws = True, crossover_type=crossover), ("Crossover = {}".format(crossover)))
    print("Finished crossover test")
    
def test_parents():
    #Test parents
    print("Beginning parents kept test")
    parents = [0.95, 0.8, 0.7]
    for parent in parents:
        append_data("parenttest", wfo.run_test(seed = 1, keep_parents_ratio=parent), ("Parents = {}".format(parent)))
        append_data("parenttestc", wfo.run_test(seed = 1, constant_ws = True, keep_parents_ratio=parent), ("Parents = {}".format(parent)))
    print("Finished parents kept test")
    
def test_precision():
    #Test precision
    print("Beginning precision test")
    precisions = [500, 250, 100]
    for precision in precisions:
        append_data("prectest", wfo.run_test(seed = 1, precision=precision), ("Precision = {}".format(precision)))
        append_data("prectestc", wfo.run_test(seed = 1, constant_ws = True, precision=precision), ("Precision = {}".format(precision)))
    print("Finished precision test")

def test_all():
    print("Beginning all tests")
    test_crossover()
    test_mut()
    test_one()
    test_parents()
    test_precision()
    print("All tests concluded")

print_menu()
exit_input = False
while exit_input == False:
    test_num = input()
    try:
        test_num = int(test_num)
    except:
        if test_num != "q":
            print("Bad input")
    match test_num:
        case 1:
            test_one()
        case 2:
            test_mut()
        case 3:
            test_crossover()
        case 4:
            test_parents()
        case 5:
            test_precision()
        case 6:
            test_all()
        case _:
            exit_input = True