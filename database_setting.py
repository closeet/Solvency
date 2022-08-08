import pickle


def serialize(ls, filename):
    with open(filename, 'wb') as file:
        pickle.dump(ls, file)


def deserialize(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


ls_setting_asset = deserialize('setting_asset')
db_database_asset = ls_setting_asset[3]
ls_setting_solvency = deserialize('setting_solvency')
db_database_solvency = ls_setting_solvency[3]
