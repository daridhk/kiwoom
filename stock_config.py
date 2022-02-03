import json

class StockConfig:
    """
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
        return self.init_settings(codes)
        '''
        try:
            dict_file = open('asset_setting.json', 'r')
            settings = json.load(dict_file)
            dict_file.close()
            return settings
        except:
            return self.init_settings(codes)
        '''

    def save_settings(self, asset):
        dict_file = open('asset_setting.json', 'w')
        json.dump(asset, dict_file)
        dict_file.close()
    """

    def _init_asset(self, codes):
        # read saved file
        asset = {}
        for index, code in enumerate(codes):
            asset[code] = {'index': index, 'name':'N/A', 't_budget': 10000000, 'change_yn': '.', 'sell_yn': '.', 'step':0, 't_balance':0, 'purchase_price':0, 'quantity':0, 'market_price':0, 'target_percent': 0.1, 'yield': 0, 'gostop': True, 'period': 24}
        return asset

    def _init_config(self):
        codes = ['000660', '051910', '000270', '005930']
        plans = [[3, 10], [5, 20], [7, 30], [10, 50], [15, 90]]
        leave = [5]
        asset = self._init_asset(codes)
        return codes, plans, leave, asset

    def save_config(self, codes, plans, leave, asset):
        json_file = open('config.json', 'w')
        json.dump({'codes': codes, 'plans': plans, 'leave': leave, 'asset': asset}, json_file, indent=2)
        json_file.close()
        print('save_config: save to config.json')

    def load_config(self):
        try:
            json_file = open('config.json', 'r')
            dict = json.load(json_file)
            json_file.close()
            print('load_config: load from config.json')
            return dict['codes'], dict['plans'], dict['leave'], dict['asset']
        except:
            print('load_config: init_config')
            return self._init_config()
