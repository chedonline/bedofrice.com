"""Make the Harvest Race announcer lines with ElevenLabs (run on the rig).

    python make_voice.py            # only the lines that don't have an mp3 yet
    python make_voice.py --all      # redo every line

The key comes from the beat-filler client (C:\\Users\\chedo\\.secrets\\elevenlabs.key first) and is never printed.
The game loads voice/<id>.mp3 and falls back to silence if a file is missing.
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', 'beat-filler', 'voice'))
import eleven  # noqa: E402

VOICE_NAME = 'Charlie'          # Deep, Confident, Energetic
MODEL = 'eleven_multilingual_v2'
SETTINGS = {'stability': .32, 'similarity_boost': .8, 'style': .75, 'use_speaker_boost': True}

LINES = {
    # big cuts, by size
    'nice':      'Nice!',
    'double':    'Double cut!',
    'mega':      'Mega cut!',
    'ricestorm': 'RICE STORM!',
    'unstop':    'Un-stop-pable!',
    # moments
    'ready':     'Get ready...',
    'harvest':   'Harvest!',
    'fever':     'Harvest fever!',
    'together':  'Together!',
    'perfect':   'Perfect!',
    'handoff':   'Hand-off!',
    'shoo':      'Shoo!',
    'penned':    'Penned!',
    'delivered': 'Delivered!',
    'golden':    'Golden duck!',
    'goldgot':   'You caught the golden duck!',
    'boar':      'Look out, boar!',
    'bonk':      'Bonk!',
    'star1':     'One star!',
    'star2':     'Two stars!',
    'star3':     'Three stars!',
    'cleared':   'Field cleared!',
    'sunset':    'Sunset!',
    'winner':    'Winner!',
    'newhat':    'New hat!',
    'milestone': 'What a haul!',
    'daily':     "Today's field!",
}


def tts(voice_id, text):
    body = json.dumps({'text': text, 'model_id': MODEL, 'voice_settings': SETTINGS}).encode()
    req = urllib.request.Request(f'{eleven.API}/text-to-speech/{voice_id}?output_format=mp3_44100_64', data=body,
                                 headers={'xi-api-key': eleven.key(), 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main():
    redo = '--all' in sys.argv
    v = next(v for v in eleven.voices() if v['name'].startswith(VOICE_NAME))
    made = 0
    for k, text in LINES.items():
        out = os.path.join(HERE, k + '.mp3')
        if os.path.exists(out) and not redo:
            continue
        open(out, 'wb').write(tts(v['voice_id'], text))
        made += 1
        print('made', k, '-', text)
    json.dump({'voice': v['name'], 'model': MODEL, 'lines': LINES}, open(os.path.join(HERE, 'lines.json'), 'w'), indent=1)
    print(f'{made} new, {len(LINES)} lines in all')


if __name__ == '__main__':
    main()
