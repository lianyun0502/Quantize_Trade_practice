import pprint
import shioaji as sj
from shioaji import TickFOPv1, Exchange, TickSTKv1
import os
from dotenv import load_dotenv #從dotenv模組中匯入load_dotenv這個function

load_dotenv() #讀取設定檔中的內容至環境變數

api = sj.Shioaji(simulation=True)# 初始化時，simulation設為True，代表要使用模擬環境

api.login(
    api_key=os.getenv('API_Key'),
    secret_key=os.getenv('Secret_Key'),
    contracts_timeout=10000,
          )
accounts = api.list_accounts()
pprint.pp(accounts)

result = api.activate_ca(
    ca_path=r'./憑證/ekey/551/A127016469/S/Sinopac.pfx',
    ca_passwd=os.getenv('CA_PASSWORD'),
    person_id=os.getenv('PERSON_ID'),
)

print(f'Active CA : {result}')


@api.quote.on_event
def event_callback(resp_code: int, event_code: int, info: str, event: str):
    print(f'Event code: {event_code} | Event: {event}')
    # print(f'Info: {info}')


def quote_callback(exchange:Exchange, tick:TickSTKv1):
    print('--------------')
    print(f"Exchange: {exchange}\nTick: {tick}")
    pass

api.quote.set_on_tick_fop_v1_callback(quote_callback)
api.quote.set_on_tick_stk_v1_callback(quote_callback)

api.quote.subscribe(api.Contracts.Stocks["2330"], 
                    quote_type="tick",
                    version=sj.constant.QuoteVersion.v1,
                    )
# api.quote.subscribe(
#     api.Contracts.Futures.TXF["TXFR1"],
#     quote_type = sj.constant.QuoteType.Tick,
#     version = sj.constant.QuoteVersion.v1,
# )

input("Press any key to continue...")
api.logout()
