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

    root_path = os.path.dirname(os.path.abspath(__file__ + '../../'))

    print 'Which data do you want?:\nCannes: [1]\nSpring Fair: [2]\nTracking: [3]\nM2020Europe: [4]\n'
    source = raw_input()

    if source == '1':
        print 'Which Project?:\nApp: [1]\nFootfall: [2]\nFootfall: [3]\nBraindate: [4]\nFringe: [5]\nHotel: [6]\n'
        project = raw_input()
        if project == '1':
            return root_path + '/Projects/Tracking/WiFi'
        elif wifi_or_ble == '2':
            return root_path + '/Projects/Tracking/BLE'
        else:
            print "Project not recognised, please try again... \n"
            return get_path()
        return root_path+'/Projects/Cannes/Data'
    elif source == '2':
        return root_path+'/Projects/SpringAutumnFair/Data'
    elif source == '3':
        print 'Which tracking data?:\nWiFi: [1]\nBLE: [2]\n'
        wifi_or_ble = raw_input()
        if wifi_or_ble == '1':
            return root_path+'/Projects/Tracking/WiFi'
        elif wifi_or_ble == '2':
            return root_path+'/Projects/Tracking/BLE'
        else:
            print "Project not recognised, please try again... \n"
            return get_path()
    elif source == '4':
        return root_path + '/Projects/M2020/Europe/Data'
    else:
        print "Project not recognised, please try again... \n"
        return get_path()

