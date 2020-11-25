from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
# import csv    # csvファイルの読み書きに必要，自分で書き足すこと
# import pandas as pd
# import json



class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict(
            players_per_group = self.session.config['players_per_group'],
            num_rounds = self.session.config['num_rounds'],
            pool_start = self.session.config['pool_start'],
        )



class ResultsWaitPage1(WaitPage):
    after_all_players_arrive = 'data_update'



class Exploit1(Page):
    form_model = 'player'
    form_fields = ['exploitation','bassai_suru']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        name_in_url = self.participant.code
        return dict(
            name_in_url = name_in_url,
            pool_start = self.session.config['pool_start'],
        )



class Exploit2(Page):

    form_model = 'player'
    form_fields = ['exploitation','bassai_suru']

    timeout_seconds = 60

    def is_displayed(self):
        return self.round_number != 1

    def vars_for_template(self):

        return dict(
            round_number = self.round_number,
            common_pool = self.group.in_round(self.round_number - 1).current_pool,
        )

    def js_vars(self): # Result クラスの同名の関数とは微妙に違うので注意
        ## 配列の作成に必要な定数をローカルに作成
        num_rounds = self.round_number              # 現在のラウンド数
        players = self.group.get_players()          # すべてのプレイヤーのリスト
        # num_players = Constants.players_per_group   # プレイヤーの人数

        ## resource を出力する List を作成（形式は List_exploitation と同じ）
        List_resource = []
        for p in players:          # リストに含まれるプレイヤーについて
            id = p.id_in_group     # id を取得
            pname = 'Player' + str(id)  # プレイヤー名の文字列
            pdata = []                  # データ格納用のリスト
            for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                pdata.append(p.in_round(j+1).resource)  # pdata リストに値を追加
            pdict = {'name':pname,'data':pdata}    # プレイヤー毎のリストを作成
            List_resource.append(pdict)

        ## current_pool を出力する List を作成（形式は total_exploitation と同じ）
        pname = 'current_pool'  # プレイヤー名の文字列
        pdata = []                  # データ格納用のリスト
#        pdata.append(self.session.config['pool_start'])
        for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
            pdata.append(self.group.in_round(j+1).current_pool)  # pdata リストに値を追加
        List_current_pool = [{'name':pname,'data':pdata}]    # プレイヤー毎のリストを作成

        print('List_resource is', List_resource)  # デバッグ用
        print('List_current_pool is', List_current_pool)  # デバッグ用

        return dict(
        num_rounds = self.session.config['num_rounds'],
        List_resource=List_resource,
        List_current_pool=List_current_pool,
        )



class ResultsWaitPage2(WaitPage):
    after_all_players_arrive = 'resource_update'



class Results(Page): # Exploit2 クラスの同名の関数とは微妙に違うので注意
    def is_displayed(self):
        return self.group.resource_outage == False and self.group.timeout == False



class GameOver1(Page):
    def is_displayed(self):
        return self.group.resource_outage == False and self.group.timeout == True

    def js_vars(self): # Result クラスの同名の関数とは微妙に違うので注意
        ## 配列の作成に必要な定数をローカルに作成
        num_rounds = self.round_number              # 現在のラウンド数
        players = self.group.get_players()          # すべてのプレイヤーのリスト

        ## exploitation を出力する List を作成
        List_exploitation = []
        for p in players:          # リストに含まれるプレイヤーについて
            id = p.id_in_group     # id を取得
            pname = 'Player' + str(id)  # プレイヤー名の文字列
            pdata = []                  # データ格納用のリスト
            if num_rounds > 1:
                for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                    pdata.append(p.in_round(j+1).exploitation)  # pdata リストに値を追加
            pdata.append(p.exploitation)  # 現在のラウンドについて pdata リストに値を追加
            pdict = {'name':pname,'data':pdata}    # プレイヤー毎のリストを作成
            List_exploitation.append(pdict)

        ## bassai_suru を出力する List を作成
        List_bassai_suru = []
        for p in players:          # リストに含まれるプレイヤーについて
            id = p.id_in_group     # id を取得
            pname = 'Player' + str(id)  # プレイヤー名の文字列
            pdata = []                  # データ格納用のリスト
            if num_rounds > 1:
                for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                    pdata.append(p.in_round(j+1).bassai_suru)  # pdata リストに値を追加
            pdata.append(p.bassai_suru)  # 現在のラウンドについて pdata リストに値を追加
            pdict = {'name':pname,'data':pdata}    # プレイヤー毎のリストを作成
            List_bassai_suru.append(pdict)

        ## resource を出力する List を作成
        List_resource = []
        for p in players:          # リストに含まれるプレイヤーについて
            id = p.id_in_group     # id を取得
            pname = 'Player' + str(id)  # プレイヤー名の文字列
            pdata = []                  # データ格納用のリスト
            if num_rounds > 1:
                for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                    pdata.append(p.in_round(j+1).resource)  # pdata リストに値を追加
            pdata.append(p.resource)  # 現在のラウンドについて pdata リストに値を追加
            pdict = {'name':pname,'data':pdata}    # プレイヤー毎のリストを作成
            List_resource.append(pdict)

        ## total_exploitation を出力する List を作成
        pname = 'total_exploitation'  # プレイヤー名の文字列
        pdata = []                  # データ格納用のリスト
        if num_rounds >1:
            for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                pdata.append(self.group.in_round(j+1).total_exploitation)  # pdata リストに値を追加
        pdata.append(self.group.total_exploitation)  # 現在のラウンドについて pdata リストに値を追加
        List_total_exploitation = [{'name':pname,'data':pdata}]    # プレイヤー毎のリストを作成

        ## total_bassai_suru を出力する List を作成
        pname = 'total_bassai_suru'  # プレイヤー名の文字列
        pdata = []                  # データ格納用のリスト
        if num_rounds >1:
            for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                pdata.append(self.group.in_round(j+1).total_bassai_suru)  # pdata リストに値を追加
        pdata.append(self.group.total_bassai_suru)  # 現在のラウンドについて pdata リストに値を追加
        List_total_bassai_suru = [{'name':pname,'data':pdata}]    # プレイヤー毎のリストを作成

        ## current_pool を出力する List を作成
        pname = 'current_pool'  # プレイヤー名の文字列
        pdata = []                  # データ格納用のリスト
        if num_rounds >1:
            for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                pdata.append(self.group.in_round(j+1).current_pool)  # pdata リストに値を追加
        pdata.append(self.group.current_pool)  # 現在のラウンドについて pdata リストに値を追加
        List_current_pool = [{'name':pname,'data':pdata}]    # プレイヤー毎のリストを作成

        return dict(
        num_rounds = self.session.config['num_rounds'],
        List_exploitation=List_exploitation,
        List_bassai_suru=List_bassai_suru,
        List_resource=List_resource,
        List_total_exploitation=List_total_exploitation,
        List_total_bassai_suru=List_total_bassai_suru,
        List_current_pool=List_current_pool,
        )



