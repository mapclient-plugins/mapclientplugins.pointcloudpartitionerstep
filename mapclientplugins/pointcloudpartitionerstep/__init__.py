"""
MAP Client Plugin
"""

__version__ = '0.4.1'
__author__ = 'Timothy Salemink'
__stepname__ = 'Point Cloud Partitioner'
__location__ = 'https://github.com/mapclient-plugins/mapclientplugins.pointcloudpartitionerstep'

# import class that derives itself from the step mountpoint.
from mapclientplugins.pointcloudpartitionerstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
from . import resources_rc
