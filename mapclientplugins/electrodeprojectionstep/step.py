"""
MAP Client Plugin Step
"""
import json

from PySide2 import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.electrodeprojectionstep.configuredialog import ConfigureDialog
from mapclientplugins.electrodeprojectionstep.model.master import ElectrodeProjectionModel
from mapclientplugins.electrodeprojectionstep.view.view import ElectrodeProjectionWidget


class ElectrodeProjectionStep(WorkflowStepMountPoint):
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

    def __init__(self, location):
        super(ElectrodeProjectionStep, self).__init__('Electrode Projection', location)
        self._configured = False  # A step cannot be executed until it has been configured.
        self._category = 'Fitting'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/electrodeprojectionstep/images/fitting.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#time_labelled_electrode_marker_locations'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#mesh_description'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#2d_image_dimension'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#time_based_electrode_scaffold_positions'))
        # Port data:
        self._electrode_positions_on_plane = None  # electrode_positions
        self._scaffold_description = None  # scaffold_description
        self._electrode_positions_projected = None  # time_based_electrode_scaffold_positions
        self._image_dimensions = None  # 2d_image_dimension
        # Config:
        self._config = {'identifier': ''}

        self._model = None
        self._view = None

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.
        self._model = ElectrodeProjectionModel(
            self._scaffold_description,
            self._electrode_positions_on_plane,
            self._image_dimensions)

        self._view = ElectrodeProjectionWidget(self._model)
        self._view.register_done_execution(self._my_done_execution)
        self._setCurrentWidget(self._view)

    def _my_done_execution(self):
        self._electrode_positions_projected = self._model.get_electrode_positions_description()
        self._model.done()
        self._view = None
        self._model = None
        self._doneExecution()

    def setPortData(self, index, dataIn):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.

        :param index: Index of the port to return.
        :param dataIn: The data to set for the port at the given index.
        """
        if index == 0:
            self._electrode_positions_on_plane = dataIn  # electrode_positions
        elif index == 1:
            self._scaffold_description = dataIn  # scaffold_parameters
        elif index == 2:
            self._image_dimensions = dataIn  # 2d_image_dimension

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.

        :param index: Index of the port to return.
        """
        return self._electrode_positions_projected  # time_based_electrode_scaffold_positions

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
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

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

        :param string: JSON representation of the configuration in a string.
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog(self._main_window)
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
