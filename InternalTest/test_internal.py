"""
共通API内部テスト用テストコード

[テスト内容]
    本テストでは、lambda_handlerをAPI毎に対応したpathで呼び出し、
    正常/異常なパラメータを使ってテストを行うことで
    ・仮想リソース層のカバレッジ率の測定
    ・デグレの早期発見
    を行う

事前準備・環境構築:
    pytestをインストールしておく事。

変更方法
    詳細な手順については "API内部テストのガイドライン.pptx" と下方のコメントを参照する事。

    1. API: /[Resource]の単位で下方のテスト関数群に
        test_XXXX_lambda_handlerを追加する。
        XXXXは追加する[Resource]名に対応。
        ※ 新しいリソースのテストを追加する場合は、test_OperationTime_lambda_handlerをコピーして作成
    2. API毎にtest_XXXX_lambda_handlerのテスト条件を@pytest.mark.parametrizeに追加する
        追加方法は下方に記載
    3. pytestを実行する。

補足
    カバレッジ率を上げる場合にはHTTPリクエストのパラメータ部分を設定しているPARAM_CHOICESからテスト条件を選んで、
    対応する仮想リソースのtest_XXXX_lambda_handlerの@pytest.mark.parametrizeに追加する。
    テスト条件が不足している場合は、PARAM_CHOICESを追加する。
"""
import datetime
import pytest
import sys

today_start = int(datetime.date.today().strftime('%Y%m%d000000'))
today_end = int(datetime.date.today().strftime('%Y%m%d235959'))


