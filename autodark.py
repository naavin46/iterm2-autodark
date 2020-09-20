#!/usr/bin/env python3.7

import asyncio
import iterm2
import sys

# Duration between checks
DURATION=300

# Color presets to use
LIGHT_PRESET_NAME="Light"
DARK_PRESET_NAME="Dark"

# Profiles to update
PROFILES=["Default"]

async def dark_mode():
  command = 'defaults read -g AppleInterfaceStyle 2>/dev/null'
  proc = await asyncio.create_subprocess_shell(
      command,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await proc.communicate()
  #print('[{!r} exited with {}]'.format(command, proc.returncode))

  if stdout:
    return True if stdout.decode('ascii').rstrip() == 'Dark' else False
  if stderr:
    print('[stderr] {}'.format(stderr.decode('ascii').rstrip()))
  return False

async def set_colors(connection, preset_name):
  print("[set_colors] Setting the {} preset...".format(preset_name.lower()))
  preset = await iterm2.ColorPreset.async_get(connection, preset_name)
  for partial in (await iterm2.PartialProfile.async_get(connection)):
    if partial.name in PROFILES:
      await partial.async_set_color_preset(preset)

async def main(connection):
  while True:
    is_dark = await dark_mode()
    await asyncio.sleep(1)
    if is_dark:
      await set_colors(connection, DARK_PRESET_NAME)
    else:
      await set_colors(connection, LIGHT_PRESET_NAME)
    await asyncio.sleep(DURATION)

iterm2.run_forever(main)