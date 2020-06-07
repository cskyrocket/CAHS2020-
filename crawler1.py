import time
import GetOldTweets3 as got
import datetime
from random import uniform
from tqdm import tqdm
import pandas as pd

days_range = []

start = datetime.datetime.strptime("2020-02-01", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-02-02", "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))

print("설정 트윗 수집 기간은 {}에서 {} 까지".format(days_range[0], days_range[-1]))
print("총 {}일간 데이터 수집".format(len(days_range)))

start_date = days_range[0]
end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d")
            + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# 크롤링 기준 및 크롤링
tweetCriteria = got.manager.TweetCriteria().setQuerySearch('코로나 OR 쿠팡') \
    .setSince(start_date) \
    .setUntil(end_date) \
    .setMaxTweets(-1)

start_time = time.time()
tweet = got.manager.TweetManager.getTweets(tweetCriteria)

print("Collecting data end... {0:0.2f} Minutes".format((time.time() - start_time) / 60))
print("total number of tweets is {}".format(len(tweet)))

# 변수 저장


tweet_list = []

for index in tqdm(tweet):
    tweet_date = index.date.strftime('%Y-%m-%d')
    tweet_time = index.date.strftime('%H:%M:%S')
    content = index.text
    retweets = index.retweets
    favorites = index.favortites

    info_list = [tweet_date, tweet_time, content, retweets, favorites]
    tweet_list.append(info_list)

    time.sleep(uniform(1, 2))

# 파일 저장

twitter_df = pd.DataFrame(tweet_list,
                          columns=["date", "time", "text", "retweets", "favorites"])

twitter_df.to_csv("twitter_data_{}_to_{}.csv".format(days_range[0], days_range[-1]), index=False)
print("{} tweets are saved".format(len(tweet_list)))
