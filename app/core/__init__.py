import os

work_dir = os.getcwd()

def export_results(result):
    """
    Empty results file and write new results to it
    """
    res_file = open(work_dir + "\\results.txt", "w")
    res_file.close()
    with open("results.txt", "w") as results_file:
        results_file.write(result)


def beautify_results():
    """
    Generates list of list for pandas.DataFrame
    """
    with open(work_dir + "\\results.txt", "r") as results_file:
        file_content = results_file.readlines()
    del file_content[0]
    values_list_of_list = []
    for line in file_content:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        values_list_of_list.append(line_list)
    return values_list_of_list
    