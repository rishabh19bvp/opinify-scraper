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

# Send Telegram alert if this many items share a domain within 3 hours
SPIKE_THRESHOLD = 10

SCORE_WEIGHTS = {
    "reddit_upvotes":  0.4,
    "reddit_comments": 0.3,
    "news_recency":    0.2,
    "keyword_density": 0.1,
}

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
