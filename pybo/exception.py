class ExceptionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg # 에러 메시지 가공