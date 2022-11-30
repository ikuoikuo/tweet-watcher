import json
import tweepy
from tweepy.streaming import StreamResponse
from dotenv import load_dotenv
import os 
import textwrap
import requests
load_dotenv()
twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

BEARER_TOKEN = twitter_bearer_token


class MyStreamingClient(tweepy.StreamingClient):

    def on_data(self, raw_data: str) -> None:
        # 生データを確認する
        print(json.loads(raw_data))
        super().on_data(raw_data)

    def on_response(self, response: StreamResponse) -> None:
        # raw_data が加工されて StreamResponse で受け取れる
        print("ーーーーーーーーーーーーーーーーーーーーーーーー")
        print(response.data.text)
        print(response.includes["users"][0].name)
        heredoc = textwrap.dedent('''
        {user_name} tweeted!
        {text}
        ''').format(user_name =response.includes["users"][0].name , text = response.data.text).strip()

        #lineに通知
        line_notify_token = os.getenv('LINE_NOTIFY_TOKEN')
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': f'message: {heredoc}'}
        requests.post(line_notify_api, headers = headers, data = data)	


client = MyStreamingClient(BEARER_TOKEN)
rules = client.get_rules()
print(rules)
client.filter(
    expansions=[
        "author_id",
        "referenced_tweets.id",
        "edit_history_tweet_ids",
        "in_reply_to_user_id",
        "attachments.media_keys",
        "attachments.poll_ids",
        "geo.place_id",
        "entities.mentions.username",
        "referenced_tweets.id.author_id"
    ],
    media_fields=[
        "media_key",
        "type",
        "url",
        "duration_ms",
        "height",
        "non_public_metrics",
        "organic_metrics",
        "preview_image_url",
        "promoted_metrics",
        "public_metrics",
        "width",
        "alt_text",
        "variants"
    ],
    place_fields=[
        "full_name",
        "id",
        "contained_within",
        "country",
        "country_code",
        "geo",
        "name",
        "place_type"
    ],
    poll_fields=[
        "id",
        "options",
        "duration_minutes",
        "end_datetime",
        "voting_status"
    ],
    tweet_fields=[
        "id",
        "text",
        "attachments",
        "author_id",
        "context_annotations",
        "created_at",
        "entities",
        "geo",
        "in_reply_to_user_id",
        "lang",
        "possibly_sensitive",
        "public_metrics",
        "referenced_tweets",
        "source",
        "withheld"
    ],
    user_fields=[
        "id",
        "name",
        "username",
        "created_at",
        "description",
        "entities",
        "location",
        "pinned_tweet_id",
        "profile_image_url",
        "protected",
        "url",
        "verified",
        "withheld"
    ]
)