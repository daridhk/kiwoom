import json



class StockConfig:
    def get_codes(self):
        # return ['002360', '001440', '001510']
        return ['000660', '051910', '000270', '005930']

    def init_settings(self, codes):
        # read saved file
        asset = {}
        for index, code in enumerate(codes):
            asset[code] = {'index': index, 'name':'N/A', 't_budget': 10000000, 'step':0, 't_balance':0, 'purchase_price':0, 'quantity':0, 'market_price':0, 'target_percent': 0.1, 'yield': 0, 'gostop': True, 'period': 24}
        return asset

    def load_settings(self, codes):
        try:
            dict_file = open('asset_setting.json', 'r')
            settings = json.load(dict_file)
            dict_file.close()
            return settings
        except:
            return self.init_settings(codes)

    def save_settings(self, asset):
        dict_file = open('asset_setting.json', 'w')
        json.dump(asset, dict_file)
        dict_file.close()