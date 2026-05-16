CIVIC_KEYWORDS = [
    # PMC and governance
    "pmc", "pune municipal", "ward", "councillor", "nagar sevak",
    "corporation", "mayor", "civic", "municipality",
    # Infrastructure
    "pothole", "road", "footpath", "flyover", "bridge", "signal",
    "streetlight", "drainage", "flood", "waterlogging", "pipeline",
    "water supply", "water cut", "electricity cut", "outage",
    # Environment
    "tree", "garden", "lake", "river", "mula", "mutha", "pollution",
    "garbage", "waste", "dumping", "sewage", "open drain",
    # Transport
    "pmpml", "bus", "metro", "cycle", "rickshaw", "auto", "traffic",
    "parking", "signal", "speed breaker",
    # Healthcare and social
    "hospital", "dispensary", "health centre", "ambulance",
    "street children", "homeless", "beggar", "slum",
    # Civic chaos signal words
    "complaint", "broken", "damaged", "filthy", "stench", "unsafe",
    "accident", "collapsed", "overflowing", "blocked", "encroachment",
]

DOMAIN_KEYWORDS = {
    "transport":      ["pmpml", "bus", "metro", "cycle", "traffic", "parking", "signal", "road", "pothole", "flyover", "footpath"],
    "environment":    ["tree", "lake", "river", "pollution", "garbage", "waste", "dumping", "sewage", "mula", "mutha", "garden"],
    "healthcare":     ["hospital", "dispensary", "health", "ambulance", "street children", "homeless", "slum"],
    "governance":     ["pmc", "ward", "councillor", "nagar sevak", "mayor", "corporation", "election", "civic"],
    "infrastructure": ["waterlogging", "flood", "drainage", "water supply", "electricity", "streetlight", "bridge", "pipeline"],
}

# Words that signal someone is frustrated/complaining (not just mentioning a topic)
COMPLAINT_SIGNALS = [
    # Frustration words
    "terrible", "pathetic", "disgusting", "useless", "horrible", "shameful",
    "worst", "absurd", "ridiculous", "unacceptable", "embarrassing", "disgrace",
    # Time-based frustration
    "months", "years", "still", "since", "waiting", "no action", "ignored",
    "never fixed", "always", "every day", "every monsoon", "again",
    # Direct complaint language
    "complaint", "complain", "fix this", "why is", "why are", "when will",
    "nobody", "no one", "nothing done", "helpless", "frustrated", "fed up",
    "tired of", "sick of", "enough",
    # Damage/danger words
    "broken", "damaged", "collapsed", "dangerous", "accident", "injured",
    "flooded", "overflowing", "blocked", "filthy", "stench", "garbage",
    "open drain", "no water", "no electricity", "power cut", "water cut",
    # Question/rant markers
    "wtf", "seriously", "smh", "rant", "issue", "problem", "concern",
    # Casual Reddit frustration language
    "why tf", "how long", "pathetic state", "no one cares", "please fix",
    "raise complaint", "filed complaint", "no response", "disappointed",
    "shocking", "outrageous", "unbearable", "intolerable", "miserable",
    "what is pmc", "pmc does", "bmc does", "authorities", "responsible",
    "who is responsible", "take action", "please help", "help needed",
    "anyone else", "same problem", "same issue", "facing this",
    "my area", "our area", "our society", "our colony", "our ward",
    "not working", "stopped working", "out of order", "no maintenance",
]

# Send Telegram alert if this many items share a domain within 3 hours
SPIKE_THRESHOLD = 10

SCORE_WEIGHTS = {
    "reddit_upvotes":  0.4,
    "reddit_comments": 0.3,
    "news_recency":    0.2,
    "keyword_density": 0.1,
}

# Reddit feeds — subreddit new posts + site-wide civic complaint searches
REDDIT_RSS_FEEDS = [
    # r/pune — general but has complaints
    "https://www.reddit.com/r/pune/new.rss",
    # Reddit-wide searches — catches posts across ALL subreddits mentioning Pune civic issues
    "https://www.reddit.com/search.rss?q=pune+pothole&sort=new&t=week",
    "https://www.reddit.com/search.rss?q=pune+pmc+complaint&sort=new&t=week",
    "https://www.reddit.com/search.rss?q=pune+waterlogging&sort=new&t=week",
    "https://www.reddit.com/search.rss?q=pune+garbage+problem&sort=new&t=week",
    "https://www.reddit.com/search.rss?q=pune+pmpml&sort=new&t=week",
    "https://www.reddit.com/search.rss?q=pune+worst+OR+pune+pathetic+OR+pune+broken&sort=new&t=week",
    "https://www.reddit.com/search.rss?q=pcmc+OR+pmc+pune&sort=new&t=week",
]

# Quora via Google RSS — bypasses Cloudflare, finds real complaint threads
QUORA_RSS_FEEDS = [
    "https://news.google.com/rss/search?q=site:quora.com+pune+civic+problem&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=site:quora.com+pune+pmc&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=site:quora.com+pune+pothole+garbage+traffic&hl=en-IN&gl=IN&ceid=IN:en",
    "https://news.google.com/rss/search?q=site:quora.com+pune+waterlogging+flood&hl=en-IN&gl=IN&ceid=IN:en",
]

# Direct RSS feeds — news sites with Pune civic coverage
DIRECT_RSS_FEEDS = [
    {"name": "toi-pune",       "url": "https://timesofindia.indiatimes.com/rssfeeds/7503928.cms"},
    {"name": "ie-pune",        "url": "https://indianexpress.com/section/cities/pune/feed/"},
    {"name": "hindustan-times-pune", "url": "https://www.hindustantimes.com/feeds/rss/cities/pune/rssfeed.xml"},
    {"name": "sakal-pune",     "url": "https://www.sakaaltimes.com/rss/pune"},
]

RSS_QUERIES = [
    "PMC Pune",
    "Pune ward",
    "Pune pothole",
    "Pune waterlogging",
    "Pune civic",
    "Pune traffic",
    "Pune garbage",
    "Pune tree",
    "Pune municipal corporation",
    "Pune flooding",
]

NEWS_SITES = [
    {
        "name": "Pune Mirror",
        "url": "https://punemirror.com/pune",
        "article_selector": "article",
        "title_selector": "h2",
        "link_selector": "a",
    },
    {
        "name": "Maharashtra Times",
        "url": "https://maharashtratimes.com/maharashtra/pune-news",
        "article_selector": ".article-list article",
        "title_selector": "h3",
        "link_selector": "a",
    },
]
