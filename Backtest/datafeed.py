from backtrader import feeds
class DataFeed(feeds.GenericCSVData):
    params = (
        ('dtformat', '%Y%m%d %H:%M:%S'),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', -1),
        ('openinterest', -1)
    )