import pprint
import shioaji as sj
from shioaji import TickFOPv1, Exchange
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
    ca_path=r'E:/桌面/憑證/ekey/551/A127016469/S/Sinopac.pfx',
    ca_passwd="A127016469",
    person_id="A127016469",
)

print(f'Active CA : {result}')


# print(api.Contracts.Stocks["2890"])

# print(api.Contracts.Futures["TXFA2"])

# print(api.Contracts.Options["TXO18000R3"])

@api.quote.on_event
def event_callback(resp_code: int, event_code: int, info: str, event: str):
    print(f'Event code: {event_code} | Event: {event}')
    print(f'Info: {info}')


@api.on_tick_fop_v1()
def quote_callback(exchange:Exchange, tick:TickFOPv1):
    print(f"Exchange: {exchange}, Tick: {tick}")

api.quote.subscribe(api.Contracts.Stocks["2330"], quote_type="tick")
api.quote.subscribe(
    api.Contracts.Futures.TXF["TXFR1"],
    quote_type = sj.constant.QuoteType.Tick,
    version = sj.constant.QuoteVersion.v1,
)


api.logout()
