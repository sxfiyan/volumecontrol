"""
Volume Controller Module
------------------------
Cross-platform system volume abstraction module supporting macOS (AppleScript / osascript),
Windows (Pycaw), and Linux (amixer).
"""

import platform
import subprocess
import os


class VolumeController:
    """
    Handles system volume getting and setting across different OS platforms.
    """
    def __init__(self):
        self.os_name = platform.system()
        self.min_vol = 0
        self.max_vol = 100
        self.is_macos = (self.os_name == "Darwin")
        self.is_windows = (self.os_name == "Windows")
        self.is_linux = (self.os_name == "Linux")

        # Pycaw variables for Windows
        self.volume_object = None

        if self.is_windows:
            self._init_windows_pycaw()

    def _init_windows_pycaw(self):
        """Initializes Pycaw COM objects on Windows platform."""
        try:
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_object = cast(interface, POINTER(IAudioEndpointVolume))
            vol_range = self.volume_object.GetVolumeRange()
            self.min_vol = vol_range[0]  # e.g., -65.25 dB
            self.max_vol = vol_range[1]  # e.g., 0.0 dB
        except Exception as e:
            print(f"[Warning] Pycaw initialization failed on Windows: {e}")

    def get_volume(self):
        """Returns current system volume percentage (0 - 100)."""
        if self.is_macos:
            try:
                cmd = ["osascript", "-e", "output volume of (get volume settings)"]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return int(result.stdout.strip())
            except Exception:
                return 50

        elif self.is_windows and self.volume_object:
            try:
                # Master volume level scalar: 0.0 to 1.0
                vol_scalar = self.volume_object.GetMasterVolumeLevelScalar()
                return int(vol_scalar * 100)
            except Exception:
                return 50

        elif self.is_linux:
            try:
                cmd = "amixer get Master | grep -o -m 1 '[0-9]*%' | tr -d '%'"
                result = subprocess.check_output(cmd, shell=True, text=True)
                return int(result.strip())
            except Exception:
                return 50

        return 50

    def set_volume(self, volume_percent):
        """
        Sets system volume given a target percentage (0 to 100).
        """
        # Clamp to 0-100
        vol_pct = max(0, min(100, int(volume_percent)))

        if self.is_macos:
            try:
                # AppleScript volume setting: 0 to 100
                script = f"set volume output volume {vol_pct}"
                subprocess.run(["osascript", "-e", script], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"[Error] Failed to set macOS volume: {e}")

        elif self.is_windows and self.volume_object:
            try:
                # Pycaw master volume level scalar expects 0.0 to 1.0
                vol_scalar = vol_pct / 100.0
                self.volume_object.SetMasterVolumeLevelScalar(vol_scalar, None)
            except Exception as e:
                print(f"[Error] Failed to set Windows volume: {e}")

        elif self.is_linux:
            try:
                subprocess.run(["amixer", "set", "Master", f"{vol_pct}%"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"[Error] Failed to set Linux volume: {e}")


def main():
    """Testing utility for VolumeController."""
    vc = VolumeController()
    curr_vol = vc.get_volume()
    print(f"Current OS: {vc.os_name}")
    print(f"Current Volume Level: {curr_vol}%")
    
    print("Testing volume set to 30%...")
    vc.set_volume(30)
    print(f"Updated Volume: {vc.get_volume()}%")
    
    print(f"Restoring volume to original {curr_vol}%...")
    vc.set_volume(curr_vol)
    print("Done!")


if __name__ == "__main__":
    main()
