import os

def get_path():
    """
    This simple function returns the path to the data directory, which sits
    at the same level as the src directory. This allows access to data files
    using the same commands within different subdirectories.
    :return:
    """

    print "Which project are you interested in: [Cannes, SpringAutumnFair]"
    project = raw_input()

    root_path = os.path.dirname(os.path.abspath(__file__+'../../'))
    PATH = root_path+'/Projects/%s/Data/' % project
    if PATH.endswith('/Data'):
        return PATH
    else:
        print 'Path to data source not found. Check documentation for correct structure. \n'