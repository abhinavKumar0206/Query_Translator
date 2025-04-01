Here's a clear guide for shutting down and restarting your project:

### **How to Properly Shutdown**
1. **Stop Streamlit Server**:
   - In the terminal where Streamlit is running, press:
     ```
     Ctrl + C
     ```
   - Wait until you see: `Server stopped`

2. **Stop Ollama Server** (if running separately):
   - In its terminal, press:
     ```
     Ctrl + C
     ```
   - Or kill it completely:
     ```powershell
     taskkill /f /im ollama.exe
     ```

3. **Close All Terminals**:
   - Simply close all PowerShell/Command Prompt windows

---

### **Restarting Your Project**
Follow these steps in order:

1. **Start Ollama** (in a new terminal):
   ```powershell
   ollama serve
   ```

   if its not running that way then :
   try running this:

   _________________________________________________

   $action = New-ScheduledTaskAction -Execute "ollama" -Argument "serve"
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd
Register-ScheduledTask -TaskName "OllamaService" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest


_______________________________________________________

if this throws some error like :

------------------------------------------------

Register-ScheduledTask : Cannot create a file when that file already exists.
At line:3 char:1
+ Register-ScheduledTask -TaskName "OllamaService" -Action $action -Tri ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ResourceExists: (PS_ScheduledTask:Root/Microsoft/...S_ScheduledTask) [Register-Scheduled
   Task], CimException
    + FullyQualifiedErrorId : HRESULT 0x800700b7,Register-ScheduledTask

 ---------------------------------------------------------

 then run this and run the above(previous) command again

 _______________________________________________________________

 Unregister-ScheduledTask -TaskName "OllamaService" -Confirm:$false

 ___________________________________________________________________   


   *Keep this terminal open*

2. **Activate Virtual Environment** (new terminal):
   ```powershell
   cd C:\Users\ab141\Desktop\SIGMA\PROJECTS\_query_translator
   venv\Scripts\activate
   ```

3. **Run Streamlit App** (same terminal):
   ```powershell
   streamlit run streamlit_app.py
   ```

---

### **Quick Reference Cheatsheet**
| Action                | Command                          |
|-----------------------|----------------------------------|
| **Stop Streamlit**    | `Ctrl + C` (in running terminal) |
| **Stop Ollama**       | `Ctrl + C` or `taskkill /f /im ollama.exe` |
| **Start Ollama**      | `ollama serve`                   |
| **Restart Project**   | `venv\Scripts\activate` → `streamlit run streamlit_app.py` |

### **Pro Tips**
1. If ports are stuck (especially 8501 or 11434):
   ```powershell
   netstat -ano | findstr 8501
   taskkill /pid [PID] /f
   ```

2. For complete freshness:
   ```powershell
   # After shutdown
   del /q venv\Lib\site-packages\*  # Clears cached packages
   ```

3. Bookmark these commands in your project's `README.md` for quick reference.

Would you like me to create a batch file that automates this start/stop process for you?