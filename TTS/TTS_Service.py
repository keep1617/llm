from google.cloud import texttospeech
import rospy
from std_msgs.msg import String

class TTS:
    def __init__(self):
        self.tts_client = texttospeech.TextToSpeechClient()
        self.voice = texttospeech.VoiceSelectionParams(
            language_code="ko-KR", 
            name="ko-KR-Neural2-C", #목소리 C 또는 D로 변경 가능
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )
        self.audio_config = texttospeech.AudioConfig( # MP3로 저장
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
    def get_input(self,input_text): #input 가져오기
        self.input = texttospeech.SynthesisInput(text=input_text)
        
    def get_output(self): #get response
        self.response = self.tts_client.synthesize_speech(
        request={"input": self.input, "voice": self.voice, "audio_config": self.audio_config}
    )
    
    def save_ouput(self):
        with open("./ko-KR-Neural2-C.mp3", "wb") as out:
            out.write(self.response.audio_content)
            print('Audio content written to file "output_texttospeech-ko-KR-Standard-D.mp3')

def callback(msg):
    rospy.loginfo("Received message: %s", msg.data)
    tts_client = TTS()
    tts_client.get_input(msg.data)
    tts_client.get_output()
    tts_client.save_output()
    

def listener():
    node_name = "TTSServiceServerNode"
    rospy.init_node(node_name)
    rospy.Subscriber('speaking', String, callback) #토픽 이름을 모르겠당
    rospy.spin()




if __name__ == "__main__":
    listener()