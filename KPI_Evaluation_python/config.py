from logging_util import setup_logging
class Config:
    T = 24
    median = int(T/2)
    FF_PC_ref = 7.0
    def get_config():
        return Config()