class GameOver2(Page):
    def is_displayed(self):
        return self.group.resource_outage == True

    def js_vars(self): # Result クラスの同名の関数とは微妙に違うので注意
        ## 配列の作成に必要な定数をローカルに作成
        num_rounds = self.round_number              # 現在のラウンド数
        players = self.group.get_players()          # すべてのプレイヤーのリスト

        ## exploitation を出力する List を作成
        List_exploitation = []
        for p in players:          # リストに含まれるプレイヤーについて
            id = p.id_in_group     # id を取得
            pname = 'Player' + str(id)  # プレイヤー名の文字列
            pdata = []                  # データ格納用のリスト
            if num_rounds > 1:
                for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                    pdata.append(p.in_round(j+1).exploitation)  # pdata リストに値を追加
            pdata.append(p.exploitation)  # 現在のラウンドについて pdata リストに値を追加
            pdict = {'name':pname,'data':pdata}    # プレイヤー毎のリストを作成
            List_exploitation.append(pdict)

        ## bassai_suru を出力する List を作成
        List_bassai_suru = []
        for p in players:          # リストに含まれるプレイヤーについて
            id = p.id_in_group     # id を取得
            pname = 'Player' + str(id)  # プレイヤー名の文字列
            pdata = []                  # データ格納用のリスト
            if num_rounds > 1:
                for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                    pdata.append(p.in_round(j+1).bassai_suru)  # pdata リストに値を追加
            pdata.append(p.bassai_suru)  # 現在のラウンドについて pdata リストに値を追加
            pdict = {'name':pname,'data':pdata}    # プレイヤー毎のリストを作成
            List_bassai_suru.append(pdict)

        ## resource を出力する List を作成
        List_resource = []
        for p in players:          # リストに含まれるプレイヤーについて
            id = p.id_in_group     # id を取得
            pname = 'Player' + str(id)  # プレイヤー名の文字列
            pdata = []                  # データ格納用のリスト
            if num_rounds > 1:
                for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                    pdata.append(p.in_round(j+1).resource)  # pdata リストに値を追加
            pdata.append(p.resource)  # 現在のラウンドについて pdata リストに値を追加
            pdict = {'name':pname,'data':pdata}    # プレイヤー毎のリストを作成
            List_resource.append(pdict)

        ## total_exploitation を出力する List を作成
        pname = 'total_exploitation'  # プレイヤー名の文字列
        pdata = []                  # データ格納用のリスト
        if num_rounds >1:
            for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                pdata.append(self.group.in_round(j+1).total_exploitation)  # pdata リストに値を追加
        pdata.append(self.group.total_exploitation)  # 現在のラウンドについて pdata リストに値を追加
        List_total_exploitation = [{'name':pname,'data':pdata}]    # プレイヤー毎のリストを作成

        ## total_bassai_suru を出力する List を作成
        pname = 'total_bassai_suru'  # プレイヤー名の文字列
        pdata = []                  # データ格納用のリスト
        if num_rounds >1:
            for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                pdata.append(self.group.in_round(j+1).total_bassai_suru)  # pdata リストに値を追加
        pdata.append(self.group.total_bassai_suru)  # 現在のラウンドについて pdata リストに値を追加
        List_total_bassai_suru = [{'name':pname,'data':pdata}]    # プレイヤー毎のリストを作成

        ## current_pool を出力する List を作成
        pname = 'current_pool'  # プレイヤー名の文字列
        pdata = []                  # データ格納用のリスト
        if num_rounds >1:
            for j in range(num_rounds-1): # 1ラウンド目から直前のラウンドまでについて
                pdata.append(self.group.in_round(j+1).current_pool)  # pdata リストに値を追加
        pdata.append(self.group.current_pool)  # 現在のラウンドについて pdata リストに値を追加
        List_current_pool = [{'name':pname,'data':pdata}]    # プレイヤー毎のリストを作成

        return dict(
        num_rounds = self.session.config['num_rounds'],
        List_exploitation=List_exploitation,
        List_bassai_suru=List_bassai_suru,
        List_resource=List_resource,
        List_total_exploitation=List_total_exploitation,
        List_total_bassai_suru=List_total_bassai_suru,
        List_current_pool=List_current_pool,
        )



page_sequence = [
    Introduction,
    ResultsWaitPage1,
    Exploit1,
    Exploit2,
    ResultsWaitPage2,
    GameOver1,
    GameOver2
]