"""
---------------------------------------------------
# テストで使用するHTTPリクエストのパラメータ設定場所
---------------------------------------------------
"""
"""
REQUEST_EVENT
Lambda_handlerが受け取るテスト用のHTTPリクエストのひな型
テスト時は'path'と'multiValueQueryStringParameters'に各テスト条件の値が入ってくる
変更は不要
"""
REQUEST_EVENT = {
    'path': None,
    'headers': {
        'Authorization': 'eyJraWQiOiJ6eEQ2OVZTY3Y0ZDA1dWpjcGhPMzhjYWQwd24xZ2N2V3F6TzVkZXlrM013PSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI4ZWU1MGJmYS01OTdjLTQ2Y2YtOTE1NC0xMjE5MzlhYmRjNGIiLCJjdXN0b206c25zX3RvcGljIjoic25zX3RvcGljX2lzdG9rdXNoaW1hIiwiY3VzdG9tOmxpbmVzIjoi5be75Y-W6KOF572u77yRLOW3u-WPluijhee9ru-8kizlt7vlj5boo4Xnva7vvJMs5be75Y-W6KOF572u77yULOW3u-WPluijhee9ru-8lSzlt7vlj5boo4Xnva7vvJYs5be75Y-W6KOF572u77yXLOW3u-WPlljnt5rmpJzmn7ss5be75Y-W44K544OI44OD44KrLOOCv-ODluabsuOBkizosqDmpbXntbbnuIHmnb9cL-e8tuaMv-WFpSznvLbntZ7jgoos57y25bqV6LaF6Z-z5rOiLOe8tuW6lea6tuaOpVwv44OU44Oz5oy_5YWlXC_mraPmpbXntbbnuIHmnb8s5rqd5YWl44KMKFJTR--8iSzjgqzjgrnjgrHjg4Pjg4jvvIhSQ0fvvIks5bCB5Y-j5L2T5rq25o6lLOODkeODrOOCv-OCpOOCtuODvCzlsIHlj6PkvZPmurbmjqUo776a772w7727776e772wKSzliY3ph43ph4_muKzlrpos5LqI5YKZ5Yqg54ax44Kz44Oz44OZ44KiLOacrOazqOa2su-8kSzmnKzms6jmtrLvvJIs5pys5rOo5ray77yTLOacrOazqOa2su-8lCzmnKzms6jmtrLvvJUs5pys5rOo5ray77yWLOacrOazqOa2su-8lyzjg5Hjg6zjg4Pjg4jmtJfmtYQsR05DLOi_veOBhOazqOa2sizku67lsIHlj6Pjg7vlvozph43lgbQs5bCB5Y-j77yI44OX44Os44K577yJLOa0l-a1hCxWb-ODu0lS5qSc5p-7LOWkluims-aknOafuyzjg5Hjg6zjg4Pjg4joqbDjgoEiLCJjdXN0b206bWVudSI6IklTdG9rdXNoaW1hIiwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLW5vcnRoZWFzdC0xX0UzN0tPZDk3biIsImN1c3RvbTp3b3JrX2VuZCI6IjI0OjAwIiwiY3VzdG9tOmZsb3dsaW5lIjoi5be75Y-W6KOF572u77yRLOW3u-WPluijhee9ru-8kizlt7vlj5boo4Xnva7vvJMs5be75Y-W6KOF572u77yULOW3u-WPluijhee9ru-8lSzlt7vlj5boo4Xnva7vvJYs5be75Y-W6KOF572u77yXLOW3u-WPlljnt5rmpJzmn7ss5be75Y-W44K544OI44OD44KrLOOCv-ODluabsuOBkizosqDmpbXntbbnuIHmnb9cL-e8tuaMv-WFpSznvLbntZ7jgoos57y25bqV6LaF6Z-z5rOiLOe8tuW6lea6tuaOpVwv44OU44Oz5oy_5YWlXC_mraPmpbXntbbnuIHmnb8s5rqd5YWl44KMKFJTR--8iSzjgqzjgrnjgrHjg4Pjg4jvvIhSQ0fvvIks5bCB5Y-j5L2T5rq25o6lLOODkeODrOOCv-OCpOOCtuODvCzlsIHlj6PkvZPmurbmjqUo776a772w7727776e772wKSzliY3ph43ph4_muKzlrpos5LqI5YKZ5Yqg54ax44Kz44Oz44OZ44KiLOacrOazqOa2su-8kSzmnKzms6jmtrLvvJIs5pys5rOo5ray77yTLOacrOazqOa2su-8lCzmnKzms6jmtrLvvJUs5pys5rOo5ray77yWLOacrOazqOa2su-8lyzjg5Hjg6zjg4Pjg4jmtJfmtYQsR05DLOi_veOBhOazqOa2sizku67lsIHlj6Pjg7vlvozph43lgbQs5bCB5Y-j77yI44OX44Os44K577yJLOa0l-a1hCxWb-ODu0lS5qSc5p-7LOWkluims-aknOafuyzjg5Hjg6zjg4Pjg4joqbDjgoEiLCJjdXN0b206Zmxvd2xpbmVfYXJlYXMiOiJ7XCIwMVwiOiBbXCLlt7vlj5boo4Xnva7vvJFcIl0sIFwiMDJcIjogW1wi5be75Y-W6KOF572u77ySXCJdLCBcIjAzXCI6IFtcIuW3u-WPluijhee9ru-8k1wiXX0iLCJjdXN0b206dG9waWMiOiIkYXdzXC90aGluZ3NcL2RldiIsImF1dGhfdGltZSI6MTY1MjA1NTU5OSwiY3VzdG9tOnRiX2luZm8iOiJodHRwOlwvXC8xMC4xNzguNjQuMjQyOjMwMDEsRVPlvrPls7Zf5be75Y-W44Ko44Oq44KiLGRHSmZTVk4wYjJ0MWMyaHBiV0UiLCJjdXN0b206cHJvYmxlbV90YWJsZV9sYWJlbHMiOiJ7XCIxXCI6W1wi44OG44K544OIMVwiLCBcIuODhuOCueODiDAxXCIsIFwi44OG44K544OIMDAxXCJdLFwiMlwiOltcIuODhuOCueODiDJcIiwgXCLjg4bjgrnjg4gwMlwiLCBcIuODhuOCueODiDAwMlwiXSwgXCIzXCI6W1wi44OG44K544OIMDNcIl0sIFwiNFwiOltcIuODhuOCueODiDA0XCJdLCBcIjVcIjogW1wi44OG44K544OIMDVcIl0sIFwiNlwiOltcIuODhuOCueODiDA2XCJdfSIsImV4cCI6MTY1MjIzMjAyMywiaWF0IjoxNjUyMjI4NDIzLCJjdXN0b206ZGJuYW1lIjoiSVN0b2t1c2hpbWFfZGV2IiwiY3VzdG9tOm5vdGlmaWNhdGlvbiI6IjEsMSwxLDEsMSIsImNvZ25pdG86dXNlcm5hbWUiOiJpc3Rva3VzaGltYSIsImN1c3RvbTptYWNoaW5lX3N0YXJ0IjoiMTowMCIsImF1ZCI6IjRpdjI0azRjY2pxaWQxdjNyMWtldmpqbXRuIiwiZXZlbnRfaWQiOiI3MDk2MmRhZi1hMzY0LTRmODItYmIwZS0zY2UxMGI3ZDgxZWQiLCJ0b2tlbl91c2UiOiJpZCIsImN1c3RvbTpjYW1lcmFzIjoie1wi5be75Y-W6KOF572u77yRXCI6IFwiY2FtMDFcIiwgXCLlt7vlj5boo4Xnva7vvJJcIjogXCJjYW0wMlwiLCBcIuW3u-WPluijhee9ru-8k1wiOiBcImNhbTAzXCJ9IiwiY3VzdG9tOndvcmtfc3RhcnQiOiIxOjAwIiwiY3VzdG9tOnRocmVzaG9sZCI6IjAsMCwwLDAsMCwwLDAsMCJ9.StME3UC3-IwZ57mMmvqnyad3y_wUhNd-5YtS1QMkpoRo5TiKVZzWrmeX3zsRWQGa5V-3Cppe9qDFo5DsM_e1Tp2i72v9fT67UX6_CjlvWQVbpOpnlI_AisgQkBaB2s6cv8ETZkti4aNZyNLKtNGXQTE2u2WMWPXgxQ0W3yiRSBHKVmz59E51gSuTMqK1fTh0WFlq1O1LYx962xzxtKqsl7RKD4kbvEg7an_qVD6A23zduXh19FxNcgtHOLGWmbQGeyPib1ffNKIQk5lkxa1Ahse5eBK4o7oyiARXFxjA3FH3R-QdeBLTf1NpnYWNlc8yRE2o6UCTRtw_9Hw1Bax-wg',
    },
    'multiValueQueryStringParameters': None
}

