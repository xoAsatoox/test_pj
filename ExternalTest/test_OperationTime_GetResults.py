import copy
import datetime
import json
import pytest

from Lib.APIAccess import APIAccess
from Lib.TypeChecker import TypeChecker

today_start = int(datetime.date.today().strftime('%Y%m%d000000'))
today_end = int(datetime.date.today().strftime('%Y%m%d235959'))


"""
------------------------------
# 設定
------------------------------
"""
# ★★ ファイル内の、認証用ユーザー名などを変更
FILE_CONFIG = 'config.json'

# ★★ テスト対象のAPIのアドレスを設定
# TARGET_API = 'https://g9s1xfmhha.execute-api.ap-northeast-1.amazonaws.com/default/OperationTime/getResults'
TARGET_API = 'https://b3h8cjobme.execute-api.ap-northeast-1.amazonaws.com/default/OperationTime/getResults'

# ★★ テスト用のデータを入れたディレクトリを設定
DIR_TESTDATA = './TestCase/OperationTime/'

# ★★ 応答パターンのファイルを設定
FILE_RESULT_PATTERN = DIR_TESTDATA + 'ResultPattern_GetResults.json'


"""
------------------------------
# 準備
------------------------------
"""
with open(FILE_CONFIG, encoding='utf-8') as f:
    config = json.load(f)

apiAccessor = APIAccess(config)
apiAccessor.readyAccess(isGetToken=True)
apiAccessor.setURI(TARGET_API)

typeChecker = TypeChecker(config)

outlinePattern = None
resultPattern = None

with open(config['ResultPattern']['outline'], encoding='utf-8') as f:
    outlinePattern = json.load(f)

with open(FILE_RESULT_PATTERN, encoding='utf-8') as f:
    resultPattern = json.load(f)

@pytest.mark.fast
@pytest.mark.parametrize(
    'targetPath, patternIdx, addParam', [
        ('', '変換無し', {}),
    ]
)
def test_TypeCheck(targetPath, patternIdx, addParam):
    params = {
        'periodStartTime': 20220105000000,
        'periodEndTime': 20220105235959,
    }
    params.update(addParam)

    # API実行
    res = apiAccessor.get(path=targetPath, params=params)
    assert res is not None

    # 書式チェック(全API共通部分)
    assert typeChecker.isValidOutline(outlinePattern['Normal'], res)
    # 書式チェック(API固有部分)
    assert typeChecker.isValidUnique(resultPattern[patternIdx]['Pattern'], res['Values'])
