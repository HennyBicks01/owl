from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QLabel, QPushButton, QGroupBox, QTabWidget, QWidget, QSpinBox, 
                             QCheckBox, QDialogButtonBox, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setModal(True)
        self.config = self.load_config()
        self.current_conversation = None
        self.initUI()
        
    def load_config(self):
        """Load configuration from config.json"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        default_config = {
            'voice_type': 'Azure Voice',
            'voice_name': 'en-US-AnaNeural',
            'sleep_timer': 30,
            'personality_preset': 'ova',
            'display_mode': 'bubble',
            'max_conversation_pairs': 10,  # Default to 10 pairs (20 messages)
            'save_conversation_history': True,  # Default to saving history
            'enable_random_actions': True,
            'min_action_interval': 5,
            'max_action_interval': 10,
            'enabled_actions': {
                'take_flight': True,
                'look_around': True,
                'dance': True,
                'screech': True
            }
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    logger.info(f"Loaded config: {loaded_config}")
                    return loaded_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        
        logger.info("Using default config")
        return default_config.copy()
    
    def save_config(self):
        """Save configuration to config.json"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        try:
            logger.info(f"Saving config: {self.config}")
            with open(config_path, 'w') as f:
                json.dump(self.config, f)
            logger.info("Config saved successfully")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get_available_presets(self):
        """Get list of available preset files"""
        presets_dir = os.path.join(os.path.dirname(__file__), 'presets')
        presets = []
        if os.path.exists(presets_dir):
            for file in os.listdir(presets_dir):
                if file.endswith('.txt'):
                    presets.append(os.path.splitext(file)[0])
        logger.info(f"Available presets: {presets}")
        return sorted(presets)

    def get_available_voices(self):
        """Get list of available voices"""
        edge_voices = [
            # Rename Ana to Ova
            ("Ova", "en-US-AnaNeural"),
            # US Voices
            ("Aria (US)", "en-US-AriaNeural"),
            ("Christopher (US)", "en-US-ChristopherNeural"),
            ("Eric (US)", "en-US-EricNeural"),
            ("Guy (US)", "en-US-GuyNeural"),
            ("Jenny (US)", "en-US-JennyNeural"),
            ("Michelle (US)", "en-US-MichelleNeural"),
            ("Roger (US)", "en-US-RogerNeural"),
            ("Steffan (US)", "en-US-SteffanNeural"),
            # US Multilingual
            ("Ava (US Multi)", "en-US-AvaMultilingualNeural"),
            ("Andrew (US Multi)", "en-US-AndrewMultilingualNeural"),
            ("Emma (US Multi)", "en-US-EmmaMultilingualNeural"),
            ("Brian (US Multi)", "en-US-BrianMultilingualNeural"),
            # UK Voices
            ("Libby (UK)", "en-GB-LibbyNeural"),
            ("Maisie (UK)", "en-GB-MaisieNeural"),
            ("Ryan (UK)", "en-GB-RyanNeural"),
            ("Sonia (UK)", "en-GB-SoniaNeural"),
            ("Thomas (UK)", "en-GB-ThomasNeural"),
            # Australian Voices
            ("Natasha (AU)", "en-AU-NatashaNeural"),
            ("William (AU)", "en-AU-WilliamNeural"),
            # Canadian Voices
            ("Clara (CA)", "en-CA-ClaraNeural"),
            ("Liam (CA)", "en-CA-LiamNeural"),
            # Irish Voices
            ("Connor (IE)", "en-IE-ConnorNeural"),
            ("Emily (IE)", "en-IE-EmilyNeural"),
            # Indian Voices
            ("Neerja (IN)", "en-IN-NeerjaNeural"),
            ("Neerja Expressive (IN)", "en-IN-NeerjaExpressiveNeural"),
            ("Prabhat (IN)", "en-IN-PrabhatNeural"),
            # South African Voices
            ("Leah (ZA)", "en-ZA-LeahNeural"),
            ("Luke (ZA)", "en-ZA-LukeNeural"),
            # Other Regional Voices
            ("Asilia (KE)", "en-KE-AsiliaNeural"),
            ("Chilemba (KE)", "en-KE-ChilembaNeural"),
            ("Mitchell (NZ)", "en-NZ-MitchellNeural"),
            ("Molly (NZ)", "en-NZ-MollyNeural"),
            ("Abeo (NG)", "en-NG-AbeoNeural"),
            ("Ezinne (NG)", "en-NG-EzinneNeural"),
            ("James (PH)", "en-PH-JamesNeural"),
            ("Rosa (PH)", "en-PH-RosaNeural"),
            ("Luna (SG)", "en-SG-LunaNeural"),
            ("Wayne (SG)", "en-SG-WayneNeural"),
            ("Elimu (TZ)", "en-TZ-ElimuNeural"),
            ("Imani (TZ)", "en-TZ-ImaniNeural")
        ]
        
        # Get Windows voices
        try:
            engine = pyttsx3.init()
            windows_voices = [(voice.name, voice.id) for voice in engine.getProperty('voices')]
            engine.stop()
        except:
            windows_voices = []
            
        return edge_voices + windows_voices
    
    def initUI(self):
        layout = QVBoxLayout()
        
        # Create tabs
        tabs = QTabWidget()
        
        # General Settings Tab
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        
        # Preset Selection Group
        preset_group = QGroupBox("System Preset")
        preset_group_layout = QHBoxLayout()
        
        # Preset Selection
        self.preset_selection = QComboBox()
        self.preset_selection.addItems(self.get_available_presets())
        preset_group_layout.addWidget(QLabel("Preset:"))
        preset_group_layout.addWidget(self.preset_selection)
        
        preset_group.setLayout(preset_group_layout)
        general_layout.addWidget(preset_group)
        
        # Display Mode Group
        display_group = QGroupBox("Display Settings")
        display_group_layout = QHBoxLayout()
        
        # Display Mode Selection
        self.display_mode = QComboBox()
        self.display_mode.addItems(["Speech Bubble", "Chat Window", "No Display"])
        display_group_layout.addWidget(QLabel("Display Mode:"))
        display_group_layout.addWidget(self.display_mode)
        
        display_group.setLayout(display_group_layout)
        general_layout.addWidget(display_group)
        
        general_layout.addStretch()
        general_tab.setLayout(general_layout)

        # Voice Settings Tab
        voice_tab = QWidget()
        self.setupVoiceTab(voice_tab)
        
        # Behavior Settings Tab
        behavior_tab = QWidget()
        self.setupBehaviorTab(behavior_tab)
        
        # History Settings Tab
        history_tab = QWidget()
        self.setupHistoryTab(history_tab)
        
        # Add tabs
        tabs.addTab(general_tab, "General")
        tabs.addTab(voice_tab, "Voice")
        tabs.addTab(behavior_tab, "Behavior")
        tabs.addTab(history_tab, "History")
        layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Load saved settings
        self.loadSavedSettings()

    def setupVoiceTab(self, tab):
        """Setup the voice settings tab"""
        voice_layout = QVBoxLayout()
        
        # Voice Selection Group
        voice_group = QGroupBox("Voice Selection")
        voice_group_layout = QVBoxLayout()
        
        # Voice Type Selection
        type_layout = QHBoxLayout()
        self.voice_type = QComboBox()
        self.voice_type.addItems(["Azure Voice", "Windows Voice"])
        self.voice_type.currentTextChanged.connect(self.onVoiceTypeChanged)
        type_layout.addWidget(QLabel("Voice Type:"))
        type_layout.addWidget(self.voice_type)
        
        # Voice Selection
        voice_selection_layout = QHBoxLayout()
        self.voice_selection = QComboBox()
        voice_selection_layout.addWidget(QLabel("Voice:"))
        voice_selection_layout.addWidget(self.voice_selection)
        
        voice_group_layout.addLayout(type_layout)
        voice_group_layout.addLayout(voice_selection_layout)
        voice_group.setLayout(voice_group_layout)
        voice_layout.addWidget(voice_group)
        
        voice_layout.addStretch()
        tab.setLayout(voice_layout)

    def setupBehaviorTab(self, tab):
        """Setup the behavior settings tab"""
        layout = QVBoxLayout()
        
        # Sleep Timer Group
        sleep_group = QGroupBox("Sleep Timer")
        sleep_layout = QHBoxLayout()
        
        sleep_layout.addWidget(QLabel("Sleep After (seconds):"))
        self.sleep_timer = QSpinBox()
        self.sleep_timer.setRange(5, 3600)
        self.sleep_timer.setValue(self.config.get('sleep_timer', 60))
        sleep_layout.addWidget(self.sleep_timer)
        
        sleep_group.setLayout(sleep_layout)
        layout.addWidget(sleep_group)
        
        # Random Actions Group
        random_group = QGroupBox("Random Actions")
        random_layout = QVBoxLayout()
        
        # Enable random actions
        self.enable_random = QCheckBox("Enable Random Actions")
        self.enable_random.setChecked(self.config.get('enable_random_actions', True))
        random_layout.addWidget(self.enable_random)
        
        # Interval settings
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Action Interval (seconds):"))
        
        self.min_interval = QSpinBox()
        self.min_interval.setRange(1, 3600)
        self.min_interval.setValue(self.config.get('min_action_interval', 5))
        interval_layout.addWidget(self.min_interval)
        
        interval_layout.addWidget(QLabel("to"))
        
        self.max_interval = QSpinBox()
        self.max_interval.setRange(1, 3600)
        self.max_interval.setValue(self.config.get('max_action_interval', 10))
        interval_layout.addWidget(self.max_interval)
        
        random_layout.addLayout(interval_layout)
        
        # Action selection
        action_layout = QVBoxLayout()
        
        self.action_checkboxes = {}
        default_actions = self.config.get('enabled_actions', {
            'take_flight': True,
            'look_around': True,
            'dance': True,
            'screech': True
        })
        
        for action, label in [
            ('take_flight', 'Take Flight'),
            ('look_around', 'Look Around'),
            ('dance', 'Dance'),
            ('screech', 'Screech')
        ]:
            checkbox = QCheckBox(label)
            checkbox.setChecked(default_actions.get(action, True))
            self.action_checkboxes[action] = checkbox
            action_layout.addWidget(checkbox)
        
        random_layout.addLayout(action_layout)
        random_group.setLayout(random_layout)
        layout.addWidget(random_group)
        
        layout.addStretch()
        tab.setLayout(layout)

    def setupHistoryTab(self, tab):
        """Setup the history settings tab"""
        layout = QVBoxLayout()
        
        # Conversation History Group
        history_group = QGroupBox("Conversation Memory")
        history_layout = QVBoxLayout()
        
        # Save History Toggle
        save_history_layout = QHBoxLayout()
        self.save_history = QComboBox()
        self.save_history.addItems(["Save History", "Don't Save"])
        save_history_layout.addWidget(QLabel("Save History:"))
        save_history_layout.addWidget(self.save_history)
        
        # History Length Setting
        history_length_layout = QHBoxLayout()
        self.history_length = QSpinBox()
        self.history_length.setMinimum(1)
        self.history_length.setMaximum(50)  # Max 50 pairs (100 messages)
        self.history_length.setValue(self.config.get('max_conversation_pairs', 10))
        self.history_length.setSuffix(" pairs")
        history_length_layout.addWidget(QLabel("Remember last:"))
        history_length_layout.addWidget(self.history_length)
        
        history_layout.addLayout(save_history_layout)
        history_layout.addLayout(history_length_layout)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # Conversation Management Group
        convo_group = QGroupBox("Conversation Management")
        convo_layout = QVBoxLayout()
        
        # Table for conversations
        self.convo_table = QTableWidget()
        self.convo_table.setColumnCount(4)  # Select, Number, Last Message, Delete
        self.convo_table.setHorizontalHeaderLabels(["", "Conversation", "Last Message", ""])
        self.convo_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.convo_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.convo_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)
        self.convo_table.setColumnWidth(0, 30)  # Width for checkbox
        self.convo_table.setColumnWidth(3, 30)  # Width for delete button
        
        # Load conversations into table
        self.load_conversations()
        
        # Buttons for managing conversations
        button_layout = QHBoxLayout()
        new_convo_btn = QPushButton("New Conversation")
        clear_all_btn = QPushButton("Clear All")
        new_convo_btn.clicked.connect(self.new_conversation)
        clear_all_btn.clicked.connect(self.clear_all_conversations)
        
        button_layout.addWidget(new_convo_btn)
        button_layout.addWidget(clear_all_btn)
        
        convo_layout.addWidget(self.convo_table)
        convo_layout.addLayout(button_layout)
        convo_group.setLayout(convo_layout)
        layout.addWidget(convo_group)
        
        layout.addStretch()
        tab.setLayout(layout)

    def load_conversations(self):
        """Load conversations into the table"""
        self.convo_table.setRowCount(0)
        history_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'history')
        
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
            
        # Get current conversation from config
        current_convo = self.config.get('current_conversation')
        files = sorted(os.listdir(history_dir))
        json_files = [f for f in files if f.endswith('.json')]
        
        # If no current conversation is set or it doesn't exist, select the first one
        if not current_convo or current_convo not in json_files:
            if json_files:
                current_convo = json_files[0]
                self.config['current_conversation'] = current_convo
                self.save_config()
            
        for file in json_files:
            try:
                with open(os.path.join(history_dir, file), 'r') as f:
                    convo = json.load(f)
                    
                row = self.convo_table.rowCount()
                self.convo_table.insertRow(row)
                
                # Add select checkbox
                checkbox = QCheckBox()
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                checkbox_widget.setLayout(checkbox_layout)
                if file == current_convo:
                    checkbox.setChecked(True)
                    self.current_conversation = file
                checkbox.clicked.connect(lambda checked, f=file: self.on_checkbox_clicked(f))
                self.convo_table.setCellWidget(row, 0, checkbox_widget)
                
                # Just show the number, not the .json extension
                convo_num = file.split('.')[0]
                self.convo_table.setItem(row, 1, QTableWidgetItem(convo_num))
                
                # Get last message or show "Empty Conversation"
                last_msg = convo[-1]['content'] if convo else "Empty Conversation"
                last_msg = (last_msg[:50] + '...') if len(last_msg) > 50 else last_msg
                self.convo_table.setItem(row, 2, QTableWidgetItem(last_msg))
                
                # Add delete button
                delete_btn = QPushButton("🗑")
                delete_btn.setFixedWidth(25)
                delete_btn.clicked.connect(lambda _, f=file: self.delete_conversation(f))
                delete_widget = QWidget()
                delete_layout = QHBoxLayout(delete_widget)
                delete_layout.addWidget(delete_btn)
                delete_layout.setAlignment(Qt.AlignCenter)
                delete_layout.setContentsMargins(0, 0, 0, 0)
                delete_widget.setLayout(delete_layout)
                self.convo_table.setCellWidget(row, 3, delete_widget)
                
            except Exception as e:
                logger.error(f"Error loading conversation {file}: {e}")

    def on_checkbox_clicked(self, file_name):
        """Handle checkbox selection"""
        self.current_conversation = file_name
        self.switch_conversation()
        
        # Update all other checkboxes
        for row in range(self.convo_table.rowCount()):
            checkbox_widget = self.convo_table.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.layout().itemAt(0).widget()
                convo_num = self.convo_table.item(row, 1).text()
                checkbox.setChecked(f"{convo_num}.json" == file_name)

    def switch_conversation(self):
        """Switch to the selected conversation"""
        if self.current_conversation:
            # Update config with current conversation
            self.config['current_conversation'] = self.current_conversation
            # Save config immediately
            self.save_config()
            # Reload the conversation in voice assistant
            if hasattr(self.parent(), 'voice_assistant'):
                self.parent().voice_assistant.reload_config()

    def delete_conversation(self, file_name):
        """Delete a conversation file"""
        history_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'history')
        file_path = os.path.join(history_dir, file_name)
        
        try:
            # Delete the file
            os.remove(file_path)
            
            # Find another conversation or create new one
            existing_files = [f for f in os.listdir(history_dir) if f.endswith('.json')]
            if existing_files:
                # Switch to the first available conversation
                self.current_conversation = existing_files[0]
                self.config['current_conversation'] = self.current_conversation
                self.save_config()
            else:
                # No conversations left, create a new one
                self.new_conversation()
            
            # Refresh the table
            self.load_conversations()
            
            # Reload voice assistant
            if hasattr(self.parent(), 'voice_assistant'):
                self.parent().voice_assistant.reload_config()
        except Exception as e:
            logger.error(f"Error deleting conversation {file_name}: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Could not delete conversation: {str(e)}")

    def new_conversation(self):
        """Start a new conversation"""
        history_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'history')
        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
            
        # Find next available number
        existing_files = [f for f in os.listdir(history_dir) if f.endswith('.json')]
        next_num = 1
        while f"{next_num}.json" in existing_files:
            next_num += 1
            
        # Create new empty conversation file
        new_file = f"{next_num}.json"
        with open(os.path.join(history_dir, new_file), 'w') as f:
            json.dump([], f)
            
        # Set as current conversation
        self.current_conversation = new_file
        self.config['current_conversation'] = new_file
        self.save_config()
        
        # Refresh table
        self.load_conversations()

    def clear_all_conversations(self):
        """Clear all conversation files"""
        history_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'history')
        
        try:
            # Ask for confirmation
            from PyQt5.QtWidgets import QMessageBox
            reply = QMessageBox.question(self, "Clear All", 
                                       "Are you sure you want to delete all conversations?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # Delete all json files
                for file in os.listdir(history_dir):
                    if file.endswith('.json'):
                        os.remove(os.path.join(history_dir, file))
                
                # Create and select new conversation
                self.new_conversation()
                
                # Reload voice assistant
                if hasattr(self.parent(), 'voice_assistant'):
                    self.parent().voice_assistant.reload_config()
        except Exception as e:
            logger.error(f"Error clearing all conversations: {e}")
            QMessageBox.warning(self, "Error", f"Could not clear all conversations: {str(e)}")

    def loadSavedSettings(self):
        """Load and apply saved settings"""
        voice_type = self.config.get('voice_type', 'Azure Voice')
        voice_name = self.config.get('voice_name', 'en-US-AnaNeural')
        preset = self.config.get('personality_preset', 'ova')
        display_mode = self.config.get('display_mode', 'bubble')
        save_history = self.config.get('save_conversation_history', True)
        
        # Set preset
        index = self.preset_selection.findText(preset)
        if index >= 0:
            self.preset_selection.setCurrentIndex(index)
        
        # Set display mode
        mode_map = {'bubble': 'Speech Bubble', 'chat': 'Chat Window', 'none': 'No Display'}
        mode_text = mode_map.get(display_mode, 'Speech Bubble')
        index = self.display_mode.findText(mode_text)
        if index >= 0:
            self.display_mode.setCurrentIndex(index)
        
        # Set history settings
        self.save_history.setCurrentText("Save History" if save_history else "Don't Save")
        self.history_length.setValue(self.config.get('max_conversation_pairs', 10))
        
        # Set voice type
        index = self.voice_type.findText(voice_type)
        if index >= 0:
            self.voice_type.setCurrentIndex(index)
        
        # Populate voice selection
        self.onVoiceTypeChanged(voice_type)
        
        # Set voice name
        index = self.voice_selection.findText(voice_name)
        if index >= 0:
            self.voice_selection.setCurrentIndex(index)

    def onVoiceTypeChanged(self, voice_type):
        self.voice_selection.clear()
        if voice_type == "Azure Voice":
            voices = self.get_available_voices()
            azure_voices = [voice for voice in voices if voice[1].startswith("en-")]
            self.voice_selection.addItems([voice[0] for voice in azure_voices])
        else:  # Windows Voice
            import pyttsx3
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            self.voice_selection.addItems([voice.name for voice in voices])
            engine.stop()
            
    def accept(self):
        """Called when Save button is clicked"""
        logger.info("Save button clicked")
        
        # Update config with current values
        self.config['voice_type'] = self.voice_type.currentText()
        self.config['voice_name'] = self.getSelectedVoice()
        self.config['sleep_timer'] = self.sleep_timer.value()
        self.config['personality_preset'] = self.preset_selection.currentText()
        
        # Map display mode text to config value
        mode_map = {'Speech Bubble': 'bubble', 'Chat Window': 'chat', 'No Display': 'none'}
        self.config['display_mode'] = mode_map.get(self.display_mode.currentText(), 'bubble')
        
        # Save history settings
        self.config['save_conversation_history'] = (self.save_history.currentText() == "Save History")
        self.config['max_conversation_pairs'] = self.history_length.value()
        
        # Add random action settings
        self.config['enable_random_actions'] = self.enable_random.isChecked()
        self.config['min_action_interval'] = self.min_interval.value()
        self.config['max_action_interval'] = self.max_interval.value()
        self.config['enabled_actions'] = {
            action: checkbox.isChecked()
            for action, checkbox in self.action_checkboxes.items()
        }
        
        # Save current conversation if one is selected
        if self.current_conversation:
            self.config['current_conversation'] = self.current_conversation
        
        # Save config
        self.save_config()
        
        # Call parent accept to close dialog
        super().accept()
    
    def getSelectedVoice(self):
        """Get the selected voice"""
        voice_type = self.voice_type.currentText()
        voice = self.voice_selection.currentText()
        
        if voice_type == "Azure Voice":
            voices = self.get_available_voices()
            azure_voices = [voice for voice in voices if voice[1].startswith("en-")]
            for v in azure_voices:
                if v[0] == voice:
                    return v[1]
        else:
            # For Windows voices, we need to find the matching voice ID
            voices = self.get_available_voices()
            windows_voices = [voice for voice in voices if not voice[1].startswith("en-")]
            for v in windows_voices:
                if v[0] == voice:
                    return v[1]
            return None
