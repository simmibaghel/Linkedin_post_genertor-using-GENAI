def linkedin_prompt(context_posts, topic):
    return f"""
You are a LinkedIn content creator.

Below are example LinkedIn posts written in a specific style.
Carefully observe their tone, structure, emojis, and formatting.

EXAMPLE POSTS:
{context_posts}

TASK:
Write a new LinkedIn post on the topic:
"{topic}"

RULES:
- Follow the same writing style
- Use professional but engaging tone
- Use emojis naturally
- Keep line breaks like LinkedIn posts
- End with a question or CTA
"""
