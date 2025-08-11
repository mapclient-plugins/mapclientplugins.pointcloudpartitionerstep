from PySide6 import QtCore, QtWidgets


class GroupTableView(QtWidgets.QTableView):

    def __init__(self, parent):
        super().__init__(parent)
        self.setItemDelegateForColumn(1, PushButtonDelegate(self))
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def dropEvent(self, event):
        super().dropEvent(event)

        source_index = self.selectedIndexes()[0].row()
        target_index = self.indexAt(event.pos()).row()

        self.model().move_row(source_index, target_index)
        event.accept()

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.clearSelection()
        super().mousePressEvent(event)


class GroupModel(QtCore.QAbstractTableModel):

    def __init__(self, model_source, parent=None):
        super().__init__(parent)
        self._model_source = model_source

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemFlag.ItemIsDropEnabled

        index_flags = QtCore.Qt.ItemFlag.ItemIsDragEnabled | QtCore.Qt.ItemFlag.ItemIsDropEnabled | super().flags(index)
        if index.column() == 0:
            index_flags |= QtCore.Qt.ItemFlag.ItemIsEditable

        return index_flags

    def supportedDropActions(self):
        return QtCore.Qt.DropAction.MoveAction

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self._model_source.group_count()

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.ItemDataRole.DisplayRole or role == QtCore.Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                return self._model_source.group_data(index.row(), index.column())

        return None

    def setData(self, index, value, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return False

        if role == QtCore.Qt.ItemDataRole.EditRole:
            if index.column() == 0:
                self._model_source.set_group_data(index.row(), index.column(), value)
                return True

        return False

    def begin_add_group(self):
        row = self.rowCount()
        self.beginInsertRows(QtCore.QModelIndex(), row, row)

    def end_add_group(self):
        self.endInsertRows()

    def begin_remove_group(self, start_row, end_row=None):
        self.beginRemoveRows(QtCore.QModelIndex(), start_row, start_row if end_row is None else end_row)
        for row in range(self.rowCount()):
            self.parent().closePersistentEditor(self.index(row, 1))

    def end_remove_group(self):
        self.endRemoveRows()

    def move_row(self, source_row, target_row):
        self._model_source.move_group_data(source_row, target_row)


class PushButtonDelegate(QtWidgets.QStyledItemDelegate):
    button_clicked = QtCore.Signal(int)

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QPushButton(parent)
        editor.setText("sel.")
        editor.clicked.connect(lambda: self.button_clicked.emit(index.row()))
        return editor

    def paint(self, painter, option, index):
        if isinstance(self.parent(), QtWidgets.QAbstractItemView):
            self.parent().openPersistentEditor(index)

        super().paint(painter, option, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
