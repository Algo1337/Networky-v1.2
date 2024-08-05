import os, time, threading, discord, importlib

class DiscordMessage():
    def __init__(self, message: discord.Message):
        self.message = message;

class Shitcord(discord.Client):
    CMD_ROOT_PATH:      str = "";
    Servers:            dict;
    Message:            discord.message;
    Commands:           dict[str, str] = {};
    def __init__(self, CMD_PATH: str, auto_reload: bool) -> None:
        if not CMD_PATH.strip() or not os.path.isfile(CMD_PATH):
            return;

        self.__CheckCmds();
        
        if auto_reload:
            threading.Thread(target=self.__DetectChanges).start();

    def __CheckCmds(self) -> None:
        bs = os.walk(self.CMD_ROOT_PATH)
    
    def __DetectChanges(self) -> None:
        while True:
            self.__CheckCmds();
            time.sleep(1);
    
    async def on_ready(self):
        self.Servers = self.guilds;

class Library:
    lib:        None;
    path:       str = "";
    vars:       list = [];
    methods:    list = [];
    def __init__(self, lpath: str) -> None:
        if not os.path.exists(lpath.replace(".", "/") + ".py"):
            print("ERROR, MISSING LIB");
            return;
        
        self.path = lpath;
        self._loadLib();

    def _loadLib(self) -> None:
        self.lib = importlib.import_module(self.path);
        if not hasattr(self, "lib"):
            print("ERROR, MISSING LIB");
            return False;
        
        lib_content = open(self.path.replace(".", "/") + ".py", "r").read();

        for line in lib_content.split("\n"):
            if line.startswith("def"):
                self.methods.append(self.__get_method_name(line));
    
    def retrieve_method(self, method_name: str):
        if not hasattr(self.lib, method_name):
            return None;
        
        return getattr(self.lib, method_name);

    """ Specific method for Discord.PY ONLY """
    async def execute_method(self, method_name: str, discord_var) -> bool:
        if not hasattr(self, "lib"):
            print("ERROR, MISSING LIB");
            return False;
        
        if not hasattr(self.lib, method_name):
            print("ERROR, MISSING METHOD");
            return False;
        
        method = getattr(self.lib, method_name);
        await method(discord_var);
        return True;
                
    def __get_method_name(self, line: str) -> str:
        name = "";
        for chr in line.split(" ")[1]:
            if chr == "(":
                break;

            name += chr;

        return name;