from datetime import datetime


class Logger:
    @staticmethod
    def get_log(text, *args):
        now_date = datetime.now().date()
        now_time = datetime.now().time()
        print(f'{now_date} - {now_time} >>> {text}', *args)
