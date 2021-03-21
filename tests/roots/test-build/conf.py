extensions = ["ablog"]

# Enable Atom feed generation
blog_baseurl = "https://blog.example.com/"
# Include full post in feeds
blog_feed_fulltext = True
# Add a social media Atom feed
blog_feed_templates = {
    # Use defaults, no templates
    "atom": {},
    # Create content text suitable posting to micro-bogging
    "social": {
        # Format tags as hashtags and append to the content
        "content": "{{ title }}{% for tag in post.tags %}"
        " #{{ tag.name|trim()|replace(' ', '') }}"
        "{% endfor %}",
    },
}
