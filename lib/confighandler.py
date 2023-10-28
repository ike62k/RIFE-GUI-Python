import configparser

class ConfigHandler():
    def __init__(self, path: str):
        self.config = configparser.ConfigParser()
        self.__path = path
        self.config.read(self.__path)

    def read_default(self) -> dict:
        self._errorcheck_isdefault()
        return self.config.defaults()
        
    def read_selected(self, section: str, include_default=True) -> dict:
        self.section = section
        self._errorcheck_notselectdefault(self.section)
        self._errorcheck_isselected(self.section)
        config_dict = {}
        for key, value in self.config.items(self.section):
            config_dict[key] = value
        if not include_default:
            config_dict = self._remove_default(config_dict)
        return config_dict
        
    def read_all(self, include_default=True) -> dict:
        section_list = ["DEFAULT"]
        for sec in self.config.sections():
            section_list.append(sec)
        if self.config.defaults == {}:
            section_list.remove("DEFAULT")
        config_dict = {}
        key_and_value = {}
        for sec in section_list:
            for key, value in self.config.items(sec):
                key_and_value[key] = value
            if not include_default:
                key_and_value = self._remove_default(key_and_value.copy())
            config_dict[sec] = key_and_value.copy()
            key_and_value.clear()
        return config_dict

    #ゲッター
    @property
    def get_path(self):
        return self.__path

    #エラー用関数/クラス
    class ConfigError(Exception):
        pass

    def _errorcheck_isdefault(self):
        if self.config.defaults() == {}:
            raise ConfigHandler.ConfigError("There is not DEFAULT section. DEFAULTセクションが存在しません")

    def _errorcheck_isselected(self, section: str):
        if not self.config.has_section(self.section):
            raise ConfigHandler.ConfigError(f"There is not \"{section}\". \"{section}\"というセクションは存在しません")

    def _errorcheck_notselectdefault(self, section: str):
        if section == "DEFAULT":
            raise ConfigHandler.ConfigError("You can't select \"DEFAULT\" section. \"DEFAULT\"セクションは選択できません")

    #内部処理用関数 外部からの参照不可
    def _remove_default(self, target: dict) -> dict:
        if self.config.defaults() != {} and self.config.defaults() != target:
            for key,value in (self.config.defaults()).items():
                if value == target[key]:
                    target.pop(key)
        return target