from setup import *
from sklearn import datasets
import sys
sys.path.append('PythonSrc') # For access to the python libraries
import hdf5_getters as getter

pp = pprint.PrettyPrinter(indent=2)


"""
Method to convert all hdf5 files into csv with 10,000 lines of format:
data:
key, mode, tempo, time_signature, loudness, *timbre*

target:
year

The indices of the two match up.

"""
def convert_to_csv():
    i = 0

    data = []
    target = []
    count = 0

    with open('data_no_timbre.csv', 'w+') as f:
        with open('target_no_timbre.csv', 'w+') as f2:
            writer = csv.writer(f)
            target_writer = csv.writer(f2)

            for root, dirs, files in os.walk(msd_subset_data_path):
                if count < 10:
                    files = glob.glob(os.path.join(root,'*.h5'))
                    for f in files:
                        try: # Opening is very prone to causing exceptions, we'll just skip file if exception is thrown
                            h5 = getter.open_h5_file_read(f)
                            year = getter.get_year(h5)
                            if year:
                                count +=1
                                print "Currently at " + str(count)
                                target.append([year])
                                row = []
                                
                                timbre = getter.get_segments_timbre(h5)
                                segstarts = getter.get_segments_start(h5)
                                btstarts = getter.get_beats_start(h5)
                                duration = getter.get_duration(h5)
                                end_of_fade_in = getter.get_end_of_fade_in(h5)
                                key = getter.get_key(h5)
                                key_confidence = getter.get_key_confidence(h5)
                                loudness = getter.get_loudness(h5)
                                start_of_fade_out = getter.get_start_of_fade_out(h5)
                                tempo = getter.get_tempo(h5)
                                time_signature = getter.get_time_signature(h5)
                                time_signature_confidence = getter.get_time_signature_confidence(h5)

                                h5.close() # VERY IMPORTANT

                                segstarts = np.array(segstarts).flatten()
                                btstarts = np.array(btstarts).flatten()

                                bttimbre = align_feats(timbre.T, segstarts, btstarts, duration, end_of_fade_in, key, key_confidence, loudness, start_of_fade_out, tempo, time_signature, time_signature_confidence)

                                if bttimbre is None:
                                    continue # Skip this track, some features broken

                                npicks, winsize, finaldim = 12, 12, 144  # Calculated by 12 * 12. 12 is fixed as number of dimensions.
                                processed_feats = extract_and_compress(bttimbre, npicks, winsize, finaldim)
                                n_p_feats = processed_feats.shape[0]

                                if processed_feats is None:
                                    continue # Skip this track, some features broken

                                row = processed_feats.flatten()
                                if len(row) != 12*144: # 12 dimensions * 144 features per dimension
                                    continue # Not enough features

                                year_row = np.array([year])

                                if row.any() and year_row.any():
                                    writer.writerow(row)
                                    target_writer.writerow(year_row)

                                i+=1

                            else:
                                h5.close()

                        except Exception:
                            pass



    print 'Finished!'
    return 


def align_feats(feats, segstarts, btstarts, duration, end_of_fade_in, key, key_confidence, loudness, start_of_fade_out, tempo, time_signature, time_signature_confidence):
    """
    MAIN FUNCTION: aligned whatever matrix of features is passed,
    one column per segment, and interpolate them to get features
    per beat.
    Note that btstarts could be anything, e.g. bar starts
    INPUT
       feats      - matrix of features, one column per segment
       segstarts  - segments starts in seconds,
                    dim must match feats # cols (flatten ndarray)
       btstarts   - beat starts in seconds (flatten ndarray)
       duration   - overall track duration in seconds
    RETURN
       btfeats    - features, one column per beat
                    None if there is a problem
    """
    if feats.shape[0] == 0 or feats.shape[1] == 0:
        return None
    if btstarts.shape[0] == 0 or segstarts.shape[0] == 0:
        return None

    warpmat = get_time_warp_matrix(segstarts, btstarts, duration, end_of_fade_in, key, key_confidence, loudness, start_of_fade_out, tempo, time_signature, time_signature_confidence)

    featchroma = np.dot(warpmat, feats.T).T
    if featchroma.shape[1] == 0:
        return None

    return featchroma


