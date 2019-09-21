# from file_manager import FileManager

# root = '/home/enigmaeth/Videos/accentPhase2/raw'
# accepted_formats = ['wav', 'mp3']
# FM = FileManager(root, accepted_formats)

# all_files = FM.get_all_files()

# for file in all_files:
#     language = file.split(' ')[0].split('/')[-1]

# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

# Load your audio.
song = AudioSegment.from_mp3("/home/enigmaeth/Videos/accentPhase2/raw/sb.wav")

# Split track where the silence is 2 seconds or more and get chunks using 
# the imported function.
chunks = split_on_silence (
    # Use the loaded audio.
    song, 
    # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
    min_silence_len = 1,
    # Consider a chunk silent if it's quieter than -16 dBFS.
    # (You may want to adjust this parameter.)
    silence_thresh = 1000
)
print("split ", len(chunks))

# Process each chunk with your parameters
for i, chunk in enumerate(chunks):
    # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
    # silence_chunk = AudioSegment.silent(duration=500)

    # Add the padding chunk to beginning and end of the entire chunk.
    # audio_chunk = silence_chunk + chunk + silence_chunk

    # Normalize the entire chunk.
    # normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

    # Export the audio chunk with new bitrate.
    print("Exporting chunk{0}.mp3.".format(i))
    normalized_chunk.export(
        ".//chunk{0}.mp3".format(i),
        bitrate = "192k",
        format = "mp3"
    )