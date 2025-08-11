"""
MAP Client Plugin Step
"""
import os
import json

from PySide6 import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint

from mapclientplugins.pointcloudpartitionerstep.configuredialog import ConfigureDialog
from mapclientplugins.pointcloudpartitionerstep.model.pointcloudpartitionermodel import PointCloudPartitionerModel
from mapclientplugins.pointcloudpartitionerstep.view.pointcloudpartitionerwidget import PointCloudPartitionerWidget


class PointCloudPartitionerStep(WorkflowStepMountPoint):
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

    def __init__(self, location):
        super(PointCloudPartitionerStep, self).__init__('Point Cloud Partitioner', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Morphometric'
        self._icon = QtGui.QImage(':/pointcloudpartitionerstep/images/pointcloudicon.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort([('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                       'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                       'http://physiomeproject.org/workflow/1.0/rdf-schema#exf_file'),
                      ('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                       'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                       'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location')
                      ])
        self._config = {
            'identifier': ''
        }

        self._view = None
        self._model = None
        self._source_points = None
        self._segmentation_surface = None
        self._output_points = None
        self._input_hash = None

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        if self._source_points is None:
            raise RuntimeError('Source points not set. Please set the source points before executing the step.')

        input_hash = hash(self._source_points + '' if self._segmentation_surface is None else self._segmentation_surface)
        if self._view is None or input_hash != self._input_hash:
            self._model = PointCloudPartitionerModel()
            self._view = PointCloudPartitionerWidget(self._model)
            self._view.register_done_execution(self._my_done_execution)
            self._input_hash = input_hash

        self._view.set_location(os.path.join(self._location, self._config['identifier']))
        self._view.clear()
        self._view.load(self._source_points, self._segmentation_surface)
        self._setCurrentWidget(self._view)

    def _my_done_execution(self):
        self._doneExecution()

    def setPortData(self, index, data_in):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        """
        if index == 0:
            self._source_points = data_in
        elif index == 2:
            self._segmentation_surface = data_in

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        """
        return self._view.get_output_file()

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.set_config(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.get_config()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def serialize(self):
        """
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.set_config(self._config)
        self._configured = d.validate()