def get_time_warp_matrix(segstart, btstart, duration, end_of_fade_in, key, key_confidence, loudness, start_of_fade_out, tempo, time_signature, time_signature_confidence):
    """
    Used by create_beat_synchro_chromagram
    Returns a matrix (#beats,#segs)
    #segs should be larger than #beats, i.e. many events or segs
    happen in one beat.
    THIS FUNCTION WAS ORIGINALLY CREATED BY RON J. WEISS (Columbia/NYU/Google)
    """

    seglen = np.concatenate((segstart[9:], [duration], [end_of_fade_in], [key], [key_confidence], [loudness], [start_of_fade_out], [tempo], [time_signature], [time_signature_confidence])) - segstart
    btlen = np.concatenate((btstart[9:], [duration], [end_of_fade_in], [key], [key_confidence], [loudness], [start_of_fade_out], [tempo], [time_signature], [time_signature_confidence])) - btstart

    warpmat = np.zeros((len(segstart), len(btstart)))
    # iterate over beats (columns of warpmat)
    for n in xrange(len(btstart)):
        # beat start time and end time in seconds
        start = btstart[n]
        end = start + btlen[n]
        # np.nonzero returns index of nonzero elems
        # find first segment that starts after beat starts - 1
        try:
            start_idx = np.nonzero((segstart - start) >= 0)[0][0] - 1
        except IndexError:
            # no segment start after that beats, can happen close
            # to the end, simply ignore, maybe even break?
            # (catching faster than ckecking... it happens rarely?)
            break
        # find first segment that starts after beat ends
        segs_after = np.nonzero((segstart - end) >= 0)[0]
        if segs_after.shape[0] == 0:
            end_idx = start_idx
        else:
            end_idx = segs_after[0]
        # fill col of warpmat with 1 for the elem in between
        # (including start_idx, excluding end_idx)
        warpmat[start_idx:end_idx, n] = 1.
        # if the beat started after the segment, keep the proportion
        # of the segment that is inside the beat
        warpmat[start_idx, n] = 1. - ((start - segstart[start_idx])
                                 / seglen[start_idx])
        # if the segment ended after the beat ended, keep the proportion
        # of the segment that is inside the beat
        if end_idx - 1 > start_idx:
            warpmat[end_idx-1, n] = ((end - segstart[end_idx-1])
                                     / seglen[end_idx-1])
        # normalize so the 'energy' for one beat is one
        warpmat[:, n] /= np.sum(warpmat[:, n])
    # return the transpose, meaning (#beats , #segs)
    return warpmat.T


def extract_and_compress(btfeat,npicks,winsize,finaldim,seed=3232343,randproj=None):
    """
    From a btfeat matrix, usually 12xLENGTH
    Extracts 'npicks' windows of size 'winsize' equally spaced
    Flatten these picks, pass them through a random projection, final
    size is 'finaldim'
    Returns matrix npicks x finaldim, or 0 x finaldim if problem
    (btfeats not long enough for instance)
    We could return less than npicks if not long enough!
    For speed, we can compute the random projection once and pass it as an
    argument.
    """

    # features length
    ftlen = btfeat.shape[1]
    ndim = btfeat.shape[0]
    # too small case
    if ftlen < winsize:
        return np.zeros((0,finaldim))
    # random projection
    if randproj is None:
        randproj = proj_point5(ndim * winsize, finaldim, seed=seed)
    # not big enough for number of picks, last one too large return just 1
    if ftlen < int(ftlen * (npicks *1./(npicks+1))) + winsize:
        pos = int( (ftlen-winsize) /  2.) # middle
        picks = [ btfeat[:,pos:pos+winsize] ]
    # regular case, picks will contain npicks
    else:
        picks = []
        for k in range(1,npicks+1):
            pos = int(ftlen * (k *1./(npicks+1)))
            picks.append( btfeat[:,pos:pos+winsize] )
    # project / compress these
    projections = map(lambda x: np.dot(x.flatten(),randproj).reshape(1,finaldim), picks)
    return np.concatenate(projections)


def proj_point5(dimFrom,dimTo,seed=3232343):
    """
    Creates a matrix dimFrom x dimTo where each element is
    .5 or -.5 with probability 1/2 each
    For theoretical results using this projection see:
      D. Achlioptas. Database-friendly random projections.
      In Symposium on Principles of Database Systems
      (PODS), pages 274-281, 2001.
      http://portal.acm.org/citation.cfm?doid=375551.375608
    """
    if dimFrom == dimTo:
        return np.eye(dimFrom)
    np.random.seed(seed)
    return np.random.randint(2,size=(dimFrom,dimTo)) - .5



convert_to_csv()