import os

def get_path():
    """
    This simple function returns the path to the data directory, which sits
    at the same level as the src directory. This allows access to data files
    using the same commands within different subdirectories.
    :return:
    """

    print 'Which project are you interested in:\nCannes: [1]\nSpring Fair: [2]'
    r = raw_input()
    if r == 1:
        project = 'Cannes'
    elif r == 2:
        project = 'SpringAutumnFair'
    else:
        print "Project not recognised, please try again... \n"
        project = ''
        get_path()

    root_path = os.path.dirname(os.path.abspath(__file__+'../../'))
    PATH = root_path+'/Projects/%s/Data/' % project
    if PATH.endswith('Data/'):
        return PATH
    else:
        print 'Path to data source not found. Check documentation for correct structure. \n'