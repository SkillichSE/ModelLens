"""
News Parser for AI Model Updates
Scrapes news from various AI providers
"""

import os
import json
import requests
import feedparser
from datetime import datetime
from pathlib import Path
from config import NEWS_SOURCES

class NewsParser:
    def __init__(self):
        self.news_items = []
    
    def parse_rss_feed(self, url, keywords):
        """Parse RSS feed"""
        try:
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:10]:  # Latest 10
                title = entry.get("title", "")
                
                # Check if relevant
                if any(kw.lower() in title.lower() for kw in keywords):
                    self.news_items.append({
                        "title": title,
                        "link": entry.get("link", ""),
                        "date": entry.get("published", ""),
                        "source": "HuggingFace",
                        "summary": entry.get("summary", "")[:200]
                    })
        except Exception as e:
            print(f"⚠️  Error parsing RSS: {e}")
    
    def parse_webpage(self, source_name, config):
        """Parse webpage for news (placeholder - needs proper scraping)"""
        # Note: For production, would use BeautifulSoup
        # This is a simplified version using RSS when available
        print(f"📰 Checking {source_name}...")
        
        if "rss" in config:
            self.parse_rss_feed(config["rss"], config["keywords"])
    
    def fetch_all_news(self):
        """Fetch news from all sources"""
        print("🔍 Fetching AI news...")
        
        for source_name, config in NEWS_SOURCES.items():
            self.parse_webpage(source_name, config)
        
        # Sort by date (newest first)
        self.news_items.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        # Deduplicate
        seen = set()
        unique_news = []
        for item in self.news_items:
            if item["title"] not in seen:
                seen.add(item["title"])
                unique_news.append(item)
        
        self.news_items = unique_news[:20]  # Keep latest 20
        print(f"✅ Found {len(self.news_items)} news items")
    
    def save_news(self):
        """Save news to JSON"""
        Path("data/results").mkdir(parents=True, exist_ok=True)
        
        news_file = "data/results/news.json"
        with open(news_file, "w") as f:
            json.dump({
                "updated": datetime.now().isoformat(),
                "count": len(self.news_items),
                "items": self.news_items
            }, f, indent=2)
        
        print(f"💾 News saved to {news_file}")

if __name__ == "__main__":
    parser = NewsParser()
    parser.fetch_all_news()
    parser.save_news()
    print("✨ News parsing complete!")
