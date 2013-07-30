"""Unit tests for loader module."""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import os
from collections import Counter

import numpy as np
import numpy.random as rnd
import pandas as pd
import shutil
from nose.tools import with_setup

from klustaviewa.dataio.tests.mock_data import (
                            nspikes, nclusters, nsamples, nchannels, fetdim)
from klustaviewa.dataio import (HDF5Loader, HDF5Writer, select, get_indices,
    check_dtype, check_shape, get_array, load_text)
from klustaviewa.utils.userpref import USERPREF


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
def test_hdf5_loader1():
    # Open the mock data.
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mockdata')
    filename = os.path.join(dir, 'test.xml')
    
    # Convert in HDF5.
    with HDF5Writer(filename) as writer:
        writer.convert()
        
    # Open the HDF5 file.
    filename = os.path.join(dir, 'test.main.h5')
    l = HDF5Loader(filename=filename)
    
    # Select cluster.
    cluster = 3
    l.select(clusters=[cluster])
    
    # Get clusters.
    clusters = l.get_clusters('all')
    nspikes = np.sum(clusters == cluster)
    
    # Get the spike times.
    spiketimes = l.get_spiketimes()
    assert np.all(spiketimes <= 60)
    
    # Get features.
    features = l.get_features()
    spikes = l.get_spikes()
    # Assert the indices in the features Pandas object correspond to the
    # spikes in the selected cluster.
    assert np.array_equal(features.index, spikes)
    # Assert the array has the right number of spikes.
    assert features.shape[0] == nspikes
    assert l.fetdim == fetdim
    assert l.nextrafet == 1
    
    # Get masks.
    masks = l.get_masks()
    assert masks.values.dtype == np.uint8
    assert masks.shape[0] == nspikes
    
    # Get waveforms.
    waveforms = l.get_waveforms()
    assert waveforms.shape == (nspikes, nchannels * nsamples)
    
    l.close()
    
    