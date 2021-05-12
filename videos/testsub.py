from moviepy import editor
import os.path as op

'''
def annotate(clip, txt, txt_color='red', fontsize=50, font='Xolonium-Bold'):
    """ Writes a text at the bottom of the clip. """
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=font, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)

video = editor.VideoFileClip('video_desktop_app.mp4')
subs = [((0, 4), 'subs1'),
        ((4, 9), 'subs2'),
        ((9, 12), 'subs3'),
        ((12, 16), 'subs4')]
annotated_clips = [annotate(video.subclip(from_t, to_t), txt) for (from_t, to_t), txt in subs]
final_clip = editor.concatenate_videoclips(annotated_clips)
final_clip.write_videofile('video_desktop_app2.mp4')
'''

from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

generator = lambda txt: TextClip(txt, font='Arial', fontsize=24, color='white')
#subs = open('vid2.srt').read().splitlines()
subs = [((5, 16), 'Hello, I am Alexa, your health insurance assistant!\n You can ask for your benefits, premiums and recommendations!\n First tell me your user id!'),\
	((25, 42), 'Welcome John. Your last premium for policy Alpha Hospital Cash Insurance was missed,\n which was due on 05 of March 2021, please pay it ASAP.\n Now, tell me what do you want to know about?\n You can ask for your benefits, premiums and recommendations.'),\
	((48, 55), 'what service do you want to know more about? you can ask for the coverage for a disease.'),\
	((59, 65), 'Your coverage for orthopedic for the policy Alpha Hospital Cash Insurance is $15000\n and you have claimed $1000.'),\
	((72,76), 'diabetes is not covered in your policy.'),\
	((83, 94), 'Hey John , your premium amount for policy Alpha Hospital Cash Insurance is $500\n and you have only paid 2 premium(s) till now!\n Please pay the remaining ASAP to avoid inconvenience.'),\
	((99, 106), 'Top 2 products recommended for you are:\n Alpha Comprehensive Insurance and Alpha Care Micro Insurance.')]

subtitles = SubtitlesClip(subs, generator)

video = VideoFileClip("video_desktop_app.mp4")
result = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])

result.write_videofile("out.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")
