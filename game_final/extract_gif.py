import os
from PIL import Image
#https://gist.github.com/revolunet/848913
def extractFrames(inGif, outFolder):
    frame = Image.open(inGif)
    nframes = 0
    while frame:
        frame.save( '%s/%s-%s.png' % (outFolder, os.path.basename(inGif), nframes ))
        nframes += 1
        try:
            frame.seek( nframes )
        except EOFError:
            break;
    return True

extractFrames("explosion.gif", "explosion_gif")