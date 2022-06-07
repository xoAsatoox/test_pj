import sys
import re


class TypeChecker:
    def __init__(self, config):
        pass

    def isValidOutline(self, expect, record):
        print('Function:', sys._getframe().f_code.co_name)
        return self.isValidBlock(expect, record)

    def isValidUnique(self, expect, record):
        print('Function:', sys._getframe().f_code.co_name)
        if type(record) is list:
            for item in record:
                if not self.isValidBlock(expect, item):
                    return False
        else:
            if not self.isValidBlock(expect, record):
                return False

        return True

    def isValidBlock(self, expect, record):
        for expectName, expectType in expect.items():

            if expectName not in record:
                print('Not Found:', expectName)
                return False

            if not self.isValidItem(record[expectName], expectType):
                print('Invalid Field:', expectName)
                return False

        return True

    def isValidItem(self, fieldValue, expectType):
        if fieldValue != '':
            if type(expectType) is str:
                if not self.isValidLiteral(expectType, fieldValue):
                    return False
            elif type(expectType) is dict:
                if not self.typeCheck(fieldValue, dict):
                    return False

                if not self.isValidBlock(expectType, fieldValue):
                    return False
            elif type(expectType) is list:
                if not self.typeCheck(fieldValue, list):
                    return False

                if len(expectType) > 0:
                    for item in fieldValue:
                        if not self.isValidBlock(expectType[0], item):
                            return False
            else:
                raise Exception("Invalid Expect Result Pattern.")

        return True

    def isValidLiteral(self, expectType, item):
        if expectType == 'str':
            return self.typeCheck(item, str)
        elif expectType == 'int':
            # TODO: 応急処置
            if type(item) == float:
                item = int(item)
            return self.typeCheck(item, int)
        elif expectType == 'date':
            if self.typeCheck(item, str):
                ReDatestr = re.compile(r'\d{14}')
                return ReDatestr.match(item)
            else:
                return False
        elif expectType == 'dateYYYYMMDDHHMM':
            if self.typeCheck(item, str):
                ReDatestr = re.compile(r'\d{12}')
                return ReDatestr.match(item)
            else:
                return False
        elif expectType == 'dateYYYYMMDDHH':
            if self.typeCheck(item, str):
                ReDatestr = re.compile(r'\d{10}')
                return ReDatestr.match(item)
            else:
                return False
        elif expectType == 'dateYYYYMMDD':
            if self.typeCheck(item, str):
                ReDatestr = re.compile(r'\d{8}')
                return ReDatestr.match(item)
            else:
                return False
        elif expectType == 'dateYYYYMM':
            if self.typeCheck(item, str):
                ReDatestr = re.compile(r'\d{6}')
                return ReDatestr.match(item)
            else:
                return False
        elif expectType == 'dateYYYY':
            if self.typeCheck(item, str):
                ReDatestr = re.compile(r'\d{4}')
                return ReDatestr.match(item)
            else:
                return False
        else:
            return False

    def typeCheck(self, target, expect):
        if type(target) is not expect:
            print('InvalidType:', type(target), 'expect:', expect)
            return False
        else:
            return True
