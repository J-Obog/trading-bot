from yahoo import Sentiment, YahooApi
import numpy as np

buys = 0
sells = 0
holds = 0 

sratings = YahooApi.get_ratings("UNH")

for rating in sratings:
    if rating.sentiment == Sentiment.BUY:
        buys += 1
        #print(rating.price_target)
    elif rating.sentiment == Sentiment.SELL:
        sells += 1
    else:
        holds += 1





if buys > 0:
    bb = [r.price_target for r in sratings if r.sentiment == Sentiment.BUY and (r.price_target is not None)]
    print(f"Buy avg = {np.average(bb)}")

if sells > 0:
    aa = [r.price_target for r in sratings if r.sentiment == Sentiment.SELL and (r.price_target is not None)]
    print(f"Sell avg = {np.average(aa)}")

if holds > 0:
    cc = [r.price_target for r in sratings if r.sentiment == Sentiment.NEUTRAL and (r.price_target is not None)]
    print(f"Hold avg = {np.average(cc)}")

#np.average

print(buys, sells, holds)