
from PySide6.QtWidgets import (
    QComboBox, QGridLayout, QLabel,
    QPushButton, QSpinBox, QWidget, QVBoxLayout, QDialog
)
import Class.seedSettings
from Class.seedSettings import ProgressionChainSelect
from Module.progressionPoints import ProgressionPoints


class ProgressionDisplayWidget(QDialog):
    def __init__(self,progress_info : ProgressionPoints):
        super().__init__()
        self.progress_info = progress_info
        self.setWindowTitle("Progression")
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)

        box = QGridLayout()

        hint_label = QLabel("Hint Thresholds:")
        box.addWidget(hint_label,0,0)

        for x in range(18):
            hint_threshold_label = QLabel(str(self.progress_info.get_point_threshold(x)))
            box.addWidget(hint_threshold_label,0,x+1)

        world_names = self.progress_info.get_world_options()
        world_count = 1
        for w in world_names:
            box.addWidget(QLabel(w),world_count,0)
            for x in range(self.progress_info.get_num_cp_for_world(w)):
                box.addWidget(QLabel(str(self.progress_info.get_cp_for_world(w,x))),world_count,x+1)
            world_count+=1


        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        box.addWidget(close_button,world_count,0)

        self.setLayout(box)


class ProgressionWidget(QWidget):
    def __init__(self, settings, setting_name):
        super().__init__()
        self.settings = settings
        self.setting_name = setting_name
        setting: ProgressionChainSelect = Class.seedSettings.settings_by_name[setting_name]

        self.world_options = setting.progression.get_world_options()

        self.full_layout = QVBoxLayout()

        # make a combo box for worlds
        self.world_select = QComboBox()
        self.world_select.addItems(self.world_options)
        # self.world_select.lineEdit().setReadOnly(True)
        self.world_select.currentIndexChanged.connect(lambda index: self._change_visibility(self.world_options[index]))
        self.full_layout.addWidget(self.world_select)

        self.tier2_selects = {}
        self.tier3_selects = {}
        spin_boxes = []
        for w in self.world_options:
            self.tier3_selects[w] = []
            world_cp_select_labels = []
            for w_cp_index in range(setting.progression.get_num_cp_for_world(w)):
                world_cp_select_labels.append(setting.progression.get_cp_label_for_world(w,w_cp_index))
                spin_box = QSpinBox()
                spin_box.setRange(0,7)
                spin_box.setSingleStep(1)
                spin_box.setValue(setting.progression.get_cp_for_world(w,w_cp_index))
                spin_box.valueChanged.connect(lambda value, world=w,world_cp=w_cp_index: self._change_setting(world,world_cp,value))
                # spin_box.lineEdit().setReadOnly(True)
                self.tier3_selects[w].append(spin_box)
                spin_boxes.append(spin_box)
            world_cp_select_box = QComboBox()
            world_cp_select_box.addItems(world_cp_select_labels)
            world_cp_select_box.setCurrentIndex(0)
            world_cp_select_box.currentIndexChanged.connect(lambda index,world=w: self._change_visibility_again(world,index))
            # world_cp_select_box.lineEdit().setReadOnly(True)
            self.tier2_selects[w] = world_cp_select_box
            self.full_layout.addWidget(world_cp_select_box)
        
        for s in spin_boxes:
            self.full_layout.addWidget(s)

        self.world_select.setCurrentIndex(1)
        self.world_select.setCurrentIndex(0)


        self.full_layout.addWidget(QLabel("Hint Thresholds"))

        # widgets for the hint thresholds
        self.threshold_select = QComboBox()
        hint_texts = []
        for x in range(0,18):
            hint_texts.append(f"Hint Threshold {x+1}")
        self.threshold_select.addItems(hint_texts)
        self.threshold_select.currentIndexChanged.connect(lambda index: self._change_threshold_visibility(index))
        self.full_layout.addWidget(self.threshold_select)

        self.threshold_values = {}
        for x in range(0,18):
            spin_box = QSpinBox()
            spin_box.setRange(0,9)
            spin_box.setSingleStep(1)
            spin_box.setValue(setting.progression.get_point_threshold(x))
            spin_box.valueChanged.connect(lambda value, hint_index=x: self._change_threshold(hint_index,value))
            # spin_box.lineEdit().setReadOnly(True)
            self.threshold_values[x] = spin_box
            self.full_layout.addWidget(spin_box)
        
        self.threshold_select.setCurrentIndex(1)
        self.threshold_select.setCurrentIndex(0)

        display_button = QPushButton("Show All")
        display_button.clicked.connect(lambda : ProgressionDisplayWidget(Class.seedSettings.settings_by_name[self.setting_name].progression).exec())
        self.full_layout.addWidget(display_button)

        self.setLayout(self.full_layout)

    def _change_threshold(self,index,value):
        setting: ProgressionChainSelect = Class.seedSettings.settings_by_name[self.setting_name]
        setting.progression.set_point_threshold(index,value)
        self.settings.set(self.setting_name,setting.progression.get_compressed())

    def _change_threshold_visibility(self,index):
        for w in self.threshold_values:
            self.threshold_values[w].setVisible(w==index)
    
    def _change_setting(self,world,world_cp,value):
        setting: ProgressionChainSelect = Class.seedSettings.settings_by_name[self.setting_name]
        setting.progression.set_cp_for_world(world,world_cp,value)
        self._update_spinboxes()
        self.settings.set(self.setting_name,setting.progression.get_compressed())

    def _change_visibility(self,selected_world):
        for w in self.tier2_selects:
            self.tier2_selects[w].setVisible(w==selected_world)
        self._change_visibility_again(selected_world,0)

    def _change_visibility_again(self,selected_world,selected_cp_index):
        # only change visibility of tier 3
        for w in self.tier3_selects:
            for s in self.tier3_selects[w]:
                s.setVisible(False)
        self.tier3_selects[selected_world][selected_cp_index].setVisible(True)

    def _update_spinboxes(self):
        setting: ProgressionChainSelect = Class.seedSettings.settings_by_name[self.setting_name]
        for w in self.threshold_values:
            self.threshold_values[w].setValue(setting.progression.get_point_threshold(w))
        for w in self.world_options:
            for w_cp_index in range(setting.progression.get_num_cp_for_world(w)):
                self.tier3_selects[w][w_cp_index].setValue(setting.progression.get_cp_for_world(w,w_cp_index))