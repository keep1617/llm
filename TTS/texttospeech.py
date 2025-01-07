def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        name="ko-KR-Neural2-C",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("./ko-KR-Neural2-C.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output_texttospeech-ko-KR-Standard-D.mp3')
        
synthesize_text("물론이죠! 손님, 오늘 어떤 기분이신지 여쭤봐도 될까요? 취향에 맞는 음료를 추천드리고 싶어서요. 오늘의 분위기에 맞는 특별한 한 잔을 제안드려도 될까요 ")
    