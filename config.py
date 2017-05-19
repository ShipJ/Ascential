import os

def get_path():
    """
    This simple function returns the path to the data directory, which sits
    at the same level as the src directory. This allows access to data files
    using the same commands within different subdirectories.
    :return:
    """
    root_path = os.path.dirname(os.path.abspath(__file__+'../../'))
    PATH = root_path+'/Projects'
    if PATH.endswith('/Projects'):
        return PATH
    else:
        print 'Path to data source not found. Check documentation for correct structure. \n'