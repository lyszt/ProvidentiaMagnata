import sqlite3
import peewee
import logging
import inspect

class Whitelist:
    def __init__(self):
        pass
    def checkUser(self,user_id: int) -> bool:
        userid = str(user_id)
        current_frame = inspect.currentframe()
        top_function = inspect.getframeinfo(current_frame.f_back).function
        try:
            whitelisted = Whitelist.get(Whitelist.userid == userid)
            if whitelisted:
                if "on_message" not in top_function:
                    logging.info(f"Whitelisted user command. ID: {userid}")
                return True
        except ValueError:
            return False
        except Exception as err:
            error = str(err)
            if "instance matching query does not exist" in error:
                pass
            else:
                logging.info("Erro na verificação da Whitelist:", err)
                logging.error(err)
