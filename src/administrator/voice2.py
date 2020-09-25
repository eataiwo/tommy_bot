import talkey
tts = talkey.Talkey(
    preferred_languages=['en'],

    # The factor by which preferred_languages gets their score increased, defaults to 80.0
    preferred_factor=80.0,

    engine_preference=['pico'],

    # Here you segment the configuration by engine
    # Key is the engine SLUG, in this case ``espeak``
    pico={
        # Specify the engine options:
        'options': {
            'enabled': True,
        }
    }
)
tts.say('Old McDonald had a farm', 'en')