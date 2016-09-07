import requests
import os
import datetime
import dateutil.parser
import asyncio

class TwitchModule:

    def __init__(self, client, channel):
        self.client = client
        self.channel = channel
        self.name = 'Twitch'
        if 'TWITCH_TOKEN' in os.environ:
            twitch_token = os.environ['TWITCH_TOKEN']
        else:
            self.client.send_message(channel, 'No twitch token found!')
        self.headers = {'Accept': 'application/vnd.twitchtv.v3+json', 'Authorization': 'OAuth ' + twitch_token}
        self.params = {'stream_type': 'all'}
        self.events = [self.get_streams]

    async def get_streams(self):
        while True:
            r = requests.get('https://api.twitch.tv/kraken/streams/followed',
                   headers=self.headers, params=self.params)
            streams = r.json()['streams']
            summary = []
            for stream in streams:
                stream_time = dateutil.parser.parse(stream['created_at'], ignoretz=True)
                time_diff = datetime.datetime.utcnow() - stream_time
                if time_diff.total_seconds() < 130:
                    streamer  = stream['channel']['display_name']
                    stream_game = stream['game']
                    stream_title = stream['channel']['status']
                    summary.append('{} is streaming {}: {}'.format(streamer, stream_game, stream_title))
                #print(stream['created_at'])
                #print(stream['channel']['display_name'])
            if summary:
                await self.client.send_message(self.channel, '\n'.join(summary))
            await asyncio.sleep(120)

    async def on_message(self):
        pass
