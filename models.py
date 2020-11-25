from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Kengo Suzuki'

doc = """
Resource reproduction game
"""


class Constants(BaseConstants):
    name_in_url = 'resource_reproduction_9'
    players_per_group = None
    num_rounds = 100
    pool_start = 500
    max_exploitation = 5
    reproduction_rate = 2

    max_bassai_suru = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        group_matrix = []
        players = self.get_players()
        ppg = self.session.config['players_per_group']
        for i in range(0, len(players), ppg):
            group_matrix.append(players[i:i+ppg])
        self.set_group_matrix(group_matrix)

    def vars_for_admin_report(self):
        num_rounds = self.round_number  # 現在のラウンド数
        exploitation = [p.exploitation for p in self.get_players()]
        bassai_suru = [p.bassai_suru for p in self.get_players()] #フジノ追記
        resources = [p.resource for p in self.get_players()]
        game = self.get_groups()[0]

        print('game is', game)  # デバッグ用

        ## current_pool を出力する List を作成
        pname = 'current_pool'  # プレイヤー名の文字列
        pdata = []  # データ格納用のリスト
#        pdata.append(self.session.config['pool_start'])
        for j in range(num_rounds-1):  # 1ラウンド目から直前のラウンドまでについて
            pdata.append(game.in_round(j + 1).current_pool)  # pdata リストに値を追加
        List_current_pool = [{'name': pname, 'data': pdata}]  # プレイヤー毎のリストを作成

        print('current_pool is', List_current_pool)  # デバッグ用

        return dict(
            exploitation = exploitation,
            bassai_suru = bassai_suru, #藤野追記
            resources = resources,
            List_current_pool = List_current_pool
        )



class Group(BaseGroup):

    total_exploitation = models.IntegerField(
        initial = 0
    )
    total_bassai_suru = models.IntegerField(
        initial = 0
    )
    current_pool = models.IntegerField()
    resource_outage = models.BooleanField(
        initial = False
    )
    timeout = models.BooleanField(
        initial = False
    )

    def data_update(self):
        players = self.get_players()    # Get list of players
        if self.round_number != 1:
            self.total_exploitation = self.in_round(self.round_number - 1).total_exploitation
            self.total_bassai_suru = self.in_round(self.round_number - 1).total_bassai_suru
            self.current_pool = self.in_round(self.round_number-1).current_pool
            for p in players:
                p.exploitation = p.in_round(self.round_number - 1).exploitation
                #p.total_bassai_suru = self.in_round(self.round_number - 1).total_bassai_suru
                p.resource = p.in_round(self.round_number - 1).resource
        else:
            self.current_pool = self.session.config['pool_start']

        resource_check = [p.resource for p in players]  # デバッグ用

        print('players is', players)  # デバッグ用
        print('total_exploitation is', self.total_exploitation)  # デバッグ用
        print('current_pool is', self.current_pool)  # デバッグ用
        print('resource_check is', resource_check)  # デバッグ用
        print('total_bassai_suru is', self. total_bassai_suru)  # デバッグ用 藤野追加

    def resource_update(self):

        # Get list of players
        players = self.get_players()

        # Calculate total exploitation by all players
        exploitations = [p.exploitation for p in players]
        self.total_exploitation = sum(exploitations)

        # Calculate total bassai_suru by all players
        bassai_surus = [p.bassai_suru for p in players]
        self.total_bassai_suru = sum(bassai_surus)

        # Check the outage of common pool
        if self.total_exploitation >= self.current_pool:
            self.resource_outage = True
        # update the common pool
            self.current_pool = self.current_pool-self.total_exploitation

        # If not outage,
        # (1) update the common pool
        else:
            self.current_pool = (self.current_pool-self.total_exploitation)*Constants.reproduction_rate
            if self.current_pool > self.session.config['pool_start']:
                self.current_pool = self.session.config['pool_start']
        # (2) update the resources of players
            for p in players:
                p.resource = p.resource + p.exploitation
        # (3) check timeout
            if self.round_number == self.session.config['num_rounds']:
                self.timeout = True



class Player(BasePlayer):
    exploitation = models.IntegerField(
        initial=0,
        min = 0,
        max = Constants.max_exploitation,
    )
    bassai_suru = models.IntegerField(
        initial=0,
        min = 0,
        max = Constants.max_bassai_suru,
    )
    resource = models.IntegerField(
        initial = 0
    )

def custom_export(players):
    # header row
    yield ['group','round_number', 'id_in_group','exploitation','bassai_suru', ' resource']
    for p in players:
        yield [p.group.id_in_subsession, p.round_number, p.id_in_group, p.exploitation, p.bassai_suru, p. resource]
