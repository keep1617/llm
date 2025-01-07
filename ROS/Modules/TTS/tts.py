from gtts import gTTS

from IPython.display import Audio
from IPython.display import display

text = "안녕하세요 저는 바텐더 Cyber 예요"
tts = gTTS(text, lang="ko")
tts.save("hi.mp3")

wn = Audio('hi.mp3', autoplay=True)
display(wn)