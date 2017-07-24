import pandas as pd
from Code.config import get_path

pd.set_option('display.width', 320)




def main():

    path = get_path()  # File path to data store
    # sessions = pd.DataFrame(pd.read_csv(path+'/Cleaned/sessions.csv'))
    # df = sessions
    #
    # df2 = df['Talk Title'].str.split(',', 1)
    #
    # print df2.ix[0:20]
    # #
    # # names = []
    # # for i in range(len(df2)):
    # #     names.append(df2.ix[i][0])
    # #
    # # print names


    favs = pd.DataFrame(pd.read_csv(path+'/favs.csv'))
    speakers = pd.DataFrame(pd.read_csv(path+'/speakers.csv'))

    print favs.merge(speakers, how='inner', on='Seminar')



if __name__ == '__main__':
    main()