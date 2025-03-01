import sys
from api_communcation import *


filename = sys.argv[1]

audio_url = upload(filename)
save_transcript(audio_url=audio_url,filename=filename)