"""
PARAM_CHOICES
HTTPリクエストの各パラメータ部分の条件一覧
条件は正常系と異常系を網羅するように以下のような構造となっている
PARAM_CHOICES['test_none']：全ての条件が空の場合を設定
PARAM_CHOICES['テスト対象のパラメータ']['パラメータの種類（第２キーまであれば）']：パラメータを指定してテストを実施

正常系と異常系を網羅するように条件を選択肢してテストを行う。
設計シートでDon't careとなっている絞り込みパラメータについてはテストを行わない。
基本的に変更は不要
"""
PARAM_CHOICES = {
    'test_none':{},
    'test_normal':{
        'processName': ['1'],
        'lineName': ['01'],
        'manufacturerName': ['001'],
        'productName': ['productA'],
        'areaName': ['areaA'],
        'workTypeName': ['10'],
        'periodStartTime': ['20210618000000'],
        'periodEndTime': ['20210618235959']
    },
    'test_aggregationUnit':{
        'test_perDay':{
            'aggregationUnit':['perDay']
        },
        'test_perWeek':{
            'aggregationUnit':['perWeek']
        },
        'test_perLine':{
            'aggregationUnit':['perLine']
        },
        'test_perWorkType':{
            'aggregationUnit':['perWorkType']
        },
    },
    'test_processName':{
        'processName': ['1']
    },
    'test_lineName':{
        'lineName': ['01']
    },
    'test_manufacturerName':{
        'manufacturerName': ['001']
    },
    'test_productName':{
        'productName': ['productA']
    },
    'test_areaName':{
        'areaName': ['areaA']
    },
    'test_workTypeName':{
        'workTypeName': ['10']
    },
    'test_priodTime':{
        'test_normalRange':{
            'periodStartTime': ['20210618000000'],
            'periodEndTime': ['20210618235959']
        },
        'test_errorRange':{
            'periodStartTime': ['20210229000000'],
            'periodEndTime': ['20210229235959']
        },
        'test_errorData':{
            'periodEndTime': ['Error'], 
            'periodStartTime': ['100']
        },
    }
}

"""
------------------------------
# テストコード
------------------------------
"""

"""
test_XXXX_lambda_handler
仮想リソース１つ分のテスト用関数
追加した仮想リソースに対して、@pytest.mark.parametrize()の条件全てでテストする。

■parametrize()のテスト条件
    'test_path'：テスト条件の動作+対象と、分析方法
    'test_param'：テスト条件のHTTPリクエストの絞り込みパラメータ

■テストのひな型
ひな形は以下の通りとなっている
@pytest.mark.parametrize(
    'test_path, test_param', [
        ('テストするAPIのパス', PARAM_CHOICES[テストするパラメータの条件])
    ]
)
def test_XXXX_lambda_handler(test_path, test_param):
    sys.path.append("../CPSSVXXXXService")
    from lambda_function import lambda_handler
    REQUEST_EVENT['multiValueQueryStringParameters'] = test_param
    REQUEST_EVENT['path'] = test_path
    assert lambda_handler(REQUEST_EVENT, None) != None

■API追加時のテスト追加方法（自動化予定）
仮想リソースを追加する場合は上記のひな型をコピーして以下の各部分を修正
（既存の仮想リソースにAPIを追加する場合はコピーせずに以下を実行）
1. テスト関数名を変更
    XXXXは、CPSSVOperationTimeServiceのOperationTimeに相当するリソース名
2. importしてくるlambda関数のフォルダをテスト対象のリソースに変更
    sys.path.append("../CPSSVXXXXService")部分
3. pytest.mark.parametrizeのテスト条件の追加
    追加したAPIに合わせてテスト対象のパスとパラメータを追加
"""

"""
test_OperationTime_lambda_handler
仮想リソース：OperationTime用のテスト関数
現在、テスト対象のAPIは以下のとおりである

■テスト対象：
  動作+対象：実績値を取得、分析方法：変換無し
"""
@pytest.mark.parametrize(
    'test_path, test_param', [
        # ★★ OperationTimeのAPIが増える度にテスト条件を追加していく
        ('/OperationTime/getResults', PARAM_CHOICES['test_none']),
        ('/OperationTime/getResults', PARAM_CHOICES['test_normal']),
        ('/OperationTime/getResults', PARAM_CHOICES['test_priodTime']['test_normalRange']),
        ('/OperationTime/getResults', PARAM_CHOICES['test_priodTime']['test_errorRange']),
        ('/OperationTime/getResults', PARAM_CHOICES['test_priodTime']['test_errorData']),
        ('/OperationTime/getResults', PARAM_CHOICES['test_aggregationUnit']['test_perLine']),
    ]
)
def test_OperationTime_lambda_handler(test_path, test_param):
    from pymongo import MongoClient
    client = MongoClient("mongodb://root:password@localhost:27017")
    db = client['test']
    collection = db['test_db']
    collection.find_one()


