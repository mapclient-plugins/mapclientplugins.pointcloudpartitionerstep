"""
MAP Client Plugin
"""

__version__ = '0.2.0'
__author__ = 'Timothy Salemink'
__stepname__ = 'Point Cloud Partitioner'
__location__ = ''

# import class that derives itself from the step mountpoint.
from mapclientplugins.pointcloudpartitionerstep import step

# Import the resource file when the module is loaded,
# this enables the framework to use the step icon.
from . import resources_rc
