import numpy as np
from scipy.optimize import minimize

from PySide2 import QtWidgets

from opencmiss.zinc.status import OK as ZINC_OK
from opencmiss.zinc.node import Node
from opencmiss.zinc.field import Field
from opencmiss.zinchandlers.scenemanipulation import SceneManipulation

from mapclientplugins.electrodeprojectionstep.view.ui_electrodeprojectionwidget import Ui_ElectrodeProjectionWidget

PLAY_TEXT = 'Play'
STOP_TEXT = 'Stop'


class ElectrodeProjectionWidget(QtWidgets.QWidget):

    def __init__(self, model, parent=None):
        super(ElectrodeProjectionWidget, self).__init__(parent)
        self._ui = Ui_ElectrodeProjectionWidget()
        self._ui.setupUi(self)
        self._ui.sceneviewer_widget.set_context(model.get_context())
        self._model = model

        self._fiducial_marker_locations = []
        self._done_callback = None
        self._initialise_ui()
        self._setup_handlers()
        self._make_connections()

    def _graphics_initialized(self):
        """
        Callback for when SceneviewerWidget is initialised
        Set custom scene from model
        """
        sceneviewer = self._ui.sceneviewer_widget.get_zinc_sceneviewer()
        if sceneviewer is not None:
            self._model.load_settings()
            scene = self._model.get_scene()
            self._ui.sceneviewer_widget.set_scene(scene)
            self._view_all()

    def _make_connections(self):
        self._ui.sceneviewer_widget.graphics_initialized.connect(self._graphics_initialized)
        self._ui.done_button.clicked.connect(self._done_button_clicked)
        self._ui.viewAll_button.clicked.connect(self._view_all)
        self._ui.projectElectrodes_pushButton.clicked.connect(self._project_electrodes_clicked)
        self._ui.projectionDepth_spinBox.valueChanged.connect(self._projection_depth_value_changed)
        self._ui.projectionPointScale_doubleSpinBox.valueChanged.connect(self._projection_scale_factor_changed)

    def _setup_handlers(self):
        basic_handler = SceneManipulation()
        self._ui.sceneviewer_widget.register_handler(basic_handler)

    def _initialise_ui(self):
        self._ui.projectionDepth_spinBox.setValue(self._model.get_depth())
        self._ui.projectionPointScale_doubleSpinBox.setValue(self._model.get_z_scale_factor())

    def _update_ui(self):
        pass

    def _projection_depth_value_changed(self):
        value = self._ui.projectionDepth_spinBox.value()
        self._model.set_depth(value)

    def _projection_scale_factor_changed(self):
        value = self._ui.projectionPointScale_doubleSpinBox.value()
        self._model.set_z_scale_factor(value)

    def _project_electrodes_clicked(self):
        self._model.clear_projected_points()
        depth_value = self._ui.projectionDepth_spinBox.value()
        self._model.set_depth(depth_value)
        self._model.project()

    def register_done_execution(self, done_callback):
        self._done_callback = done_callback

    def _done_button_clicked(self):
        self._ui.dockWidget.setFloating(False)
        self._done_callback()

    def _get_field_module_and_all_nodes(self):
        scaffold_model = self._model.get_scaffold_model()
        region = scaffold_model.get_region()
        field_module = region.getFieldmodule()
        nodes = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        return field_module, nodes

    def _view_all(self):
        """
        Ask sceneviewer to show all of scene.
        """
        if self._ui.sceneviewer_widget.get_zinc_sceneviewer() is not None:
            self._ui.sceneviewer_widget.view_all()


def _get_node_numpy_array(field_cache, field_module, nodes, coordinates):
    field_module.beginChange()
    node_iter = nodes.createNodeiterator()
    node = node_iter.next()
    node_set_list = []
    while node.isValid():
        field_cache.setNode(node)
        _, xyz = coordinates.getNodeParameters(field_cache, -1, Node.VALUE_LABEL_VALUE, 1, 3)  # coordinates
        node_set_list.append(xyz)
        node = node_iter.next()
    field_module.endChange()
    return np.asarray(node_set_list)


def _set_node_parameters(field_cache, field_module, nodes, coordinates, transformed_nodes, numpy_array, rigid=True):
    field_module.beginChange()
    node_iter = nodes.createNodeiterator()
    node = node_iter.next()

    for n in range(len(transformed_nodes)):
        n_list = transformed_nodes[n].tolist()
        field_cache.setNode(node)
        if not rigid:
            new_n_list = [numpy_array[n][0], n_list[0], n_list[1]]
            result = coordinates.setNodeParameters(field_cache, -1, Node.VALUE_LABEL_VALUE, 1, new_n_list)
        else:
            result = coordinates.setNodeParameters(field_cache, -1, Node.VALUE_LABEL_VALUE, 1, n_list)
        if result == ZINC_OK:
            pass
        else:
            break
        node = node_iter.next()

    field_module.endChange()


def _rigid_transform(landmark, node):
    """

    :param landmark: a numpy array of fiducial landmark points on the image
    :param node: a numpy array selected nodes to compute the transform
    :return: transformed nodes
    """
    fitting = RigidFitting(**{'X': landmark, 'Y': node})
    TY, _ = fitting.fit()

    return TY, fitting


def _non_rigid_transform(landmark, node):
    """

    :param landmark: a numpy array of fiducial landmark points on the image
    :param node: a numpy array selected nodes to compute the transform
    :return: transformed nodes
    """
    fitting = DeformableFitting(**{'X': landmark, 'Y': node})
    TY, _ = fitting.fit()

    return TY, fitting


def rigid_transform_3d(A, B):
    assert len(A) == len(B)

    n1 = A.shape[1]  # total points
    n2 = B.shape[1]
    centroid_a = np.mean(A, axis=1)
    centroid_b = np.mean(B, axis=1)

    # centre the points
    AA = A - np.tile(centroid_a, (1, n1))
    BB = B - np.tile(centroid_b, (1, n2))

    # dot is matrix multiplication for array
    H = AA * BB.T

    U, S, Vt = np.linalg.svd(H)

    R = Vt.T * U.T

    # special reflection case
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T * U.T

    t = -R * centroid_a + centroid_b

    return R, t
