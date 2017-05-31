import os


def get_pwd():
    return 'EvMs8900'


def get_path():
    """
    This simple function returns the path to the data directory, which sits
    at the same level as the src directory. This allows access to data files
    using the same commands within different subdirectories.
    :return:
    """

    print 'Which data do you want?:\nCannes: [1]\nSpring Fair: [2]\nTracking: [3]\n'
    source = raw_input()
    if source == '1':
        project = 'Cannes'
    elif source == '2':
        project = 'SpringAutumnFair'
    elif source == '3':
        print 'Which tracking data?:\nWiFi: [1]\nBLE: [2]\n'
        wifi_or_ble = raw_input()
        if wifi_or_ble == '1':
            project = 'Tracking/WiFi'
        elif wifi_or_ble == '2':
            project = 'Tracking/BLE'
        else:
            print "Project not recognised, please try again... \n"
            project = ''
            get_path()
    else:
        print "Project not recognised, please try again... \n"
        project = ''
        get_path()

    root_path = os.path.dirname(os.path.abspath(__file__+'../../'))
    PATH = root_path+'/Projects/%s/Data' % project
    if PATH.endswith('/Data'):
        return PATH
    else:
        print 'Path to data source not found. Check documentation for correct structure. \n'